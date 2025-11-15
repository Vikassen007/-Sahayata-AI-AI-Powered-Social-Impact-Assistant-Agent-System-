import asyncio
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import random

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

@dataclass
class MatchResult:
    volunteer: Volunteer
    opportunity: Opportunity
    match_score: float
    reasoning: List[str]
    confidence: float

class SocialGoodOrchestrator:
    """Main AI Agent that coordinates all other agents for maximum social impact"""
    
    def __init__(self):
        self.volunteers = []
        self.opportunities = []
        self.completed_projects = []
        
        # Initialize specialized agents
        self.matcher = SmartMatchingAgent()
        self.optimizer = ResourceOptimizationAgent()
        self.impact_tracker = ImpactTrackingAgent()
        self.communication_agent = CommunicationAgent()
        self.crisis_detector = CrisisDetectionAgent()
        
        print("🤖 AI Agent for Good System Initialized!")
    
    async def add_volunteer(self, volunteer_data: Dict) -> Volunteer:
        """Add a new volunteer to the system"""
        volunteer = Volunteer(**volunteer_data)
        self.volunteers.append(volunteer)
        
        # Generate immediate matches
        matches = await self.matcher.find_best_matches(volunteer, self.opportunities)
        
        # Send welcome message with opportunities
        await self.communication_agent.send_welcome_package(volunteer, matches)
        
        print(f"✅ Volunteer {volunteer.name} added. Found {len(matches)} potential matches.")
        return volunteer
    
    async def add_opportunity(self, opportunity_data: Dict) -> Opportunity:
        """Add a new community opportunity"""
        opportunity = Opportunity(**opportunity_data)
        self.opportunities.append(opportunity)
        
        # Find suitable volunteers
        suitable_volunteers = await self.matcher.find_volunteers_for_opportunity(
            opportunity, self.volunteers
        )
        
        # Optimize resource allocation
        allocation_plan = await self.optimizer.allocate_resources(
            opportunity, suitable_volunteers
        )
        
        print(f"✅ Opportunity '{opportunity.title}' added. "
              f"Found {len(suitable_volunteers)} suitable volunteers.")
        
        return opportunity
    
    async def process_crisis_alert(self, crisis_data: Dict):
        """Process emergency situations and deploy rapid response"""
        crisis_opportunities = await self.crisis_detector.generate_response_plan(crisis_data)
        
        for crisis_opp in crisis_opportunities:
            await self.add_opportunity(crisis_opp)
            
        # Mobilize nearby volunteers
        mobilized = await self.mobilize_emergency_response(crisis_data)
        return mobilized
    
    async mobilize_emergency_response(self, crisis_data: Dict):
        """Mobilize volunteers for emergency response"""
        nearby_volunteers = [
            v for v in self.volunteers 
            if self._calculate_distance(v.location, crisis_data['location']) < 50  # Within 50km
        ]
        
        for volunteer in nearby_volunteers:
            await self.communication_agent.send_emergency_alert(volunteer, crisis_data)
        
        return len(nearby_volunteers)

