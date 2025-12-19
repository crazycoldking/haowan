#!/usr/bin/env python3
"""
Main Orchestration Script
Coordinates data collection, ranking, and storage
"""

import os
import json
import sys
from datetime import datetime
from typing import List, Dict

from collector import GitHubCollector
from ranker import RepositoryRanker
from storage import DataStorage


class TrendingProjectsOrchestrator:
    """Main orchestrator for the trending projects system"""
    
    def __init__(self, config_path: str = 'config.json'):
        """
        Initialize orchestrator with configuration
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.collector = GitHubCollector()
        self.ranker = RepositoryRanker(self.config['ranking'])
        self.storage = DataStorage()
    
    def _load_config(self, config_path: str) -> Dict:
        """
        Load configuration from file
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Configuration dictionary
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def run_daily_job(self) -> bool:
        """
        Execute the daily data collection and ranking job
        
        Returns:
            True if successful, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"🚀 Starting Daily GitHub Trending Projects Job")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Check rate limit
        rate_limit = self.collector.check_rate_limit()
        print(f"📊 GitHub API Rate Limit:")
        print(f"   Core: {rate_limit.get('core_remaining', 0)}/{rate_limit.get('core_limit', 0)}")
        print(f"   Search: {rate_limit.get('search_remaining', 0)}/{rate_limit.get('search_limit', 0)}")
        print()
        
        if rate_limit.get('search_remaining', 0) < 5:
            print("⚠️  Warning: Low search API rate limit remaining")
        
        # Collect repositories
        print("📦 Collecting repositories...")
        all_repositories = []
        
        github_config = self.config['github']
        languages = github_config['languages']
        
        for language in languages:
            print(f"\n🔍 Searching for {language} repositories...")
            repos = self.collector.search_repositories(
                created_days_ago=github_config['search_days'],
                min_stars=github_config['min_stars'],
                language=language,
                max_results=github_config['max_results_per_language']
            )
            all_repositories.extend(repos)
        
        # Remove duplicates (a repo might appear in multiple language searches)
        unique_repos = self._deduplicate_repositories(all_repositories)
        print(f"\n✓ Collected {len(unique_repos)} unique repositories")
        
        if not unique_repos:
            print("✗ No repositories found. Exiting.")
            return False
        
        # Rank repositories
        print(f"\n📊 Ranking repositories...")
        ranked_repos = self.ranker.rank_repositories(
            unique_repos,
            trending_topics=github_config.get('topics', [])
        )
        
        # Get top N
        max_projects = self.config['output']['max_daily_projects']
        top_repos = self.ranker.get_top_n(ranked_repos, max_projects)
        print(f"✓ Selected top {len(top_repos)} repositories")
        
        # Save data
        print(f"\n💾 Saving data...")
        date = datetime.now().strftime('%Y-%m-%d')
        self.storage.save_daily_data(top_repos, date)
        self.storage.save_latest(top_repos)
        
        # Update history
        summary = self._generate_summary(top_repos, date)
        self.storage.update_history(date, summary)
        
        # Cleanup old data
        retention_days = self.config['output']['history_retention_days']
        deleted = self.storage.cleanup_old_data(retention_days)
        if deleted > 0:
            print(f"🗑️  Cleaned up {deleted} old data files")
        
        # Print summary
        self._print_summary(top_repos)
        
        print(f"\n{'='*60}")
        print(f"✅ Daily job completed successfully!")
        print(f"{'='*60}\n")
        
        return True
    
    def _deduplicate_repositories(self, repositories: List[Dict]) -> List[Dict]:
        """
        Remove duplicate repositories based on ID
        
        Args:
            repositories: List of repositories
            
        Returns:
            List of unique repositories
        """
        seen_ids = set()
        unique = []
        
        for repo in repositories:
            if repo['id'] not in seen_ids:
                seen_ids.add(repo['id'])
                unique.append(repo)
        
        return unique
    
    def _generate_summary(self, repositories: List[Dict], date: str) -> Dict:
        """
        Generate daily summary statistics
        
        Args:
            repositories: List of repositories
            date: Date string
            
        Returns:
            Summary dictionary
        """
        # Language distribution
        lang_dist = self.ranker.get_language_distribution(repositories)
        top_language = max(lang_dist.items(), key=lambda x: x[1])[0] if lang_dist else 'Unknown'
        
        # Top repository
        top_repo = repositories[0] if repositories else None
        
        summary = {
            'date': date,
            'total_count': len(repositories),
            'top_language': top_language,
            'language_distribution': lang_dist,
            'top_repo': {
                'name': top_repo['full_name'],
                'stars': top_repo['stars'],
                'score': top_repo['score']
            } if top_repo else None,
            'average_stars': round(sum(r['stars'] for r in repositories) / len(repositories), 2),
            'total_stars': sum(r['stars'] for r in repositories)
        }
        
        return summary
    
    def _print_summary(self, repositories: List[Dict]) -> None:
        """
        Print summary of results
        
        Args:
            repositories: List of ranked repositories
        """
        print(f"\n📈 Top 10 Trending Projects:")
        print(f"{'Rank':<6} {'Repository':<40} {'Stars':<8} {'Growth':<12} {'Score':<8}")
        print(f"{'-'*80}")
        
        for repo in repositories[:10]:
            rank = repo['rank']
            name = repo['full_name'][:38]
            stars = repo['stars']
            growth = f"{repo['stars_per_day']}/day"
            score = repo['score']
            
            print(f"{rank:<6} {name:<40} {stars:<8} {growth:<12} {score:<8}")
        
        print()
        
        # Language distribution
        lang_dist = self.ranker.get_language_distribution(repositories)
        print(f"🔤 Language Distribution (Top 5):")
        for i, (lang, count) in enumerate(list(lang_dist.items())[:5], 1):
            print(f"   {i}. {lang}: {count} repositories")


def main():
    """Main entry point"""
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(script_dir))
    
    try:
        orchestrator = TrendingProjectsOrchestrator()
        success = orchestrator.run_daily_job()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
