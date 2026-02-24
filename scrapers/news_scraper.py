"""
News Scraper for SA Crime Monitor
==================================
Scrapes crime news from multiple South African sources:
- News24 RSS
- IOL Crime RSS  
- Daily Maverick
- EWN (Eyewitness News)
- TimesLIVE
- SABC News

Each item is classified by:
- Crime type (murder, robbery, assault, carjacking, kidnapping, etc.)
- Province (GP, WC, KZN, EC, etc.)
- Location (specific area/township)
"""

import re
import hashlib
from datetime import datetime
from typing import List, Dict

import requests
import feedparser
from bs4 import BeautifulSoup

# Crime type detection keywords
CRIME_KEYWORDS = {
    'murder': ['murder', 'killed', 'fatal', 'shot dead', 'stabbed to death', 'homicide', 'slain', 'found dead', 'body found', 'gunned down'],
    'robbery': ['robbery', 'robbed', 'armed robbery', 'heist', 'cash-in-transit', 'CIT', 'held up', 'store robbery', 'business robbery'],
    'assault': ['assault', 'attacked', 'beaten', 'GBH', 'grievous bodily harm', 'stabbed', 'brawl', 'fight'],
    'carjack': ['hijack', 'carjack', 'car hijack', 'vehicle hijack', 'smash and grab', 'car theft'],
    'kidnapping': ['kidnap', 'abducted', 'ransom', 'hostage', 'snatched', 'missing person', 'taken captive'],
    'shooting': ['shooting', 'shots fired', 'gunfire', 'drive-by', 'mass shooting', 'crossfire'],
    'burglary': ['burglary', 'break-in', 'housebreaking', 'breaking and entering', 'theft', 'stolen'],
    'sexual': ['rape', 'sexual assault', 'sexual offence', 'GBV', 'gender-based violence', 'molest'],
    'drugs': ['drugs', 'narcotics', 'dagga', 'tik', 'methamphetamine', 'cocaine', 'mandrax', 'drug bust', 'drug lab'],
    'gang': ['gang', 'gang-related', 'gang violence', 'turf war'],
    'extortion': ['extortion', 'protection racket', 'construction mafia'],
}

# Province detection
PROVINCE_KEYWORDS = {
    'WC': ['cape town', 'western cape', 'stellenbosch', 'paarl', 'george', 'knysna', 'nyanga', 'khayelitsha', 
           'mitchells plain', 'delft', 'gugulethu', 'langa', 'manenberg', 'bishop lavis', 'bellville',
           'mfuleni', 'kraaifontein', 'philippi', 'athlone', 'grassy park', 'lavender hill', 'hanover park',
           'cape flats', 'table bay', 'atlantis', 'muizenberg', 'fish hoek', 'worcester', 'hermanus'],
    'GP': ['johannesburg', 'gauteng', 'pretoria', 'tshwane', 'soweto', 'alexandra', 'sandton', 'midrand',
           'tembisa', 'katlehong', 'germiston', 'benoni', 'springs', 'boksburg', 'kempton park',
           'hillbrow', 'diepsloot', 'orange farm', 'mamelodi', 'soshanguve', 'centurion', 'randburg',
           'roodepoort', 'krugersdorp', 'kagiso', 'ekurhuleni', 'vereeniging', 'sebokeng', 'daveyton'],
    'KZN': ['durban', 'kwazulu-natal', 'kzn', 'pietermaritzburg', 'pmb', 'umlazi', 'inanda', 'kwamashu',
            'chatsworth', 'phoenix', 'pinetown', 'newcastle', 'richards bay', 'ladysmith', 'ethekwini',
            'plessislaer', 'ntuzuma', 'hammarsdale', 'port shepstone', 'empangeni'],
    'EC': ['eastern cape', 'port elizabeth', 'gqeberha', 'east london', 'mthatha', 'motherwell',
           'kwanobuhle', 'mdantsane', 'uitenhage', 'grahamstown', 'makhanda', 'queenstown', 'nelson mandela bay',
           'ibhayi', 'kwazakele', 'lusikisiki', 'buffalo city'],
    'MP': ['mpumalanga', 'nelspruit', 'mbombela', 'witbank', 'emalahleni', 'secunda', 'ermelo', 'standerton'],
    'NW': ['north west', 'rustenburg', 'mafikeng', 'mahikeng', 'klerksdorp', 'potchefstroom', 'brits', 'boitekong'],
    'FS': ['free state', 'bloemfontein', 'mangaung', 'welkom', 'kroonstad', 'sasolburg', 'botshabelo'],
    'LP': ['limpopo', 'polokwane', 'thohoyandou', 'giyani', 'tzaneen', 'mokopane', 'musina', 'lephalale'],
    'NC': ['northern cape', 'kimberley', 'upington', 'de aar', 'springbok'],
}

# RSS Feed sources
RSS_FEEDS = [
    {
        'name': 'News24 Crime',
        'url': 'https://feeds.news24.com/articles/news24/SouthAfrica/rss',
        'base_url': 'https://www.news24.com',
        'icon': '📰'
    },
    {
        'name': 'IOL Crime',
        'url': 'https://rss.iol.io/iol/news',
        'base_url': 'https://www.iol.co.za',
        'icon': '📰'
    },
    {
        'name': 'EWN',
        'url': 'https://ewn.co.za/RSS/EWNHomePage.xml',
        'base_url': 'https://ewn.co.za',
        'icon': '📻'
    },
    {
        'name': 'TimesLIVE',
        'url': 'https://www.timeslive.co.za/rss/',
        'base_url': 'https://www.timeslive.co.za',
        'icon': '📰'
    },
]

