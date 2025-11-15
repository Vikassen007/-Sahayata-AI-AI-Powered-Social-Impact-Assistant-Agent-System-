import os
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum

@dataclass
class AgentConfig:
    """Configuration for AI Agent system"""
    # Matching weights
    MATCHING_WEIGHTS = {
        "skills": 0.4,
        "location": 0.2,
        "interests": 0.15,
        "urgency": 0.1,
        "experience": 0.1,
        "availability": 0.05
    }
    
    # Impact calculation
    IMPACT_MULTIPLIERS = {
        "disaster_relief": 2.0,
        "healthcare": 1.5,
        "education": 1.3,
        "poverty": 1.4,
        "environment": 1.2,
        "equality": 1.3
    }
    
    # System settings
    MAX_RECOMMENDATIONS = 5
    MIN_MATCH_SCORE = 0.3
    CRISIS_RESPONSE_RADIUS_KM = 50
    
    # API settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

class ImpactArea(Enum):
    EDUCATION = "education"
    HEALTHCARE = "healthcare"
    ENVIRONMENT = "environment"
    POVERTY = "poverty"
    EQUALITY = "equality"
    DISASTER_RELIEF = "disaster_relief"

class UrgencyLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

# Database configuration
DATABASE_CONFIG = {
    "url": os.getenv("DATABASE_URL", "sqlite:///agent_good.db"),
    "echo": False
}
