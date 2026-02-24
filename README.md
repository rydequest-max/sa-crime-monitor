# 🇿🇦 SA Crime Monitor — Backend

Real-time crime monitoring dashboard for South Africa with live news scraping, trend analysis, leaderboards, and crime forecasting.

## Features

- **Interactive Map** — 45+ police stations across all 9 provinces with Leaflet.js
- **Live News Feed** — Scrapes crime articles from News24, IOL, EWN, Daily Maverick, TimesLIVE, SABC every 10 minutes
- **Trend Analysis** — Year-over-Year comparison with ▲▼ indicators per station and crime type
- **Kidnapping Tracking** — Dedicated tracking (264% increase over past decade)
- **Top 10 Leaderboard** — Weekly/Monthly/Quarterly rankings with position movement
- **Crime Forecasting** — Predictive analytics using weighted moving averages, seasonal decomposition, and risk scoring
- **What-If Scenarios** — Model the impact of policing interventions (based on real LEAP data)
- **Street-Level Zoom** — Switches to OpenStreetMap at zoom 15+ for street names

## Quick Start

```bash
# Clone or extract the project
cd sa-crime-backend

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Server starts at **http://localhost:5000**

## API Endpoints

### Core Data
| Endpoint | Description |
|---|---|
| `GET /` | Frontend dashboard |
| `GET /api/stations` | All station data with trends |
| `GET /api/stations?prov=GP&crime=murder&q=soweto` | Filtered stations |
| `GET /api/feed` | Live scraped crime feed |
| `GET /api/feed?limit=20&prov=WC&type=murder` | Filtered feed |
| `GET /api/feed/scrape` | Trigger manual scrape |
| `GET /api/leaderboard?period=weekly&cat=murder` | Top 10 rankings |
| `GET /api/trends` | National trend summary |
| `GET /api/stats` | Dashboard quick stats |

### Forecasting (Side Quest 🔮)
| Endpoint | Description |
|---|---|
| `GET /api/forecast?quarters=1` | Forecast all stations |
| `GET /api/forecast/province?prov=GP&quarters=2` | Province forecast |
| `GET /api/forecast/hotspots` | Emerging/persistent hotspot prediction |
| `GET /api/forecast/whatif?station=Nyanga&intervention=moderate` | What-if scenario |

### Intervention Scenarios
- `none` — Baseline (no change)
- `moderate` — 15% policing increase (LEAP-style)
- `aggressive` — 30% increase + intelligence operations
- `comprehensive` — Full intervention (policing + social programs)

## Project Structure

```
sa-crime-backend/
├── app.py                    # Flask server + API routes
├── requirements.txt          # Python dependencies
├── static/
│   └── index.html           # Frontend (API-connected)
├── scrapers/
│   ├── __init__.py
│   └── news_scraper.py      # RSS + web scraper (6 SA sources)
├── data/
│   ├── __init__.py
│   ├── stations.py          # 45+ stations with current + previous data
│   ├── trend_engine.py      # Leaderboard + national trends
│   ├── forecaster.py        # Crime forecasting engine
│   └── feed_cache.json      # Auto-generated feed cache
└── README.md
```

## Data Sources

| Source | Type | URL |
|---|---|---|
| SAPS Official | Quarterly stats | saps.gov.za/services/crimestats.php |
| CrimeStatsSA | Annual breakdown | crimestatssa.com |
| CrimeHub (ISS) | Analysis + maps | crimehub.org |
| ISS Africa | Research | issafrica.org |
| News24 | Live news (RSS) | news24.com |
| IOL | Live news (RSS) | iol.co.za |
| EWN | Live news (RSS) | ewn.co.za |
| Daily Maverick | Live news (web) | dailymaverick.co.za |
| TimesLIVE | Live news (RSS) | timeslive.co.za |
| SABC News | Live news (web) | sabcnews.com |

## Deployment

### Option 1: Local
```bash
python app.py
```

### Option 2: Railway / Render
1. Push to GitHub
2. Connect repo to Railway or Render
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python app.py`
5. Set port: `5000`

### Option 3: VPS (Ubuntu)
```bash
sudo apt update && sudo apt install python3-pip
pip3 install -r requirements.txt
# Run with gunicorn for production
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 4: Docker
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

## Forecasting Details

The forecasting engine uses:

1. **Weighted Moving Average** — Recent quarters weighted 70% of observed rate (dampened for mean reversion)
2. **Seasonal Adjustment** — Crime peaks in Oct-Dec (festive season): murder +18%, robbery +15%, property +20%
3. **Risk Score** — Composite 0-100 index:
   - 40% crime volume (log scale)
   - 30% growth trajectory
   - 20% violence ratio (murder + assault / total)
   - 10% kidnapping weight

4. **What-If Scenarios** — Based on real outcomes:
   - LEAP programme: 9.4% murder reduction
   - Gauteng Robbery Strategy: 32% hijacking reduction
   - Operation Restore: 25% contact crime reduction

### Future ML Pipeline (with more data)
- ARIMA/SARIMA time series
- Facebook Prophet for seasonality
- XGBoost on socioeconomic features
- LSTM neural networks
- Geospatial DBSCAN clustering
- Correlation with unemployment, load-shedding, weather

## License

Research and educational use. Data sourced from public SAPS statistics.
Crime data is the property of the South African Police Service.
