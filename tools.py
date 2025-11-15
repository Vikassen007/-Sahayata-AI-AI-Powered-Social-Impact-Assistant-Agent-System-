from typing import Dict, List, Any, Optional
import aiohttp
import asyncio
from datetime import datetime
import json

class APIClient:
    """HTTP client for external API calls"""
    
    def __init__(self, base_url: str = ""):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get(self, endpoint: str, params: Dict = None) -> Dict:
        """Make GET request"""
        url = f"{self.base_url}/{endpoint}".strip("/")
        async with self.session.get(url, params=params) as response:
            return await response.json()
    
    async def post(self, endpoint: str, data: Dict) -> Dict:
        """Make POST request"""
        url = f"{self.base_url}/{endpoint}".strip("/")
        async with self.session.post(url, json=data) as response:
            return await response.json()

class LocationService:
    """Location-based services"""
    
    @staticmethod
    async def get_coordinates(location: str) -> Optional[Dict]:
        """Get coordinates for a location (mock implementation)"""
        # In production, integrate with Google Maps API or similar
        return {"lat": 40.7128, "lng": -74.0060, "location": location}
    
    @staticmethod
    def calculate_distance(loc1: str, loc2: str) -> float:
        """Calculate distance between locations (simplified)"""
        # Mock implementation - in production use geopy or similar
        if loc1.lower() == loc2.lower():
            return 0.0
        return 25.0  # Default distance

class NotificationService:
    """Notification and communication tools"""
    
    @staticmethod
    async def send_email(to: str, subject: str, body: str) -> bool:
        """Send email notification"""
        print(f"📧 Email to {to}: {subject}")
        return True
    
    @staticmethod
    async def send_sms(to: str, message: str) -> bool:
        """Send SMS notification"""
        print(f"📱 SMS to {to}: {message}")
        return True
    
    @staticmethod
    async def send_push_notification(device_id: str, title: str, message: str) -> bool:
        """Send push notification"""
        print(f"📲 Push to {device_id}: {title} - {message}")
        return True

class DataStorage:
    """Data storage and retrieval tools"""
    
    def __init__(self):
        self.volunteers = []
        self.opportunities = []
        self.matches = []
    
    async def save_volunteer(self, volunteer_data: Dict) -> str:
        """Save volunteer data"""
        volunteer_id = f"vol_{len(self.volunteers) + 1}"
        volunteer_data['id'] = volunteer_id
        volunteer_data['created_at'] = datetime.now().isoformat()
        self.volunteers.append(volunteer_data)
        return volunteer_id
    
    async def get_volunteer(self, volunteer_id: str) -> Optional[Dict]:
        """Get volunteer by ID"""
        return next((v for v in self.volunteers if v['id'] == volunteer_id), None)
    
    async def save_opportunity(self, opportunity_data: Dict) -> str:
        """Save opportunity data"""
        opportunity_id = f"opp_{len(self.opportunities) + 1}"
        opportunity_data['id'] = opportunity_id
        opportunity_data['created_at'] = datetime.now().isoformat()
        self.opportunities.append(opportunity_data)
        return opportunity_id
    
    async def get_opportunity(self, opportunity_id: str) -> Optional[Dict]:
        """Get opportunity by ID"""
        return next((o for o in self.opportunities if o['id'] == opportunity_id), None)
    
    async def save_match(self, match_data: Dict) -> str:
        """Save match data"""
        match_id = f"match_{len(self.matches) + 1}"
        match_data['id'] = match_id
        match_data['created_at'] = datetime.now().isoformat()
        self.matches.append(match_data)
        return match_id

class AnalyticsEngine:
    """Analytics and reporting tools"""
    
    @staticmethod
    def calculate_match_quality(volunteer_skills: List[str], required_skills: List[str]) -> float:
        """Calculate match quality score"""
        if not required_skills:
            return 0.5
        
        matched = set(volunteer_skills) & set(required_skills)
        return len(matched) / len(required_skills)
    
    @staticmethod
    def generate_impact_report(completions: List[Dict]) -> Dict:
        """Generate impact analytics report"""
        total_hours = sum(c.get('hours_contributed', 0) for c in completions)
        total_people = sum(c.get('people_impacted', 0) for c in completions)
        avg_impact = sum(c.get('impact_score', 0) for c in completions) / len(completions) if completions else 0
        
        return {
            "total_completions": len(completions),
            "total_volunteer_hours": total_hours,
            "total_people_impacted": total_people,
            "average_impact_score": avg_impact,
            "efficiency_rating": min(total_people / max(total_hours, 1), 10.0)
        }
    
    @staticmethod
    def predict_success_probability(volunteer: Dict, opportunity: Dict) -> float:
        """Predict probability of successful engagement"""
        base_score = 0.5
        
        # Skill match
        skill_match = AnalyticsEngine.calculate_match_quality(
            volunteer.get('skills', []), 
            opportunity.get('required_skills', [])
        )
        base_score += skill_match * 0.3
        
        # Location bonus
        if volunteer.get('location') == opportunity.get('location'):
            base_score += 0.1
        
        # Experience bonus
        if volunteer.get('experience_level') == 'expert':
            base_score += 0.1
        
        return min(base_score, 1.0)
