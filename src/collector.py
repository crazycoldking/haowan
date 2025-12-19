#!/usr/bin/env python3
"""
GitHub Trending Projects Collector
Fetches trending repositories from GitHub API
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests


class GitHubCollector:
    """Collects trending repositories from GitHub API"""
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize collector with optional GitHub token
        
        Args:
            token: GitHub personal access token for higher rate limits
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
    
    def search_repositories(self, 
                          created_days_ago: int = 7,
                          min_stars: int = 10,
                          language: Optional[str] = None,
                          max_results: int = 100) -> List[Dict]:
        """
        Search for repositories created in the last N days
        
        Args:
            created_days_ago: Days to look back for repository creation
            min_stars: Minimum star count
            language: Programming language filter (optional)
            max_results: Maximum number of results to return
            
        Returns:
            List of repository dictionaries
        """
        since_date = (datetime.now() - timedelta(days=created_days_ago)).strftime('%Y-%m-%d')
        
        # Build query
        query_parts = [
            f'created:>{since_date}',
            f'stars:>={min_stars}'
        ]
        
        if language and language.lower() != 'all':
            query_parts.append(f'language:{language}')
        
        query = ' '.join(query_parts)
        
        # Search with sorting by stars
        url = f"{self.base_url}/search/repositories"
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': min(max_results, 100)
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Extract relevant information
            repositories = []
            for item in data.get('items', []):
                repo = self._extract_repo_info(item)
                repositories.append(repo)
            
            print(f"✓ Found {len(repositories)} repositories for language: {language or 'All'}")
            return repositories
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching repositories: {e}")
            return []
    
    def get_repository_details(self, owner: str, repo: str) -> Optional[Dict]:
        """
        Get detailed information about a specific repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Repository details dictionary or None
        """
        url = f"{self.base_url}/repos/{owner}/{repo}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return self._extract_repo_info(response.json())
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching repository {owner}/{repo}: {e}")
            return None
    
    def _extract_repo_info(self, api_data: Dict) -> Dict:
        """
        Extract relevant information from GitHub API response
        
        Args:
            api_data: Raw API response data
            
        Returns:
            Cleaned repository information
        """
        created_at = datetime.strptime(api_data['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        updated_at = datetime.strptime(api_data['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        days_since_creation = (datetime.now() - created_at).days or 1
        
        return {
            'id': api_data['id'],
            'name': api_data['name'],
            'full_name': api_data['full_name'],
            'owner': api_data['owner']['login'],
            'html_url': api_data['html_url'],
            'description': api_data.get('description', ''),
            'language': api_data.get('language', 'Unknown'),
            'stars': api_data['stargazers_count'],
            'forks': api_data['forks_count'],
            'watchers': api_data['watchers_count'],
            'open_issues': api_data['open_issues_count'],
            'topics': api_data.get('topics', []),
            'created_at': api_data['created_at'],
            'updated_at': api_data['updated_at'],
            'pushed_at': api_data.get('pushed_at', api_data['updated_at']),
            'homepage': api_data.get('homepage', ''),
            'license': api_data.get('license', {}).get('name', 'None'),
            'days_since_creation': days_since_creation,
            'stars_per_day': round(api_data['stargazers_count'] / days_since_creation, 2)
        }
    
    def check_rate_limit(self) -> Dict:
        """
        Check current GitHub API rate limit status
        
        Returns:
            Rate limit information
        """
        url = f"{self.base_url}/rate_limit"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            core = data['resources']['core']
            search = data['resources']['search']
            
            return {
                'core_remaining': core['remaining'],
                'core_limit': core['limit'],
                'search_remaining': search['remaining'],
                'search_limit': search['limit']
            }
        except requests.exceptions.RequestException as e:
            print(f"✗ Error checking rate limit: {e}")
            return {}


def main():
    """Main function for testing the collector"""
    collector = GitHubCollector()
    
    # Check rate limit
    rate_limit = collector.check_rate_limit()
    print(f"Rate Limit: {rate_limit}")
    
    # Search for Python repositories
    repos = collector.search_repositories(
        created_days_ago=7,
        min_stars=10,
        language='Python',
        max_results=10
    )
    
    print(f"\nTop 10 Python repositories:")
    for i, repo in enumerate(repos[:10], 1):
        print(f"{i}. {repo['full_name']} - ⭐ {repo['stars']} ({repo['stars_per_day']} stars/day)")


if __name__ == '__main__':
    main()
