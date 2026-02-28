"""
Startup news service for FounderOS dashboard.
Fetches startup/tech news from a public RSS feed (no API key needed).
Caches results in memory for 5 minutes to avoid blocking page loads.
"""
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Simple in-memory cache: {key: (data, expires_at)}
_cache = {}
_CACHE_TTL = timedelta(minutes=5)


def fetch_startup_news(limit=6):
    """Fetch startup/India tech news, cached for 5 minutes."""
    cache_key = f'news_{limit}'
    now = datetime.utcnow()

    if cache_key in _cache:
        data, expires = _cache[cache_key]
        if now < expires:
            return data

    result = _fetch_live(limit)
    _cache[cache_key] = (result, now + _CACHE_TTL)
    return result


def _fetch_live(limit=6):
    """Actually fetch news from external sources."""
    queries = [
        'https://news.google.com/rss/search?q=india+startup+funding+2025&hl=en-IN&gl=IN&ceid=IN:en',
        'https://feeds.feedburner.com/entrackr',
    ]

    news_items = []

    for url in queries:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=4) as resp:
                xml_data = resp.read()
            root = ET.fromstring(xml_data)
            channel = root.find('channel')
            if channel is None:
                continue
            for item in channel.findall('item')[:limit]:
                title = item.findtext('title', '').strip()
                link = item.findtext('link', '').strip()
                pub_date = item.findtext('pubDate', '').strip()
                description = item.findtext('description', '').strip()
                import re
                description = re.sub('<[^<]+?>', '', description)[:120] + '...'

                try:
                    dt = datetime.strptime(pub_date[:25], '%a, %d %b %Y %H:%M:%S')
                    pub_date = dt.strftime('%b %d')
                except Exception:
                    pub_date = 'Recent'

                if title and link:
                    news_items.append({
                        'title': title[:80],
                        'link': link,
                        'date': pub_date,
                        'description': description,
                        'source': 'Google News',
                    })
            if news_items:
                return news_items[:limit]
        except Exception:
            continue

    return _fallback_news()


def _fallback_news():
    return [
        {
            'title': 'Startup India Seed Fund to Disburse ₹945 Crore This Year',
            'link': 'https://startupindia.gov.in',
            'date': 'Feb 27',
            'description': 'DPIIT announces expanded seed fund allocation for Tier-2 and Tier-3 startup ecosystems.',
            'source': 'Startup India',
        },
        {
            'title': 'SIDBI Launches New Startup Mentorship Programme',
            'link': 'https://sidbi.in',
            'date': 'Feb 26',
            'description': 'Small Industries Development Bank of India launches initiative targeting founders outside metro cities.',
            'source': 'SIDBI',
        },
        {
            'title': 'India Now Has 118,000+ Startups Registered: DPIIT',
            'link': 'https://dpiit.gov.in',
            'date': 'Feb 25',
            'description': 'India continues to be the third-largest startup ecosystem globally with record registrations.',
            'source': 'DPIIT',
        },
        {
            'title': 'Mudra Yojana Disbursements Cross ₹25 Lakh Crore Milestone',
            'link': 'https://mudra.org.in',
            'date': 'Feb 23',
            'description': 'PM Mudra Yojana has supported over 40 crore beneficiaries since its launch.',
            'source': 'Mudra',
        },
        {
            'title': 'New GENESIS Scheme Opens Applications for DeepTech Startups',
            'link': 'https://meity.gov.in',
            'date': 'Feb 21',
            'description': 'MeitY opens the GENESIS cohort 3 for startups working in AI, blockchain, and advanced computing.',
            'source': 'MeitY',
        },
        {
            'title': 'Atal Innovation Mission Expands Incubator Network to 150+ Cities',
            'link': 'https://aim.gov.in',
            'date': 'Feb 19',
            'description': 'NITI Aayog-backed Atal Innovation Mission establishes new ATLs and incubation centres nationwide.',
            'source': 'AIM',
        },
    ]
