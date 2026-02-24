"""
SA Crime Monitor — Backend API
================================
Flask server that:
1. Serves the frontend
2. Provides REST API for crime station data with trends
3. Scrapes live crime news from SA news RSS feeds
4. Computes weekly/monthly Top 10 leaderboards
5. Stores scraped incidents in a local JSON database

Endpoints:
  GET /                    → Frontend
  GET /api/stations        → All station data with trends
  GET /api/stations?prov=GP&crime=murder → Filtered
  GET /api/feed            → Live scraped crime feed (latest 100)
  GET /api/feed/scrape     → Trigger manual scrape
  GET /api/leaderboard?period=weekly&cat=murder → Top 10
  GET /api/trends          → National trend summary
  GET /api/stats           → Dashboard stats
"""

import os
import json
import time
import threading
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from scrapers.news_scraper import NewsScraper
from data.stations import STATIONS
from data.trend_engine import TrendEngine

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize components
scraper = NewsScraper()
trend_engine = TrendEngine(STATIONS)

# In-memory feed store (persisted to disk)
FEED_FILE = os.path.join(os.path.dirname(__file__), 'data', 'feed_cache.json')
feed_items = []

def load_feed():
    global feed_items
    if os.path.exists(FEED_FILE):
        try:
            with open(FEED_FILE, 'r') as f:
                feed_items = json.load(f)
        except:
            feed_items = []

def save_feed():
    try:
        with open(FEED_FILE, 'w') as f:
            json.dump(feed_items[-500:], f)  # Keep last 500
    except:
        pass

def do_scrape():
    """Run all scrapers and merge new items"""
    global feed_items
    new_items = scraper.scrape_all()
    
    # Deduplicate by title similarity
    existing_titles = {item.get('title', '').lower()[:60] for item in feed_items}
    for item in new_items:
        key = item.get('title', '').lower()[:60]
        if key and key not in existing_titles:
            feed_items.insert(0, item)
            existing_titles.add(key)
    
    # Keep most recent 500
    feed_items = feed_items[:500]
    save_feed()
    return len(new_items)

# Background scraper thread
def scrape_loop():
    """Scrape every 10 minutes"""
    while True:
        try:
            count = do_scrape()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Scraped {count} new items. Total: {len(feed_items)}")
        except Exception as e:
            print(f"[Scrape Error] {e}")
        time.sleep(600)  # 10 minutes

# ======================== ROUTES ========================

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/stations')
def api_stations():
    """Return all station data with optional filtering"""
    prov = request.args.get('prov', 'all')
    crime = request.args.get('crime', 'all')
    search = request.args.get('q', '').lower()
    
    results = []
    for s in STATIONS:
        # Province filter
        if prov != 'all' and s['p'] != prov:
            continue
        # Search filter
        if search and search not in s['n'].lower() and search not in s['a'].lower():
            continue
        
        # Calculate totals and trends
        if crime == 'all':
            cur_total = sum(s['c'].values())
            prev_total = sum(s['prev'].values())
        else:
            cur_total = s['c'].get(crime, 0)
            prev_total = s['prev'].get(crime, 0)
        
        if cur_total == 0:
            continue
        
        # YoY trend
        if prev_total > 0:
            pct = round((cur_total - prev_total) / prev_total * 100, 1)
        else:
            pct = 0
        
        trend_dir = 'up' if pct > 2 else ('dn' if pct < -2 else 'eq')
        
        results.append({
            **s,
            'total': cur_total,
            'prev_total': prev_total,
            'trend_pct': abs(pct),
            'trend_dir': trend_dir,
            # Per-crime trends
            'crime_trends': {
                k: {
                    'current': s['c'].get(k, 0),
                    'previous': s['prev'].get(k, 0),
                    'pct': round(((s['c'].get(k,0) - s['prev'].get(k,0)) / s['prev'].get(k,1)) * 100, 1) if s['prev'].get(k,0) > 0 else 0
                } for k in s['c'].keys()
            }
        })
    
    results.sort(key=lambda x: x['total'], reverse=True)
    return jsonify({'stations': results, 'count': len(results)})

