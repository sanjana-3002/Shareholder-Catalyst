import requests
import os
from typing import Dict, List
from datetime import datetime, timedelta
import time
import re

class SECFetcher:
    """Fetches real SEC filings from EDGAR database"""
    
    BASE_URL = "https://www.sec.gov"
    
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        # SEC REQUIRES User-Agent header with contact info
        self.headers = {
            'User-Agent': 'ActivistIntel demo@activist.com',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.sec.gov'
        }
        self.cik = None
        self.company_name = None
    
    def _get_cik(self) -> str:
        """Convert ticker to CIK (Central Index Key) using SEC API"""
        
        print(f"  🔍 Looking up CIK for {self.ticker}...")
        
        # Use SEC company tickers JSON (updated daily)
        tickers_url = f"{self.BASE_URL}/files/company_tickers.json"
        
        try:
            response = requests.get(tickers_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Find ticker in data
            for entry in data.values():
                if entry['ticker'].upper() == self.ticker:
                    self.cik = str(entry['cik_str']).zfill(10)
                    self.company_name = entry['title']
                    print(f"    ✅ Found: {self.company_name} (CIK: {self.cik})")
                    return self.cik
            
            raise ValueError(f"Ticker {self.ticker} not found in SEC database")
            
        except Exception as e:
            print(f"    ❌ Error fetching CIK: {str(e)}")
            raise
    
    def fetch_filings(self, filing_types: List[str], years: int = 3) -> Dict:
        """
        Fetch real SEC filings from EDGAR
        """
        
        if not self.cik:
            self._get_cik()
        
        print(f"\n📄 Fetching SEC filings for {self.company_name} ({self.ticker})")
        print(f"   Looking for: {', '.join(filing_types)}")
        
        results = {}
        
        for filing_type in filing_types:
            print(f"\n  → Searching for {filing_type} filings...")
            results[filing_type] = self._fetch_filing_type(filing_type, years)
            time.sleep(0.2)
        
        return results
    
    def _fetch_filing_type(self, filing_type: str, years: int) -> List[Dict]:
        """Fetch filings using SEC's newer JSON API"""
        
        try:
            # Use SEC's submissions endpoint (returns JSON)
            submissions_url = f"{self.BASE_URL}/cgi-bin/browse-edgar"
            
            params = {
                'action': 'getcompany',
                'CIK': self.cik,
                'type': filing_type,
                'dateb': '',
                'owner': 'exclude',
                'start': 0,
                'count': 100,
                'output': 'atom'
            }
            
            response = requests.get(
                submissions_url,
                params=params,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            
            # Parse the ATOM XML feed
            filings = self._parse_atom_feed(response.text, years)
            
            if not filings:
                print(f"    ⚠️  No {filing_type} filings found in last {years} years")
                return []
            
            print(f"    ✅ Found {len(filings)} {filing_type} filing(s)")
            
            # Download first 3 filings
            downloaded = []
            for filing in filings[:3]:
                result = self._download_filing(filing, filing_type)
                if result:
                    downloaded.append(result)
                    time.sleep(0.2)
            
            return downloaded
            
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            return []
    
    def _parse_atom_feed(self, xml_content: str, years: int) -> List[Dict]:
        """Parse SEC ATOM feed using regex (reliable method)"""
        
        filings = []
        cutoff_date = datetime.now() - timedelta(days=365 * years)
        
        # Extract all <entry> blocks
        entries = re.findall(r'<entry>(.*?)</entry>', xml_content, re.DOTALL)
        
        for entry in entries:
            try:
                # Extract filing date
                date_match = re.search(r'<filing-date>([\d-]+)</filing-date>', entry)
                if not date_match:
                    continue
                
                filing_date_str = date_match.group(1)
                filing_date = datetime.strptime(filing_date_str, '%Y-%m-%d')
                
                # Check if within date range
                if filing_date < cutoff_date:
                    continue
                
                # Extract accession number
                acc_match = re.search(r'<accession-nunber>([\d-]+)</accession-nunber>', entry)
                if not acc_match:
                    # Try alternate format
                    acc_match = re.search(r'accession[_-]?number[=:]([0-9-]+)', entry, re.IGNORECASE)
                
                if not acc_match:
                    continue
                
                accession = acc_match.group(1)
                
                # Extract filing URL if available
                url_match = re.search(r'<filing-href>(.*?)</filing-href>', entry)
                filing_url = url_match.group(1) if url_match else None
                
                filings.append({
                    'date': filing_date_str,
                    'accession': accession,
                    'url': filing_url
                })
                
            except Exception as e:
                continue
        
        # Sort by date (most recent first)
        filings.sort(key=lambda x: x['date'], reverse=True)
        
        return filings
    
    def _download_filing(self, filing: Dict, filing_type: str) -> Dict:
        """Download the actual filing document"""
        
        accession = filing['accession']
        date = filing['date']
        
        # Try the filing URL from the feed first
        if filing.get('url'):
            doc_url = filing['url']
        else:
            # Construct URL manually
            # Format: /Archives/edgar/data/CIK/ACCESSION-NO-DASH/ACCESSION-NO-DASH-index.html
            cik_no_pad = str(int(self.cik))  # Remove leading zeros
            accession_no_dash = accession.replace('-', '')
            doc_url = f"{self.BASE_URL}/Archives/edgar/data/{cik_no_pad}/{accession_no_dash}/{accession}-index.html"
        
        # Create cache directory
        cache_dir = f"data/cache/{self.ticker}"
        os.makedirs(cache_dir, exist_ok=True)
        
        # Generate safe filename
        safe_type = filing_type.replace(' ', '_').replace('/', '-')
        filename = f"{self.ticker}_{safe_type}_{date}.html"
        filepath = os.path.join(cache_dir, filename)
        
        print(f"      📥 Downloading {date} {filing_type}...")
        
        try:
            response = requests.get(doc_url, headers=self.headers, timeout=60)
            response.raise_for_status()
            
            # Save to file
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"      ✅ Saved: {filename} ({file_size/1024:.1f} KB)")
            
            return {
                'date': date,
                'url': doc_url,
                'path': filepath,
                'size': file_size,
                'accession': accession
            }
            
        except Exception as e:
            print(f"      ❌ Download failed: {str(e)}")
            # Try alternate URL format
            return self._try_alternate_url(filing, filing_type, filepath)
    
    def _try_alternate_url(self, filing: Dict, filing_type: str, filepath: str) -> Dict:
        """Try alternate URL format if first attempt fails"""
        
        try:
            # Try the document viewer URL
            doc_url = f"{self.BASE_URL}/cgi-bin/viewer?action=view&cik={self.cik}&accession_number={filing['accession']}&xbrl_type=v"
            
            response = requests.get(doc_url, headers=self.headers, timeout=60)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"      ✅ Saved (alternate URL): {filepath.split('/')[-1]} ({file_size/1024:.1f} KB)")
            
            return {
                'date': filing['date'],
                'url': doc_url,
                'path': filepath,
                'size': file_size,
                'accession': filing['accession']
            }
        except:
            return None
    
    def get_latest_filing(self, filing_type: str) -> str:
        """Get path to most recent filing"""
        filings = self.fetch_filings([filing_type], years=1)
        if filings.get(filing_type) and len(filings[filing_type]) > 0:
            return filings[filing_type][0]['path']
        return None


# Test
if __name__ == "__main__":
    print("🧪 Testing SEC Fetcher\n")
    
    fetcher = SECFetcher('AAPL')
    filings = fetcher.fetch_filings(['10-K'], years=1)
    
    print("\n" + "="*60)
    print("RESULTS:")
    print("="*60)
    
    for filing_type, files in filings.items():
        print(f"\n{filing_type}: {len(files)} filing(s)")
        for f in files:
            print(f"  📄 {f['date']}: {f['path']}")
            print(f"     Size: {f['size']/1024:.1f} KB")
            print(f"     URL: {f['url']}")