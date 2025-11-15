from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import asyncio
from config import ImpactArea, UrgencyLevel, AgentConfig

@dataclass
class Volunteer:
    id: str
    name: str
    skills: List[str]
    location: str
    availability: Dict[str, bool]
    interests: List[ImpactArea]
    experience_level: str
    languages: List[str]
    max_hours_per_week: int
    email: str
    phone: Optional[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class Opportunity:
    id: str
    title: str
    organization: str
    description: str
    required_skills: List[str]
    location: str
    impact_area: ImpactArea
    urgency: UrgencyLevel
    timeframe: Dict[str, datetime]
    volunteers_needed: int
    resources_required: Dict[str, int]
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class MatchResult:
    volunteer: Volunteer
    opportunity: Opportunity
    match_score: float
    reasoning: List[str]
    confidence: float

class BaseAgent:
    """Base class for all AI agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        import logging
        logging.basicConfig(level=logging.INFO)
        return logging.getLogger(self.name)
    
    async def process(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement process method")

class SocialGoodOrchestrator(BaseAgent):
    """Main orchestrator agent that coordinates all sub-agents"""
    
    def __init__(self):
        super().__init__("SocialGoodOrchestrator")
        self.volunteers: List[Volunteer] = []
        self.opportunities: List[Opportunity] = []
        self.completed_projects: List[Dict] = []
        
        # Initialize sub-agents
        from sub_agents.matching_agent import MatchingAgent
        from sub_agents.impact_agent import ImpactAgent
        from sub_agents.communication_agent import CommunicationAgent
        from sub_agents.crisis_agent import CrisisAgent
        from sub_agents.optimization_agent import OptimizationAgent
        
        self.matcher = MatchingAgent()
        self.impact_tracker = ImpactAgent()
        self.communication_agent = CommunicationAgent()
        self.crisis_detector = CrisisAgent()
        self.optimizer = OptimizationAgent()
        
        self.logger.info("🤖 Social Good Orchestrator initialized!")
    
    async def register_volunteer(self, volunteer_data: Dict) -> Volunteer:
        """Register a new volunteer and find immediate matches"""
        volunteer = Volunteer(**volunteer_data)
        self.volunteers.append(volunteer)
        
        # Find matches
        matches = await self.matcher.find_matches(volunteer, self.opportunities)
        
        # Send welcome package
        await self.communication_agent.send_welcome(volunteer, matches)
        
        self.logger.info(f"✅ Volunteer {volunteer.name} registered with {len(matches)} matches")
        return volunteer
    
    async def create_opportunity(self, opportunity_data: Dict) -> Opportunity:
        """Create a new opportunity and find suitable volunteers"""
        opportunity = Opportunity(**opportunity_data)
        self.opportunities.append(opportunity)
        
        # Find suitable volunteers
        suitable_volunteers = await self.matcher.find_volunteers(opportunity, self.volunteers)
        
        # Optimize resource allocation
        allocation = await self.optimizer.allocate_resources(opportunity, suitable_volunteers)
        
        self.logger.info(f"✅ Opportunity '{opportunity.title}' created with {len(suitable_volunteers)} suitable volunteers")
        return opportunity
    
    async def handle_crisis(self, crisis_data: Dict) -> Dict:
        """Handle crisis situations with rapid response"""
        crisis_ops = await self.crisis_detector.generate_response(crisis_data)
        
        for crisis_op in crisis_ops:
            await self.create_opportunity(crisis_op)
        
        mobilized = await self._mobilize_emergency_response(crisis_data)
        return {"mobilized": mobilized, "crisis_ops_created": len(crisis_ops)}
    
    async def _mobilize_emergency_response(self, crisis_data: Dict) -> int:
        """Mobilize volunteers for emergency response"""
        nearby_volunteers = [
            v for v in self.volunteers 
            if self._calculate_proximity(v.location, crisis_data['location']) < AgentConfig.CRISIS_RESPONSE_RADIUS_KM
        ]
        
        for volunteer in nearby_volunteers:
            await self.communication_agent.send_emergency_alert(volunteer, crisis_data)
        
        return len(nearby_volunteers)
    
    def _calculate_proximity(self, loc1: str, loc2: str) -> int:
        """Calculate proximity between locations (simplified)"""
        return 0 if loc1.lower() == loc2.lower() else 25
    
    def get_system_analytics(self) -> Dict:
        """Get comprehensive system analytics"""
        impact_report = self.impact_tracker.generate_report()
        
        return {
            "total_volunteers": len(self.volunteers),
            "total_opportunities": len(self.opportunities),
            "active_crises": len([o for o in self.opportunities if o.urgency == UrgencyLevel.CRITICAL]),
            "matching_efficiency": self._calculate_matching_efficiency(),
            "impact_metrics": impact_report
        }
    
    def _calculate_matching_efficiency(self) -> float:
        """Calculate overall matching efficiency"""
        if not self.volunteers or not self.opportunities:
            return 0.0
        
        total_scores = []
        for volunteer in self.volunteers:
            matches = asyncio.run(self.matcher.find_matches(volunteer, self.opportunities))
            if matches:
                total_scores.append(matches[0].match_score if matches else 0)
        
        return sum(total_scores) / len(total_scores) if total_scores else 0.0