@app.route('/api/feed')
def api_feed():
    """Return latest crime feed items"""
    limit = int(request.args.get('limit', 50))
    prov = request.args.get('prov', '')
    crime_type = request.args.get('type', '')
    
    items = feed_items
    if prov:
        items = [i for i in items if i.get('province', '') == prov]
    if crime_type:
        items = [i for i in items if i.get('crime_type', '') == crime_type]
    
    return jsonify({'items': items[:limit], 'total': len(items)})

@app.route('/api/feed/scrape')
def api_scrape():
    """Manually trigger a scrape"""
    count = do_scrape()
    return jsonify({'scraped': count, 'total': len(feed_items)})

@app.route('/api/leaderboard')
def api_leaderboard():
    """Top 10 crime stations with movement"""
    period = request.args.get('period', 'weekly')  # weekly, monthly, quarterly
    cat = request.args.get('cat', 'total')  # total, murder, robbery, kidnap, carjack
    
    results = trend_engine.leaderboard(period, cat)
    return jsonify({'leaderboard': results, 'period': period, 'category': cat})

@app.route('/api/trends')
def api_trends():
    """National trend summary"""
    return jsonify(trend_engine.national_trends())

@app.route('/api/stats')
def api_stats():
    """Dashboard quick stats"""
    total_crimes = sum(sum(s['c'].values()) for s in STATIONS)
    total_murders = sum(s['c'].get('murder', 0) for s in STATIONS)
    total_robbery = sum(s['c'].get('robbery', 0) for s in STATIONS)
    total_kidnap = sum(s['c'].get('kidnap', 0) for s in STATIONS)
    total_carjack = sum(s['c'].get('carjack', 0) for s in STATIONS)
    
    prev_crimes = sum(sum(s['prev'].values()) for s in STATIONS)
    overall_trend = round((total_crimes - prev_crimes) / prev_crimes * 100, 1) if prev_crimes > 0 else 0
    
    return jsonify({
        'total_crimes': total_crimes,
        'total_murders': total_murders,
        'total_robbery': total_robbery,
        'total_kidnap': total_kidnap,
        'total_carjack': total_carjack,
        'stations': len(STATIONS),
        'overall_trend_pct': overall_trend,
        'overall_trend_dir': 'up' if overall_trend > 0 else 'dn',
        'feed_items': len(feed_items),
        'last_scrape': feed_items[0].get('scraped_at', '') if feed_items else 'Never'
    })

# ======================== FORECASTING (Side Quest) ========================

from data.forecaster import register_forecast_routes
register_forecast_routes(app, STATIONS)

from data.micro_hotspots import MICRO_HOTSPOTS, get_hotspots_for_station, get_hotspots_by_province, get_hotspots_by_risk

@app.route('/api/hotspots')
def api_micro_hotspots():
    """Street-level micro-hotspots with specific crime incidents"""
    station = request.args.get('station', '')
    prov = request.args.get('prov', '')
    min_risk = int(request.args.get('min_risk', 0))
    
    if station:
        results = get_hotspots_for_station(station)
    elif prov:
        results = get_hotspots_by_province(prov)
    elif min_risk:
        results = get_hotspots_by_risk(min_risk)
    else:
        results = MICRO_HOTSPOTS
    
    return jsonify({'hotspots': results, 'count': len(results)})

@app.route('/api/hotspots/dangerous')
def api_dangerous_spots():
    """Top most dangerous specific locations"""
    limit = int(request.args.get('limit', 20))
    results = get_hotspots_by_risk(7)[:limit]
    return jsonify({'hotspots': results, 'count': len(results)})

# ======================== STARTUP ========================

if __name__ == '__main__':
    load_feed()
    
    # Do initial scrape
    print("🇿🇦 SA Crime Monitor Backend starting...")
    print("📡 Running initial scrape...")
    try:
        count = do_scrape()
        print(f"✅ Initial scrape: {count} items")
    except Exception as e:
        print(f"⚠️  Initial scrape failed: {e}")
    
    # Start background scraper
    scrape_thread = threading.Thread(target=scrape_loop, daemon=True)
    scrape_thread.start()
    print("🔄 Background scraper running (every 10 min)")
    
    print("🚀 Server starting on http://localhost:5000")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
