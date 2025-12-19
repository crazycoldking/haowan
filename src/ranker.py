#!/usr/bin/env python3
"""
Repository Ranking System
Calculates scores and ranks repositories based on multiple factors
"""

import math
from typing import List, Dict
from datetime import datetime


class RepositoryRanker:
    """Ranks repositories based on configurable scoring algorithm"""
    
    def __init__(self, config: Dict):
        """
        Initialize ranker with configuration
        
        Args:
            config: Configuration dictionary with ranking weights
        """
        self.star_weight = config.get('star_weight', 0.4)
        self.growth_rate_weight = config.get('growth_rate_weight', 0.3)
        self.freshness_weight = config.get('freshness_weight', 0.2)
        self.topic_relevance_weight = config.get('topic_relevance_weight', 0.1)
    
    def calculate_score(self, repo: Dict, trending_topics: List[str] = None) -> float:
        """
        Calculate overall score for a repository
        
        Args:
            repo: Repository data dictionary
            trending_topics: List of trending topics for bonus scoring
            
        Returns:
            Overall score (0-100)
        """
        trending_topics = trending_topics or []
        
        # 1. Star score (normalized logarithmically)
        star_score = self._normalize_star_score(repo['stars'])
        
        # 2. Growth rate score
        growth_score = self._normalize_growth_score(repo['stars_per_day'])
        
        # 3. Freshness score (newer is better)
        freshness_score = self._calculate_freshness_score(repo['days_since_creation'])
        
        # 4. Topic relevance score
        topic_score = self._calculate_topic_relevance(repo['topics'], trending_topics)
        
        # Calculate weighted total
        total_score = (
            star_score * self.star_weight +
            growth_score * self.growth_rate_weight +
            freshness_score * self.freshness_weight +
            topic_score * self.topic_relevance_weight
        ) * 100
        
        return round(total_score, 2)
    
    def _normalize_star_score(self, stars: int) -> float:
        """
        Normalize star count using logarithmic scale
        
        Args:
            stars: Number of stars
            
        Returns:
            Normalized score (0-1)
        """
        if stars <= 0:
            return 0.0
        
        # Use log scale: 10 stars = 0.1, 100 = 0.5, 1000 = 0.75, 10000 = 0.9
        log_stars = math.log10(stars)
        normalized = min(log_stars / 4.5, 1.0)  # Cap at 10000+ stars
        
        return normalized
    
    def _normalize_growth_score(self, stars_per_day: float) -> float:
        """
        Normalize growth rate (stars per day)
        
        Args:
            stars_per_day: Average stars gained per day
            
        Returns:
            Normalized score (0-1)
        """
        if stars_per_day <= 0:
            return 0.0
        
        # Use log scale for growth rate
        log_growth = math.log10(stars_per_day + 1)
        normalized = min(log_growth / 3.0, 1.0)  # Cap at 1000+ stars/day
        
        return normalized
    
    def _calculate_freshness_score(self, days_since_creation: int) -> float:
        """
        Calculate freshness score (newer repos score higher)
        
        Args:
            days_since_creation: Days since repository was created
            
        Returns:
            Freshness score (0-1)
        """
        # Exponential decay: 0 days = 1.0, 7 days = 0.5, 30 days = ~0.1
        decay_rate = 0.1
        freshness = math.exp(-decay_rate * days_since_creation)
        
        return freshness
    
    def _calculate_topic_relevance(self, repo_topics: List[str], 
                                   trending_topics: List[str]) -> float:
        """
        Calculate topic relevance score
        
        Args:
            repo_topics: Topics associated with the repository
            trending_topics: List of currently trending topics
            
        Returns:
            Topic relevance score (0-1)
        """
        if not trending_topics or not repo_topics:
            return 0.5  # Neutral score if no topics
        
        # Calculate intersection
        matches = len(set(repo_topics) & set(trending_topics))
        
        if matches == 0:
            return 0.3  # Small penalty for no matching topics
        
        # Score based on number of matches
        relevance = min(matches / len(trending_topics), 1.0)
        
        return 0.5 + (relevance * 0.5)  # Range: 0.5-1.0
    
    def rank_repositories(self, repositories: List[Dict], 
                         trending_topics: List[str] = None) -> List[Dict]:
        """
        Rank a list of repositories by calculated score
        
        Args:
            repositories: List of repository dictionaries
            trending_topics: List of trending topics for bonus scoring
            
        Returns:
            Sorted list of repositories with scores
        """
        # Calculate scores for all repositories
        for repo in repositories:
            repo['score'] = self.calculate_score(repo, trending_topics)
            repo['rank'] = 0  # Will be assigned after sorting
        
        # Sort by score (descending)
        ranked = sorted(repositories, key=lambda x: x['score'], reverse=True)
        
        # Assign ranks
        for i, repo in enumerate(ranked, 1):
            repo['rank'] = i
        
        return ranked
    
    def get_top_n(self, repositories: List[Dict], n: int = 100) -> List[Dict]:
        """
        Get top N repositories
        
        Args:
            repositories: List of ranked repositories
            n: Number of top repositories to return
            
        Returns:
            Top N repositories
        """
        return repositories[:n]
    
    def filter_by_language(self, repositories: List[Dict], 
                          language: str) -> List[Dict]:
        """
        Filter repositories by programming language
        
        Args:
            repositories: List of repositories
            language: Programming language to filter by
            
        Returns:
            Filtered list of repositories
        """
        if not language or language.lower() == 'all':
            return repositories
        
        return [repo for repo in repositories 
                if repo.get('language', '').lower() == language.lower()]
    
    def get_language_distribution(self, repositories: List[Dict]) -> Dict[str, int]:
        """
        Get distribution of programming languages
        
        Args:
            repositories: List of repositories
            
        Returns:
            Dictionary with language counts
        """
        distribution = {}
        for repo in repositories:
            lang = repo.get('language', 'Unknown')
            distribution[lang] = distribution.get(lang, 0) + 1
        
        return dict(sorted(distribution.items(), 
                          key=lambda x: x[1], 
                          reverse=True))


def main():
    """Main function for testing the ranker"""
    # Sample data
    sample_repos = [
        {
            'full_name': 'user/repo1',
            'stars': 1000,
            'stars_per_day': 50,
            'days_since_creation': 5,
            'topics': ['ai', 'machine-learning']
        },
        {
            'full_name': 'user/repo2',
            'stars': 500,
            'stars_per_day': 100,
            'days_since_creation': 3,
            'topics': ['web-development']
        },
        {
            'full_name': 'user/repo3',
            'stars': 200,
            'stars_per_day': 20,
            'days_since_creation': 10,
            'topics': ['ai', 'devops']
        }
    ]
    
    config = {
        'star_weight': 0.4,
        'growth_rate_weight': 0.3,
        'freshness_weight': 0.2,
        'topic_relevance_weight': 0.1
    }
    
    ranker = RepositoryRanker(config)
    ranked = ranker.rank_repositories(
        sample_repos, 
        trending_topics=['ai', 'machine-learning']
    )
    
    print("Ranked repositories:")
    for repo in ranked:
        print(f"{repo['rank']}. {repo['full_name']} - Score: {repo['score']}")


if __name__ == '__main__':
    main()