class SmartMatchingAgent:
    """AI Agent specialized in intelligent volunteer-opportunity matching"""
    
    def __init__(self):
        self.skill_weights = {
            'technical': 1.2, 'medical': 1.3, 'teaching': 1.1, 
            'construction': 1.1, 'leadership': 1.2, 'language': 1.1
        }
        
    async def find_best_matches(self, volunteer: Volunteer, opportunities: List[Opportunity]) -> List[MatchResult]:
        """Find best opportunities for a volunteer"""
        matches = []
        
        for opportunity in opportunities:
            score, reasoning, confidence = await self._calculate_match(volunteer, opportunity)
            
            if score > 0.3:  # Minimum threshold
                matches.append(MatchResult(
                    volunteer=volunteer,
                    opportunity=opportunity,
                    match_score=score,
                    reasoning=reasoning,
                    confidence=confidence
                ))
        
        # Sort by match score
        matches.sort(key=lambda x: x.match_score, reverse=True)
        return matches[:5]  # Return top 5 matches
    
    async def find_volunteers_for_opportunity(self, opportunity: Opportunity, volunteers: List[Volunteer]) -> List[MatchResult]:
        """Find best volunteers for an opportunity"""
        matches = []
        
        for volunteer in volunteers:
            score, reasoning, confidence = await self._calculate_match(volunteer, opportunity)
            
            if score > 0.4:  # Higher threshold for opportunity matching
                matches.append(MatchResult(
                    volunteer=volunteer,
                    opportunity=opportunity,
                    match_score=score,
                    reasoning=reasoning,
                    confidence=confidence
                ))
        
        matches.sort(key=lambda x: x.match_score, reverse=True)
        return matches
    
    async def _calculate_match(self, volunteer: Volunteer, opportunity: Opportunity) -> tuple:
        """Calculate match score with detailed reasoning"""
        score = 0.0
        reasoning = []
        max_score = 0.0
        
        # Skill matching (40%)
        skill_score = self._calculate_skill_match(volunteer.skills, opportunity.required_skills)
        score += skill_score * 0.4
        max_score += 0.4
        if skill_score > 0.6:
            reasoning.append("Strong skill alignment")
        
        # Location matching (20%)
        location_score = 1.0 if volunteer.location == opportunity.location else 0.3
        score += location_score * 0.2
        max_score += 0.2
        if location_score == 1.0:
            reasoning.append("Perfect location match")
        
        # Interest alignment (15%)
        interest_score = 1.0 if opportunity.impact_area in volunteer.interests else 0.2
        score += interest_score * 0.15
        max_score += 0.15
        if interest_score == 1.0:
            reasoning.append("Matches volunteer interests")
        
        # Urgency consideration (10%)
        urgency_score = opportunity.urgency.value * 0.25
        score += min(urgency_score, 0.1)
        max_score += 0.1
        if opportunity.urgency.value >= 3:
            reasoning.append("High urgency need")
        
        # Experience level (10%)
        exp_score = self._calculate_experience_score(volunteer.experience_level)
        score += exp_score * 0.1
        max_score += 0.1
        
        # Availability (5%)
        avail_score = self._calculate_availability_match(volunteer.availability, opportunity.timeframe)
        score += avail_score * 0.05
        max_score += 0.05
        
        # Normalize score
        normalized_score = score / max_score if max_score > 0 else 0
        confidence = min(normalized_score * 1.2, 1.0)  # Confidence can be slightly higher than score
        
        return normalized_score, reasoning, confidence
    
    def _calculate_skill_match(self, volunteer_skills: List[str], required_skills: List[str]) -> float:
        """Calculate skill matching with weights"""
        if not required_skills:
            return 0.5  # Neutral score if no specific skills required
        
        matched_skills = set(volunteer_skills) & set(required_skills)
        if not matched_skills:
            return 0.0
        
        total_weight = sum(self.skill_weights.get(skill, 1.0) for skill in matched_skills)
        max_possible = sum(self.skill_weights.get(skill, 1.0) for skill in required_skills)
        
        return total_weight / max_possible

class ResourceOptimizationAgent:
    """AI Agent for optimizing resource allocation and impact maximization"""
    
    def __init__(self):
        self.impact_multipliers = {
            ImpactArea.DISASTER_RELIEF: 2.0,
            ImpactArea.HEALTHCARE: 1.5,
            ImpactArea.EDUCATION: 1.3,
            ImpactArea.POVERTY: 1.4,
            ImpactArea.ENVIRONMENT: 1.2,
            ImpactArea.EQUALITY: 1.3
        }
    
    async def allocate_resources(self, opportunity: Opportunity, volunteers: List[Volunteer]) -> Dict:
        """Create optimal resource allocation plan"""
        allocation = {
            'assigned_volunteers': [],
            'resource_distribution': {},
            'expected_impact': 0.0,
            'efficiency_score': 0.0
        }
        
        # Sort volunteers by match score and availability
        sorted_volunteers = sorted(
            volunteers, 
            key=lambda x: x.match_score, 
            reverse=True
        )[:opportunity.volunteers_needed]
        
        allocation['assigned_volunteers'] = [
            {
                'volunteer_id': match.volunteer.id,
                'match_score': match.match_score,
                'role': self._assign_role(match.volunteer, opportunity)
            }
            for match in sorted_volunteers
        ]
        
        # Calculate expected impact
        allocation['expected_impact'] = self._calculate_expected_impact(
            opportunity, sorted_volunteers
        )
        
        allocation['efficiency_score'] = self._calculate_efficiency(
            opportunity, sorted_volunteers
        )
        
        return allocation
    
    def _calculate_expected_impact(self, opportunity: Opportunity, volunteers: List) -> float:
        """Calculate expected social impact"""
        base_impact = opportunity.urgency.value * 0.25
        skill_multiplier = sum(v.match_score for v in volunteers) / len(volunteers) if volunteers else 0
        area_multiplier = self.impact_multipliers.get(opportunity.impact_area, 1.0)
        
        return base_impact * skill_multiplier * area_multiplier

