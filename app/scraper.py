import requests
from bs4 import BeautifulSoup
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class QuoteScraper:
    """Web scraper for collecting quotes from multiple sources"""
    
    def __init__(self):
        self.session = self._create_session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _create_session(self):
        """Create a requests session with retry strategy"""
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=(500, 502, 604),
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        # Disable SSL verification for development
        session.verify = False
        return session
    
    def get_life_quotes(self):
        """Scrape life quotes"""
        quotes = []
        try:
            # Source 1: quotable.io API for life category
            url = "https://api.quotable.io/quotes?tags=life&limit=150"
            response = self.session.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for quote in data.get('results', []):
                    quotes.append({
                        'text': quote['content'],
                        'author': quote.get('author', 'Unknown').replace(', type.unknown', '')
                    })
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping life quotes: {e}")
        
        return quotes[:100]
    
    def get_wisdom_quotes(self):
        """Scrape wisdom quotes"""
        quotes = []
        try:
            # Source: quotable.io API for wisdom category
            url = "https://api.quotable.io/quotes?tags=wisdom&limit=150"
            response = self.session.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for quote in data.get('results', []):
                    quotes.append({
                        'text': quote['content'],
                        'author': quote.get('author', 'Unknown').replace(', type.unknown', '')
                    })
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping wisdom quotes: {e}")
        
        return quotes[:100]
    
    def get_motivation_quotes(self):
        """Scrape motivation quotes"""
        quotes = []
        try:
            url = "https://api.quotable.io/quotes?tags=motivational&limit=150"
            response = self.session.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for quote in data.get('results', []):
                    quotes.append({
                        'text': quote['content'],
                        'author': quote.get('author', 'Unknown').replace(', type.unknown', '')
                    })
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping motivation quotes: {e}")
        
        return quotes[:100]
    
    def get_success_quotes(self):
        """Scrape success quotes"""
        quotes = []
        try:
            url = "https://api.quotable.io/quotes?tags=success&limit=150"
            response = self.session.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for quote in data.get('results', []):
                    quotes.append({
                        'text': quote['content'],
                        'author': quote.get('author', 'Unknown').replace(', type.unknown', '')
                    })
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping success quotes: {e}")
        
        return quotes[:100]
    
    def get_friendship_quotes(self):
        """Scrape friendship quotes"""
        quotes = []
        try:
            url = "https://api.quotable.io/quotes?tags=friendship&limit=150"
            response = self.session.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for quote in data.get('results', []):
                    quotes.append({
                        'text': quote['content'],
                        'author': quote.get('author', 'Unknown').replace(', type.unknown', '')
                    })
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping friendship quotes: {e}")
        
        return quotes[:100]
    
    def get_love_quotes(self):
        """Scrape love quotes"""
        quotes = []
        try:
            url = "https://api.quotable.io/quotes?tags=love&limit=150"
            response = self.session.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for quote in data.get('results', []):
                    quotes.append({
                        'text': quote['content'],
                        'author': quote.get('author', 'Unknown').replace(', type.unknown', '')
                    })
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping love quotes: {e}")
        
        return quotes[:100]
    
    def get_inspiration_quotes(self):
        """Scrape inspiration quotes"""
        quotes = []
        try:
            url = "https://api.quotable.io/quotes?tags=inspirational&limit=150"
            response = self.session.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for quote in data.get('results', []):
                    quotes.append({
                        'text': quote['content'],
                        'author': quote.get('author', 'Unknown').replace(', type.unknown', '')
                    })
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping inspiration quotes: {e}")
        
        return quotes[:100]
    
    def get_faith_quotes(self):
        """Scrape faith and spirituality quotes"""
        quotes = []
        try:
            url = "https://api.quotable.io/quotes?tags=faith&limit=150"
            response = self.session.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for quote in data.get('results', []):
                    quotes.append({
                        'text': quote['content'],
                        'author': quote.get('author', 'Unknown').replace(', type.unknown', '')
                    })
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping faith quotes: {e}")
        
        return quotes[:100]
    
    def get_courage_quotes(self):
        """Scrape courage quotes"""
        quotes = []
        try:
            url = "https://api.quotable.io/quotes?tags=courage&limit=150"
            response = self.session.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for quote in data.get('results', []):
                    quotes.append({
                        'text': quote['content'],
                        'author': quote.get('author', 'Unknown').replace(', type.unknown', ''),
                        'source': 'quotable.io'
                    })
            time.sleep(1)
        except Exception as e:
            print(f"Error scraping courage quotes: {e}")
        
        return quotes[:100]
    
    def all_quotes(self):
        """Get all quote categories"""
        return {
            'Life': self.get_life_quotes(),
            'Wisdom': self.get_wisdom_quotes(),
            'Motivation': self.get_motivation_quotes(),
            'Success': self.get_success_quotes(),
            'Friendship': self.get_friendship_quotes(),
            'Love': self.get_love_quotes(),
            'Inspiration': self.get_inspiration_quotes(),
            'Faith': self.get_faith_quotes(),
            'Courage': self.get_courage_quotes(),
        }
