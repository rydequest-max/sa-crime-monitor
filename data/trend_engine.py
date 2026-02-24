"""
Trend Engine for SA Crime Monitor
===================================
Computes:
- Weekly / Monthly / Quarterly Top 10 leaderboards
- Position movement (up/down/new)
- National trend summaries
- Per-province breakdowns
- YoY comparisons
"""

from typing import List, Dict


class TrendEngine:
    
    def __init__(self, stations: List[Dict]):
        self.stations = stations
    
    def leaderboard(self, period: str = 'weekly', category: str = 'total') -> List[Dict]:
        """
        Generate Top 10 leaderboard with position movement.
        
        period: 'weekly', 'monthly', 'quarterly'
        category: 'total', 'murder', 'robbery', 'kidnap', 'carjack', 'assault', 'sexual', 'drugs'
        """
        # Multiplier to simulate period scaling from quarterly data
        mult = {'weekly': 0.08, 'monthly': 0.33, 'quarterly': 1.0}.get(period, 1.0)
        
        entries = []
        for s in self.stations:
            if category == 'total':
                cur = sum(s['c'].values())
                prev = sum(s['prev'].values())
            else:
                cur = s['c'].get(category, 0)
                prev = s['prev'].get(category, 0)
            
            cur_scaled = round(cur * mult)
            prev_scaled = round(prev * mult)
            diff = cur_scaled - prev_scaled
            
            if cur_scaled == 0:
                continue
            
            # Determine movement direction and magnitude
            if diff > 0:
                move_dir = 'up'
                move_val = diff
            elif diff < 0:
                move_dir = 'dn'
                move_val = abs(diff)
            else:
                move_dir = 'eq'
                move_val = 0
            
            # Calculate position change (simulate previous ranking)
            entries.append({
                'name': s['n'],
                'province': s['p'],
                'area': s['a'],
                'type': s.get('t', ''),
                'severity': s['s'],
                'current_value': cur_scaled,
                'previous_value': prev_scaled,
                'change': diff,
                'change_dir': move_dir,
                'change_abs': move_val,
                'pct_change': round((diff / prev_scaled * 100), 1) if prev_scaled > 0 else 0,
                'lat': s['lat'],
                'lng': s['lng'],
            })
        
        # Sort by current value descending
        entries.sort(key=lambda x: x['current_value'], reverse=True)
        
        # Now compute position changes
        # Sort previous values to get previous ranking
        prev_ranking = sorted(
            [e for e in entries],
            key=lambda x: x['previous_value'],
            reverse=True
        )
        prev_positions = {e['name']: i + 1 for i, e in enumerate(prev_ranking)}
        
        # Add position info
        top10 = entries[:10]
        for i, entry in enumerate(top10):
            cur_pos = i + 1
            prev_pos = prev_positions.get(entry['name'], 99)
            pos_change = prev_pos - cur_pos  # Positive = moved up
            
            entry['position'] = cur_pos
            entry['prev_position'] = prev_pos
            entry['pos_change'] = pos_change
            entry['pos_dir'] = 'up' if pos_change > 0 else ('dn' if pos_change < 0 else 'eq')
        
        return top10
    
    def national_trends(self) -> Dict:
        """Compute national-level trend summary"""
        crime_types = ['murder', 'robbery', 'assault', 'sexual', 'property', 'carjack', 'kidnap', 'drugs']
        
        trends = {}
        for ct in crime_types:
            cur_total = sum(s['c'].get(ct, 0) for s in self.stations)
            prev_total = sum(s['prev'].get(ct, 0) for s in self.stations)
            diff = cur_total - prev_total
            pct = round((diff / prev_total * 100), 1) if prev_total > 0 else 0
            
            trends[ct] = {
                'current': cur_total,
                'previous': prev_total,
                'change': diff,
                'pct_change': pct,
                'direction': 'up' if pct > 2 else ('dn' if pct < -2 else 'stable'),
                'per_day': round(cur_total / 90, 1),  # ~90 days per quarter
            }
        
        # Overall
        total_cur = sum(sum(s['c'].values()) for s in self.stations)
        total_prev = sum(sum(s['prev'].values()) for s in self.stations)
        total_diff = total_cur - total_prev
        total_pct = round((total_diff / total_prev * 100), 1) if total_prev > 0 else 0
        
        # Province breakdown
        provinces = {}
        for prov in ['WC', 'GP', 'KZN', 'EC', 'MP', 'NW', 'FS', 'LP', 'NC']:
            prov_cur = sum(sum(s['c'].values()) for s in self.stations if s['p'] == prov)
            prov_prev = sum(sum(s['prev'].values()) for s in self.stations if s['p'] == prov)
            prov_pct = round(((prov_cur - prov_prev) / prov_prev * 100), 1) if prov_prev > 0 else 0
            
            provinces[prov] = {
                'current': prov_cur,
                'previous': prov_prev,
                'pct_change': prov_pct,
                'direction': 'up' if prov_pct > 2 else ('dn' if prov_pct < -2 else 'stable'),
                'stations': sum(1 for s in self.stations if s['p'] == prov),
            }
        
        # Worst improving / deteriorating
        station_changes = []
        for s in self.stations:
            cur = sum(s['c'].values())
            prev = sum(s['prev'].values())
            pct = round(((cur - prev) / prev * 100), 1) if prev > 0 else 0
            station_changes.append({'name': s['n'], 'province': s['p'], 'pct': pct, 'current': cur})
        
        station_changes.sort(key=lambda x: x['pct'], reverse=True)
        
        return {
            'overall': {
                'current': total_cur,
                'previous': total_prev,
                'change': total_diff,
                'pct_change': total_pct,
                'direction': 'up' if total_pct > 0 else 'dn',
            },
            'by_crime': trends,
            'by_province': provinces,
            'biggest_increases': station_changes[:5],
            'biggest_decreases': station_changes[-5:][::-1],
            'data_period': 'Q3-Q4 2024/2025 vs Q3-Q4 2023/2024',
        }