class ImpactTrackingAgent:
    """AI Agent for measuring and tracking social impact"""
    
    def __init__(self):
        self.projects_completed = 0
        self.total_impact_score = 0.0
        self.volunteer_hours_logged = 0
        
    async def record_completion(self, volunteer: Volunteer, opportunity: Opportunity, 
                              outcomes: Dict) -> Dict:
        """Record project completion and calculate impact"""
        impact_score = self._calculate_impact_score(opportunity, outcomes)
        
        completion_record = {
            'volunteer_id': volunteer.id,
            'opportunity_id': opportunity.id,
            'completion_date': datetime.now(),
            'hours_contributed': outcomes.get('hours_contributed', 0),
            'people_impacted': outcomes.get('people_impacted', 0),
            'impact_score': impact_score,
            'feedback': outcomes.get('feedback', {})
        }
        
        # Update system metrics
        self.projects_completed += 1
        self.total_impact_score += impact_score
        self.volunteer_hours_logged += outcomes.get('hours_contributed', 0)
        
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
        
        # Urgency multiplier
        urgency_multiplier = opportunity.urgency.value * 0.25
        
        # Sustainability factor (long-term vs immediate impact)
        sustainability = outcomes.get('sustainability_score', 0.5)
        
        final_score = base_score * urgency_multiplier * (1 + sustainability)
        return min(final_score, 1.0)
    
    def generate_impact_report(self) -> Dict:
        """Generate comprehensive impact report"""
        return {
            'total_projects_completed': self.projects_completed,
            'total_volunteer_hours': self.volunteer_hours_logged,
            'total_impact_score': self.total_impact_score,
            'average_impact_per_project': self.total_impact_score / max(self.projects_completed, 1),
            'efficiency_rating': self._calculate_efficiency_rating()
        }

class CommunicationAgent:
    """AI Agent for managing all communications and engagement"""
    
    async def send_welcome_package(self, volunteer: Volunteer, matches: List[MatchResult]):
        """Send personalized welcome package to new volunteer"""
        message = f"""
        🎉 Welcome to Agent for Good, {volunteer.name}!
        
        We're thrilled to have you join our community of change-makers. 
        Based on your skills in {', '.join(volunteer.skills[:3])}, 
        we've found {len(matches)} opportunities that match your profile.
        
        Top recommendation: {matches[0].opportunity.title if matches else 'Check our platform'}
        
        Ready to make an impact? Let's get started!
        """
        
        print(f"📧 Welcome message sent to {volunteer.name}")
        return message
    
    async def send_opportunity_alert(self, volunteers: List[Volunteer], opportunity: Opportunity):
        """Send opportunity alerts to relevant volunteers"""
        for volunteer in volunteers:
            message = f"""
            🔔 New Opportunity Alert!
            
            {opportunity.title}
            Organization: {opportunity.organization}
            Location: {opportunity.location}
            
            Your skills in {', '.join(volunteer.skills[:2])} are needed!
            Urgency: {opportunity.urgency.name}
            
            Act now to make a difference!
            """
            
            print(f"📢 Opportunity alert sent to {volunteer.name}")
    
    async def send_emergency_alert(self, volunteer: Volunteer, crisis_data: Dict):
        """Send emergency response alerts"""
        message = f"""
        🚨 EMERGENCY RESPONSE NEEDED!
        
        Crisis: {crisis_data.get('type', 'Emergency')}
        Location: {crisis_data.get('location', 'Near you')}
        Urgency: {crisis_data.get('urgency', 'HIGH')}
        
        Your help is urgently needed. Can you assist?
        """
        
        print(f"🚨 Emergency alert sent to {volunteer.name}")

class CrisisDetectionAgent:
    """AI Agent for detecting and responding to crises"""
    
    async def monitor_global_events(self):
        """Continuously monitor for crisis situations"""
        # This would integrate with news APIs, weather alerts, etc.
        simulated_crises = [
            {
                'type': 'natural_disaster',
                'location': 'Coastal Region',
                'severity': 'high',
                'people_affected': 10000,
                'resources_needed': ['medical', 'shelter', 'food']
            }
        ]
        
        return simulated_crises
    
    async def generate_response_plan(self, crisis_data: Dict) -> List[Dict]:
        """Generate rapid response opportunities for crises"""
        opportunities = []
        
        base_opportunity = {
            'id': f"crisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'title': f"Emergency Response: {crisis_data['type'].replace('_', ' ').title()}",
            'organization': 'Rapid Response Team',
            'description': f"Urgent assistance needed for {crisis_data['type']} in {crisis_data['location']}",
            'required_skills': crisis_data.get('resources_needed', ['general']),
            'location': crisis_data['location'],
            'impact_area': ImpactArea.DISASTER_RELIEF,
            'urgency': UrgencyLevel.CRITICAL,
            'timeframe': {
                'start': datetime.now(),
                'end': datetime.now() + timedelta(days=7)
            },
            'volunteers_needed': 50,
            'resources_required': {
                'medical_kits': 100,
                'shelter_materials': 200,
                'food_packages': 500
            }
        }
        
        opportunities.append(base_opportunity)
        return opportunities

