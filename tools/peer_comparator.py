"""
Peer Company Comparator
Compare target company against industry peers
"""

from typing import Dict, List
from dataclasses import dataclass

@dataclass
class PeerComparison:
    """Comparison results"""
    target_ticker: str
    peer_group: List[str]
    roe_percentile: float
    roic_percentile: float
    margin_percentile: float
    roe_gap: float
    roic_gap: float
    margin_gap: float
    upside_to_peer_median: float
    implied_market_cap_at_peer_median: float


class PeerComparator:
    """Compare company against industry peers"""
    
    def __init__(self):
        # Hardcoded peer data for demo
        # In production: fetch from financial data API
        self.peer_database = {
            'technology': [
                {'ticker': 'AAPL', 'roe': 147.0, 'roic': 45.0, 'margin': 30.0},
                {'ticker': 'MSFT', 'roe': 38.0, 'roic': 28.0, 'margin': 42.0},
                {'ticker': 'GOOGL', 'roe': 26.0, 'roic': 22.0, 'margin': 27.0},
            ]
        }
    
    def compare_to_peers(self, ticker: str, target_metrics: Dict, industry: str = 'technology') -> PeerComparison:
        """Perform comprehensive peer comparison"""
        
        peers = self.peer_database.get(industry, self.peer_database['technology'])
        peer_tickers = [p['ticker'] for p in peers]
        
        target_roe = target_metrics.get('roe', 0)
        target_roic = target_metrics.get('roic', 0)
        target_margin = target_metrics.get('operating_margin', 0)
        
        peer_roes = [p['roe'] for p in peers]
        peer_roics = [p['roic'] for p in peers]
        peer_margins = [p['margin'] for p in peers]
        
        # Calculate medians
        import statistics
        roe_median = statistics.median(peer_roes) if peer_roes else 0
        roic_median = statistics.median(peer_roics) if peer_roics else 0
        margin_median = statistics.median(peer_margins) if peer_margins else 0
        
        # Calculate gaps
        roe_gap = target_roe - roe_median
        roic_gap = target_roic - roic_median
        margin_gap = target_margin - margin_median
        
        # Calculate implied market cap (simplified)
        current_mc = target_metrics.get('market_cap', 0)
        implied_mc = current_mc * 1.15  # Simplified 15% upside
        
        return PeerComparison(
            target_ticker=ticker,
            peer_group=peer_tickers,
            roe_percentile=self._calc_percentile(target_roe, peer_roes),
            roic_percentile=self._calc_percentile(target_roic, peer_roics),
            margin_percentile=self._calc_percentile(target_margin, peer_margins),
            roe_gap=roe_gap,
            roic_gap=roic_gap,
            margin_gap=margin_gap,
            upside_to_peer_median=15.0,  # Simplified
            implied_market_cap_at_peer_median=implied_mc
        )
    
    def _calc_percentile(self, value: float, peer_values: List[float]) -> float:
        """Calculate percentile rank"""
        if not peer_values:
            return 50.0
        below = sum(1 for v in peer_values if v < value)
        return (below / len(peer_values)) * 100


if __name__ == "__main__":
    comparator = PeerComparator()
    metrics = {'roe': 18.5, 'roic': 12.0, 'operating_margin': 22.0}
    result = comparator.compare_to_peers('TARGET', metrics)
    print(f"ROE Percentile: {result.roe_percentile:.0f}th")