# Web scrape targets (used when RSS not available)
WEB_SOURCES = [
    {
        'name': 'Daily Maverick',
        'url': 'https://www.dailymaverick.co.za/section/crime-justice/',
        'base_url': 'https://www.dailymaverick.co.za',
        'icon': '📰'
    },
    {
        'name': 'SABC Crime',
        'url': 'https://www.sabcnews.com/sabcnews/category/south-africa/crime/',
        'base_url': 'https://www.sabcnews.com',
        'icon': '📺'
    },
]

HEADERS = {
    'User-Agent': 'SA-Crime-Monitor/1.0 (Research Tool; +https://github.com/sa-crime-monitor)'
}


class NewsScraper:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.session.timeout = 15
    
    def scrape_all(self) -> List[Dict]:
        """Scrape all sources and return classified crime items"""
        all_items = []
        
        # 1. RSS Feeds
        for feed in RSS_FEEDS:
            try:
                items = self._scrape_rss(feed)
                all_items.extend(items)
            except Exception as e:
                print(f"  [RSS Error] {feed['name']}: {e}")
        
        # 2. Web scraping
        for source in WEB_SOURCES:
            try:
                items = self._scrape_web(source)
                all_items.extend(items)
            except Exception as e:
                print(f"  [Web Error] {source['name']}: {e}")
        
        # Filter to crime-related only
        crime_items = [item for item in all_items if item.get('crime_type')]
        
        # Add scrape timestamp
        now = datetime.now().isoformat()
        for item in crime_items:
            item['scraped_at'] = now
        
        return crime_items
    
    def _scrape_rss(self, feed_config: Dict) -> List[Dict]:
        """Parse RSS feed and extract crime items"""
        items = []
        
        try:
            resp = self.session.get(feed_config['url'], timeout=10)
            parsed = feedparser.parse(resp.content)
        except:
            # Try feedparser directly with URL
            parsed = feedparser.parse(feed_config['url'])
        
        for entry in parsed.entries[:30]:  # Last 30 articles
            title = entry.get('title', '')
            summary = entry.get('summary', entry.get('description', ''))
            link = entry.get('link', '')
            published = entry.get('published', entry.get('updated', ''))
            
            # Clean HTML from summary
            if summary:
                summary = BeautifulSoup(summary, 'html.parser').get_text()[:300]
            
            # Classify
            crime_type = self._classify_crime(title + ' ' + summary)
            province = self._detect_province(title + ' ' + summary)
            location = self._extract_location(title + ' ' + summary)
            
            if crime_type:  # Only crime-related
                items.append({
                    'title': title[:200],
                    'description': summary[:300],
                    'url': link,
                    'source': feed_config['name'],
                    'source_icon': feed_config['icon'],
                    'source_url': feed_config['base_url'],
                    'published': published,
                    'crime_type': crime_type,
                    'province': province,
                    'location': location,
                    'id': hashlib.md5(title.encode()).hexdigest()[:12],
                })
        
        return items
    
    def _scrape_web(self, source_config: Dict) -> List[Dict]:
        """Scrape crime articles from a web page"""
        items = []
        
        try:
            resp = self.session.get(source_config['url'], timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
        except Exception as e:
            return items
        
        # Find article links - generic approach
        articles = soup.find_all('a', href=True)
        seen = set()
        
        for a in articles:
            href = a.get('href', '')
            title = a.get_text(strip=True)
            
            if not title or len(title) < 20 or len(title) > 250:
                continue
            
            # Make absolute URL
            if href.startswith('/'):
                href = source_config['base_url'] + href
            
            # Skip non-article links
            if not any(x in href for x in ['/article/', '/news/', '/crime', '2025', '2026', '2024']):
                continue
            
            # Deduplicate
            title_key = title.lower()[:50]
            if title_key in seen:
                continue
            seen.add(title_key)
            
            # Classify
            crime_type = self._classify_crime(title)
            province = self._detect_province(title)
            location = self._extract_location(title)
            
            if crime_type:
                items.append({
                    'title': title[:200],
                    'description': '',
                    'url': href,
                    'source': source_config['name'],
                    'source_icon': source_config['icon'],
                    'source_url': source_config['base_url'],
                    'published': datetime.now().isoformat(),
                    'crime_type': crime_type,
                    'province': province,
                    'location': location,
                    'id': hashlib.md5(title.encode()).hexdigest()[:12],
                })
        
        return items[:20]  # Max 20 per source
    
    def _classify_crime(self, text: str) -> str:
        """Classify text into crime type"""
        text_lower = text.lower()
        
        # Check each crime type
        scores = {}
        for crime_type, keywords in CRIME_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[crime_type] = score
        
        if not scores:
            return ''  # Not a crime article
        
        # Return highest scoring type
        return max(scores, key=scores.get)
    
    def _detect_province(self, text: str) -> str:
        """Detect which province the article is about"""
        text_lower = text.lower()
        
        scores = {}
        for prov, keywords in PROVINCE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[prov] = score
        
        if not scores:
            return ''
        
        return max(scores, key=scores.get)
    
    def _extract_location(self, text: str) -> str:
        """Extract specific location/area name from text"""
        text_lower = text.lower()
        
        # Check all known location keywords
        all_locations = []
        for prov_keywords in PROVINCE_KEYWORDS.values():
            for kw in prov_keywords:
                if kw in text_lower:
                    all_locations.append(kw.title())
        
        if all_locations:
            return all_locations[0]  # Most specific match
        return ''


if __name__ == '__main__':
    # Test the scraper
    scraper = NewsScraper()
    print("🔍 Testing scraper...")
    items = scraper.scrape_all()
    print(f"\n✅ Found {len(items)} crime articles:")
    for item in items[:10]:
        print(f"  [{item['crime_type']:>10}] [{item['province']:>3}] {item['title'][:80]}")
        print(f"             📰 {item['source']} → {item['url'][:60]}")
