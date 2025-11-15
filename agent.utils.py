import numpy as np
from typing import List, Dict, Any
from datetime import datetime, timedelta
import re

class AgentUtils:
    """Utility functions for AI agents"""
    
    @staticmethod
    def calculate_similarity(set1: set, set2: set) -> float:
        """Calculate Jaccard similarity between two sets"""
        if not set1 and not set2:
            return 0.0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
    
    @staticmethod
    def normalize_score(score: float, max_score: float = 1.0) -> float:
        """Normalize score to 0-1 range"""
        return max(0.0, min(score / max_score, 1.0))
    
    @staticmethod
    def calculate_urgency_multiplier(urgency_level: UrgencyLevel) -> float:
        """Calculate multiplier based on urgency level"""
        multipliers = {
            UrgencyLevel.LOW: 0.5,
            UrgencyLevel.MEDIUM: 1.0,
            UrgencyLevel.HIGH: 1.5,
            UrgencyLevel.CRITICAL: 2.0
        }
        return multipliers.get(urgency_level, 1.0)
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def format_duration(hours: float) -> str:
        """Format duration in human-readable format"""
        if hours < 1:
            return f"{int(hours * 60)} minutes"
        elif hours < 24:
            return f"{hours:.1f} hours"
        else:
            days = hours / 24
            return f"{days:.1f} days"
    
    @staticmethod
    def generate_id(prefix: str) -> str:
        """Generate unique ID with prefix"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = np.random.randint(1000, 9999)
        return f"{prefix}_{timestamp}_{random_suffix}"
    
    @staticmethod
    def calculate_impact_score(people_helped: int, hours_contributed: float, 
                             quality_rating: float = 0.5) -> float:
        """Calculate impact score based on multiple factors"""
        base_score = min(people_helped * 0.1, 0.4)
        time_score = min(hours_contributed * quality_rating * 0.05, 0.3)
        return base_score + time_score

class DataValidator:
    """Data validation utilities"""
    
    @staticmethod
    def validate_volunteer_data(data: Dict) -> List[str]:
        """Validate volunteer registration data"""
        errors = []
        
        if not data.get('name') or len(data['name'].strip()) < 2:
            errors.append("Name must be at least 2 characters long")
        
        if not data.get('skills') or not isinstance(data['skills'], list):
            errors.append("Skills must be a non-empty list")
        
        if not data.get('location'):
            errors.append("Location is required")
        
        if not data.get('email') or not AgentUtils.validate_email(data['email']):
            errors.append("Valid email is required")
        
        return errors
    
    @staticmethod
    def validate_opportunity_data(data: Dict) -> List[str]:
        """Validate opportunity creation data"""
        errors = []
        
        if not data.get('title') or len(data['title'].strip()) < 5:
            errors.append("Title must be at least 5 characters long")
        
        if not data.get('required_skills') or not isinstance(data['required_skills'], list):
            errors.append("Required skills must be a non-empty list")
        
        if not data.get('volunteers_needed') or data['volunteers_needed'] < 1:
            errors.append("At least 1 volunteer needed")
        
        return errors
