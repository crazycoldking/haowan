#!/usr/bin/env python3
"""
Data Storage Module
Handles persistence of repository data and historical records
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class DataStorage:
    """Manages storage and retrieval of repository data"""
    
    def __init__(self, data_dir: str = 'data'):
        """
        Initialize storage with data directory
        
        Args:
            data_dir: Directory path for storing data files
        """
        self.data_dir = data_dir
        self.daily_dir = os.path.join(data_dir, 'daily')
        self.summary_file = os.path.join(data_dir, 'latest.json')
        self.history_file = os.path.join(data_dir, 'history.json')
        
        # Create directories if they don't exist
        os.makedirs(self.daily_dir, exist_ok=True)
    
    def save_daily_data(self, repositories: List[Dict], date: str = None) -> str:
        """
        Save daily repository data
        
        Args:
            repositories: List of ranked repositories
            date: Date string (YYYY-MM-DD), defaults to today
            
        Returns:
            Path to saved file
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        file_path = os.path.join(self.daily_dir, f'{date}.json')
        
        data = {
            'date': date,
            'generated_at': datetime.now().isoformat(),
            'total_count': len(repositories),
            'repositories': repositories
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved {len(repositories)} repositories to {file_path}")
        return file_path
    
    def load_daily_data(self, date: str) -> Optional[Dict]:
        """
        Load daily repository data
        
        Args:
            date: Date string (YYYY-MM-DD)
            
        Returns:
            Daily data dictionary or None if not found
        """
        file_path = os.path.join(self.daily_dir, f'{date}.json')
        
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_latest(self, repositories: List[Dict]) -> None:
        """
        Save latest repository data for quick access
        
        Args:
            repositories: List of ranked repositories
        """
        data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'generated_at': datetime.now().isoformat(),
            'total_count': len(repositories),
            'repositories': repositories
        }
        
        with open(self.summary_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Updated latest.json with {len(repositories)} repositories")
    
    def load_latest(self) -> Optional[Dict]:
        """
        Load latest repository data
        
        Returns:
            Latest data dictionary or None if not found
        """
        if not os.path.exists(self.summary_file):
            return None
        
        with open(self.summary_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def update_history(self, date: str, summary: Dict) -> None:
        """
        Update history index with daily summary
        
        Args:
            date: Date string (YYYY-MM-DD)
            summary: Summary information for the day
        """
        # Load existing history
        history = self.load_history() or {'dates': []}
        
        # Check if date already exists
        existing_dates = [entry['date'] for entry in history['dates']]
        
        if date in existing_dates:
            # Update existing entry
            for entry in history['dates']:
                if entry['date'] == date:
                    entry.update(summary)
                    break
        else:
            # Add new entry
            history['dates'].append(summary)
        
        # Sort by date (most recent first)
        history['dates'] = sorted(
            history['dates'], 
            key=lambda x: x['date'], 
            reverse=True
        )
        
        # Save history
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Updated history.json with date {date}")
    
    def load_history(self) -> Optional[Dict]:
        """
        Load history index
        
        Returns:
            History dictionary or None if not found
        """
        if not os.path.exists(self.history_file):
            return None
        
        with open(self.history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_available_dates(self) -> List[str]:
        """
        Get list of available dates with data
        
        Returns:
            List of date strings (YYYY-MM-DD)
        """
        if not os.path.exists(self.daily_dir):
            return []
        
        dates = []
        for filename in os.listdir(self.daily_dir):
            if filename.endswith('.json'):
                dates.append(filename.replace('.json', ''))
        
        return sorted(dates, reverse=True)
    
    def cleanup_old_data(self, retention_days: int = 30) -> int:
        """
        Remove data files older than retention period
        
        Args:
            retention_days: Number of days to retain data
            
        Returns:
            Number of files deleted
        """
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        deleted_count = 0
        
        for filename in os.listdir(self.daily_dir):
            if not filename.endswith('.json'):
                continue
            
            date_str = filename.replace('.json', '')
            try:
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                if file_date < cutoff_date:
                    file_path = os.path.join(self.daily_dir, filename)
                    os.remove(file_path)
                    deleted_count += 1
                    print(f"✓ Deleted old data file: {filename}")
            except ValueError:
                continue
        
        return deleted_count
    
    def get_statistics(self) -> Dict:
        """
        Get storage statistics
        
        Returns:
            Dictionary with storage statistics
        """
        available_dates = self.get_available_dates()
        
        stats = {
            'total_daily_files': len(available_dates),
            'oldest_date': available_dates[-1] if available_dates else None,
            'newest_date': available_dates[0] if available_dates else None,
            'has_latest': os.path.exists(self.summary_file),
            'has_history': os.path.exists(self.history_file)
        }
        
        return stats


def main():
    """Main function for testing storage"""
    storage = DataStorage()
    
    # Sample data
    sample_repos = [
        {
            'full_name': 'user/repo1',
            'stars': 1000,
            'score': 85.5,
            'rank': 1
        },
        {
            'full_name': 'user/repo2',
            'stars': 500,
            'score': 75.2,
            'rank': 2
        }
    ]
    
    # Save daily data
    date = datetime.now().strftime('%Y-%m-%d')
    storage.save_daily_data(sample_repos, date)
    storage.save_latest(sample_repos)
    
    # Update history
    summary = {
        'date': date,
        'total_count': len(sample_repos),
        'top_language': 'Python',
        'top_repo': sample_repos[0]['full_name']
    }
    storage.update_history(date, summary)
    
    # Get statistics
    stats = storage.get_statistics()
    print(f"\nStorage statistics: {stats}")


if __name__ == '__main__':
    main()
