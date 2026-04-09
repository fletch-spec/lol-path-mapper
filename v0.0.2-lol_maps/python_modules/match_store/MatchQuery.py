from typing import List
import MatchStore
from _classes import Optional, Role, Dict, Match

class MatchQuery:
    def __init__(self, store: MatchStore):
        self.store = store
    
    def by_champion(self, champion_id: int, role: Optional[Role] = None) -> List[Match]:
        """Find all matches with champion + optional role"""
        pass
    
    def by_player(self, puuid: str, limit: int = 20) -> List[Match]:
        """Recent matches for player"""
        pass
    
    def winrate_by_champion(self, puuid: str) -> Dict[int, float]:
        """WR% grouped by champion"""
        pass
    
    def close_games(self, max_gold_diff: int = 5000) -> List[Match]:
        """Matches decided by < X gold"""
        pass
    
    def high_action(self, min_kills: int = 40) -> List[Match]:
        """20+ min games with 40+ total kills"""
        pass