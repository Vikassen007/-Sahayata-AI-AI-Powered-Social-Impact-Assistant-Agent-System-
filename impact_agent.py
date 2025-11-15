from typing import Dict, List, Any
from datetime import datetime, timedelta
from agent import BaseAgent, Volunteer, Opportunity
from config import AgentConfig, ImpactArea, UrgencyLevel
from agent.utils import AgentUtils

class ImpactAgent(BaseAgent):
    """AI Agent for tracking and measuring social impact"""
    
    def __init__(self):
        super().__init__("ImpactAgent")
        self.completed_projects = []
        self.impact_multipliers = AgentConfig.IMPACT_MULTIPLIERS
    
    async def record_completion(self, volunteer: Volunteer, opportunity: Opportunity, 
                              outcomes: Dict) -> Dict[str, Any]:
        """Record project completion and calculate impact"""
        impact_score = self._calculate_impact_score(opportunity, outcomes)
        
        completion_record = {
            'volunteer_id': volunteer.id,
            'volunteer_name': volunteer.name,
            'opportunity_id': opportunity.id,
            'opportunity_title': opportunity.title,
            'completion_date': datetime.now(),
            'hours_contributed': outcomes.get('hours_contributed', 0),
            'people_impacted': outcomes.get('people_impacted', 0),
            'quality_rating': outcomes.get('quality_rating', 0.5),
            'sustainability_score': outcomes.get('sustainability_score', 0.5),
            'impact_score': impact_score,
            'feedback': outcomes.get('feedback', {}),
            'calculated_at': datetime.now()
        }
        
        self.completed_projects.append(completion_record)
        self.logger.info(f"📊 Recorded impact for {volunteer.name}: {impact_score:.2f}")
        
        return completion_record
    
    def _calculate_impact_score(self, opportunity: Opportunity, outcomes: Dict) -> float:
        """Calculate comprehensive impact score"""
        base_score = 0.0
        
        # People impacted
        people_impacted = outcomes.get('people_impacted', 0)
        base_score += min(people_impacted * 0.1, 0.4)
        
        # Hours contributed with quality multiplier
        hours = outcomes.get('hours_contributed', 0)
        quality = outcomes.get('quality_rating', 0.5)
        base_score += (hours * quality * 0.05)
        
        # Area-specific multiplier
        area_multiplier = self.impact_multipliers.get(opportunity.impact_area, 1.0)
        
        # Urgency multiplier
        urgency_multiplier = AgentUtils.calculate_urgency_multiplier(opportunity.urgency)
        
        # Sustainability factor
        sustainability = outcomes.get('sustainability_score', 0.5)
        
        final_score = base_score * area_multiplier * urgency_multiplier * (1 + sustainability)
        return min(final_score, 1.0)
    
    def generate_report(self, timeframe_days: int = 30) -> Dict[str, Any]:
        """Generate comprehensive impact report"""
        cutoff_date = datetime.now() - timedelta(days=timeframe_days)
        recent_completions = [
            c for c in self.completed_projects 
            if c['completion_date'] >= cutoff_date
        ]
        
        if not recent_completions:
            return {
                "report_period": f"Last {timeframe_days} days",
                "message": "No completed projects in this period",
                "total_completions": 0,
                "total_impact_score": 0.0
            }
        
        total_hours = sum(c['hours_contributed'] for c in recent_completions)
        total_impact = sum(c['impact_score'] for c in recent_completions)
        total_people = sum(c['people_impacted'] for c in recent_completions)
        unique_volunteers = len(set(c['volunteer_id'] for c in recent_completions))
        
        return {
            "report_period": f"Last {timeframe_days} days",
            "total_completions": len(recent_completions),
            "total_volunteer_hours": total_hours,
            "total_people_impacted": total_people,
            "total_impact_score": round(total_impact, 2),
            "unique_volunteers
