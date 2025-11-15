from typing import Dict, List, Any, Tuple
import re
from datetime import datetime
from agent.utils import AgentUtils, DataValidator

class ValidationChecker:
    """Comprehensive validation system for AI Agent"""
    
    @staticmethod
    def validate_volunteer_registration(data: Dict) -> Tuple[bool, List[str]]:
        """Validate volunteer registration data"""
        errors = DataValidator.validate_volunteer_data(data)
        
        # Additional validations
        if data.get('max_hours_per_week', 0) > 168:
            errors.append("Maximum hours per week cannot exceed 168")
        
        if not data.get('interests') or len(data['interests']) == 0:
            errors.append("At least one interest area is required")
        
        if data.get('experience_level') not in ['beginner', 'intermediate', 'expert']:
            errors.append("Experience level must be beginner, intermediate, or expert")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_opportunity_creation(data: Dict) -> Tuple[bool, List[str]]:
        """Validate opportunity creation data"""
        errors = DataValidator.validate_opportunity_data(data)
        
        # Additional validations
        timeframe = data.get('timeframe', {})
        if not timeframe.get('start') or not timeframe.get('end'):
            errors.append("Timeframe must include start and end dates")
        else:
            try:
                start = datetime.fromisoformat(timeframe['start'])
                end = datetime.fromisoformat(timeframe['end'])
                if end <= start:
                    errors.append("End date must be after start date")
            except ValueError:
                errors.append("Invalid date format in timeframe")
        
        urgency = data.get('urgency')
        if urgency not in ['low', 'medium', 'high', 'critical']:
            errors.append("Urgency must be low, medium, high, or critical")
        
        impact_area = data.get('impact_area')
        valid_areas = ['education', 'healthcare', 'environment', 'poverty', 'equality', 'disaster_relief']
        if impact_area not in valid_areas:
            errors.append(f"Impact area must be one of: {', '.join(valid_areas)}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_crisis_alert(data: Dict) -> Tuple[bool, List[str]]:
        """Validate crisis alert data"""
        errors = []
        
        if not data.get('type'):
            errors.append("Crisis type is required")
        
        if not data.get('location'):
            errors.append("Crisis location is required")
        
        if not data.get('severity'):
            errors.append("Crisis severity is required")
        
        people_affected = data.get('people_affected', 0)
        if people_affected < 0:
            errors.append("People affected cannot be negative")
        
        resources = data.get('resources_needed', [])
        if not resources:
            errors.append("At least one resource type is required")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_match_parameters(volunteer: Dict, opportunity: Dict) -> Tuple[bool, List[str]]:
        """Validate parameters for matching algorithm"""
        errors = []
        
        if not volunteer.get('skills'):
            errors.append("Volunteer must have skills")
        
        if not opportunity.get('required_skills'):
            errors.append("Opportunity must have required skills")
        
        if not volunteer.get('location'):
            errors.append("Volunteer location is required")
        
        if not opportunity.get('location'):
            errors.append("Opportunity location is required")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def sanitize_input_data(data: Dict) -> Dict:
        """Sanitize input data to prevent injection attacks"""
        sanitized = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # Remove potentially dangerous characters
                sanitized[key] = re.sub(r'[<>{}]', '', value).strip()
            elif isinstance(value, list):
                sanitized[key] = [re.sub(r'[<>{}]', '', str(item)).strip() if isinstance(item, str) else item 
                                for item in value]
            else:
                sanitized[key] = value
        
        return sanitized
    
    @staticmethod
    def validate_system_health() -> Tuple[bool, Dict]:
        """Validate overall system health"""
        health_checks = {
            "database_connection": True,  # Would check actual DB connection
            "api_endpoints": True,        # Would check external APIs
            "memory_usage": True,         # Would check system resources
            "agent_communication": True   # Would check inter-agent comms
        }
        
        all_healthy = all(health_checks.values())
        return all_healthy, health_checks

class SecurityValidator:
    """Security-focused validations"""
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Validate API key format"""
        if not api_key or len(api_key) < 20:
            return False
        
        # Check for basic pattern (would be more complex in production)
        pattern = r'^[A-Za-z0-9_-]{20,}$'
        return bool(re.match(pattern, api_key))
    
    @staticmethod
    def validate_rate_limit(identifier: str, max_requests: int = 100) -> bool:
        """Simple rate limiting validation"""
        # In production, would use Redis or similar for distributed rate limiting
        return True  # Mock implementation
    
    @staticmethod
    def sanitize_sql_query(query: str) -> str:
        """Basic SQL injection prevention"""
        dangerous_patterns = [
            r';.*--', r'DROP ', r'DELETE ', r'UPDATE ', r'INSERT ',
            r'UNION ', r'SELECT.*FROM', r'xp_', r'EXEC '
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                raise ValueError("Potentially dangerous SQL pattern detected")
        
        return query