# 🌟 DEMONSTRATION AND USAGE
async def demonstrate_ai_agent_for_good():
    """Demonstrate the complete AI Agent for Good system"""
    print("🚀 Starting AI Agent for Good Demonstration...\n")
    
    # Initialize the main orchestrator
    orchestrator = SocialGoodOrchestrator()
    
    # Sample volunteers
    sample_volunteers = [
        {
            'id': 'vol_001',
            'name': 'Dr. Sarah Chen',
            'skills': ['medical', 'emergency_response', 'leadership', 'mandarin'],
            'location': 'Metro City',
            'availability': {'weekdays': True, 'weekends': True, 'emergency': True},
            'interests': [ImpactArea.HEALTHCARE, ImpactArea.DISASTER_RELIEF],
            'experience_level': 'expert',
            'languages': ['English', 'Mandarin', 'Spanish'],
            'max_hours_per_week': 20
        },
        {
            'id': 'vol_002', 
            'name': 'James Wilson',
            'skills': ['teaching', 'youth_mentoring', 'sports_coaching'],
            'location': 'Suburb Town',
            'availability': {'weekdays': False, 'weekends': True, 'emergency': False},
            'interests': [ImpactArea.EDUCATION, ImpactArea.EQUALITY],
            'experience_level': 'intermediate',
            'languages': ['English'],
            'max_hours_per_week': 10
        }
    ]
    
    # Sample opportunities
    sample_opportunities = [
        {
            'id': 'opp_001',
            'title': 'Community Health Clinic',
            'organization': 'Health for All Foundation',
            'description': 'Provide medical services in underserved communities',
            'required_skills': ['medical', 'emergency_response', 'patient_care'],
            'location': 'Metro City',
            'impact_area': ImpactArea.HEALTHCARE,
            'urgency': UrgencyLevel.HIGH,
            'timeframe': {
                'start': datetime(2024, 1, 15),
                'end': datetime(2024, 6, 15)
            },
            'volunteers_needed': 15,
            'resources_required': {'medical_supplies': 50, 'volunteers': 15}
        },
        {
            'id': 'opp_002',
            'title': 'After-School Tutoring Program',
            'organization': 'Future Leaders Initiative',
            'description': 'Help students from low-income families with academic support',
            'required_skills': ['teaching', 'youth_mentoring', 'subject_expertise'],
            'location': 'Suburb Town', 
            'impact_area': ImpactArea.EDUCATION,
            'urgency': UrgencyLevel.MEDIUM,
            'timeframe': {
                'start': datetime(2024, 2, 1),
                'end': datetime(2024, 5, 30)
            },
            'volunteers_needed': 10,
            'resources_required': {'educational_materials': 100, 'volunteers': 10}
        }
    ]
    
    print("1. 📝 Adding Volunteers to System...")
    volunteers = []
    for vol_data in sample_volunteers:
        volunteer = await orchestrator.add_volunteer(vol_data)
        volunteers.append(volunteer)
    
    print("\n2. 📋 Adding Opportunities to System...")
    opportunities = []
    for opp_data in sample_opportunities:
        opportunity = await orchestrator.add_opportunity(opp_data)
        opportunities.append(opportunity)
    
    print("\n3. 🔍 Testing Smart Matching...")
    matcher = SmartMatchingAgent()
    for volunteer in volunteers:
        matches = await matcher.find_best_matches(volunteer, opportunities)
        print(f"   {volunteer.name}: {len(matches)} matches found")
        for match in matches[:2]:  # Show top 2 matches
            print(f"     - {match.opportunity.title} ({match.match_score:.1%})")
    
    print("\n4. 📊 Testing Impact Tracking...")
    impact_tracker = ImpactTrackingAgent()
    completion_record = await impact_tracker.record_completion(
        volunteers[0], opportunities[0],
        {
            'hours_contributed': 8,
            'people_impacted': 25,
            'quality_rating': 0.9,
            'sustainability_score': 0.7,
            'feedback': {'rating': 5, 'comments': 'Excellent service'}
        }
    )
    print(f"   Recorded impact: {completion_record['impact_score']:.2f}")
    
    print("\n5. 📈 Generating Impact Report...")
    impact_report = impact_tracker.generate_impact_report()
    for key, value in impact_report.items():
        print(f"   {key}: {value}")
    
    print("\n6. 🚨 Simulating Crisis Response...")
    crisis_data = {
        'type': 'flood',
        'location': 'Coastal Region', 
        'severity': 'high',
        'people_affected': 15000,
        'resources_needed': ['medical', 'rescue', 'shelter']
    }
    
    mobilized = await orchestrator.process_crisis_alert(crisis_data)
    print(f"   Mobilized {mobilized} volunteers for crisis response")
    
    print("\n🎉 AI Agent for Good Demonstration Completed!")
    print("✨ The system is ready to coordinate volunteers, optimize resources, and maximize social impact!")

# Run the demonstration
if __name__ == "__main__":
    asyncio.run(demonstrate_ai_agent_for_good())
