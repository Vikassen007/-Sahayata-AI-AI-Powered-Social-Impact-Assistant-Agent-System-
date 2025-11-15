import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Tuple
import asyncio

class VolunteerMatchingAgent:
    """AI Agent for matching volunteers with opportunities"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.volunteer_profiles = []
        self.opportunities = []
        self.fitted = False
        
    def add_volunteer(self, skills: List[str], availability: Dict, location: str, 
                     interests: List[str], experience_level: str):
        """Add a volunteer profile to the system"""
        profile = {
            'skills': skills,
            'availability': availability,
            'location': location,
            'interests': interests,
            'experience_level': experience_level,
            'id': len(self.volunteer_profiles) + 1
        }
        self.volunteer_profiles.append(profile)
        return profile
    
    def add_opportunity(self, title: str, required_skills: List[str], 
                       location: str, timeframe: Dict, impact_area: str,
                       organization: str, urgency: int = 1):
        """Add a community service opportunity"""
        opportunity = {
            'title': title,
            'required_skills': required_skills,
            'location': location,
            'timeframe': timeframe,
            'impact_area': impact_area,
            'organization': organization,
            'urgency': urgency,
            'id': len(self.opportunities) + 1
        }
        self.opportunities.append(opportunity)
        return opportunity
    
    def calculate_match_score(self, volunteer: Dict, opportunity: Dict) -> float:
        """Calculate compatibility score between volunteer and opportunity"""
        score = 0.0
        
        # Skill matching (40% weight)
        skill_match = len(set(volunteer['skills']) & set(opportunity['required_skills']))
        skill_match /= max(len(opportunity['required_skills']), 1)
        score += skill_match * 0.4
        
        # Location proximity (20% weight)
        location_score = 1.0 if volunteer['location'] == opportunity['location'] else 0.3
        score += location_score * 0.2
        
        # Interest alignment (20% weight)
        interest_text = ' '.join(volunteer['interests'])
        impact_text = opportunity['impact_area']
        if hasattr(self, 'interest_vectorizer'):
            interest_vec = self.interest_vectorizer.transform([interest_text])
            impact_vec = self.interest_vectorizer.transform([impact_text])
            interest_sim = cosine_similarity(interest_vec, impact_vec)[0][0]
            score += interest_sim * 0.2
        
        # Urgency bonus (10% weight)
        urgency_bonus = opportunity['urgency'] * 0.1
        score += min(urgency_bonus, 0.1)
        
        # Experience level (10% weight)
        exp_levels = {'beginner': 0.3, 'intermediate': 0.7, 'expert': 1.0}
        exp_score = exp_levels.get(volunteer['experience_level'], 0.5) * 0.1
        score += exp_score
        
        return min(score, 1.0)
    
    def find_best_matches(self, volunteer_id: int, top_n: int = 5) -> List[Tuple[Dict, float]]:
        """Find top matching opportunities for a volunteer"""
        volunteer = next((v for v in self.volunteer_profiles if v['id'] == volunteer_id), None)
        if not volunteer:
            return []
        
        matches = []
        for opportunity in self.opportunities:
            score = self.calculate_match_score(volunteer, opportunity)
            matches.append((opportunity, score))
        
        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:top_n]
    
    def train_interest_model(self):
        """Train the interest matching model"""
        all_texts = []
        for volunteer in self.volunteer_profiles:
            all_texts.extend(volunteer['interests'])
        for opportunity in self.opportunities:
            all_texts.append(opportunity['impact_area'])
        
        if all_texts:
            self.interest_vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            self.interest_vectorizer.fit(all_texts)
            self.fitted = True

class ImpactTrackingAgent:
    """AI Agent for tracking and measuring social impact"""
    
    def __init__(self):
        self.completed_opportunities = []
        self.impact_metrics = {}
        
    def record_completion(self, volunteer_id: int, opportunity_id: int, 
                         hours_contributed: float, outcomes: Dict):
        """Record a completed volunteer opportunity"""
        completion = {
            'volunteer_id': volunteer_id,
            'opportunity_id': opportunity_id,
            'hours_contributed': hours_contributed,
            'outcomes': outcomes,
            'timestamp': datetime.now(),
            'impact_score': self.calculate_impact_score(outcomes, hours_contributed)
        }
        self.completed_opportunities.append(completion)
        return completion
    
    def calculate_impact_score(self, outcomes: Dict, hours: float) -> float:
        """Calculate a normalized impact score"""
        base_score = 0.0
        
        # People helped
        people_helped = outcomes.get('people_helped', 0)
        base_score += min(people_helped * 0.1, 0.3)
        
        # Environmental impact
        environmental = outcomes.get('environmental_impact', 0)
        base_score += min(environmental * 0.05, 0.2)
        
        # Educational impact
        educational = outcomes.get('educational_impact', 0)
        base_score += min(educational * 0.08, 0.2)
        
        # Hours multiplier
        hour_multiplier = min(hours / 10, 2.0)  # Cap at 2x for 20+ hours
        final_score = base_score * hour_multiplier
        
        return min(final_score, 1.0)
    
    def generate_impact_report(self, timeframe_days: int = 30) -> Dict:
        """Generate a comprehensive impact report"""
        cutoff_date = datetime.now() - timedelta(days=timeframe_days)
        recent_completions = [
            c for c in self.completed_opportunities 
            if c['timestamp'] >= cutoff_date
        ]
        
        total_hours = sum(c['hours_contributed'] for c in recent_completions)
        total_impact = sum(c['impact_score'] for c in recent_completions)
        unique_volunteers = len(set(c['volunteer_id'] for c in recent_completions))
        
        return {
            'report_period': f"Last {timeframe_days} days",
            'total_volunteer_hours': total_hours,
            'total_impact_score': total_impact,
            'unique_volunteers': unique_volunteers,
            'average_impact_per_hour': total_impact / max(total_hours, 1),
            'completions_count': len(recent_completions)
        }

class ResourceOptimizationAgent:
    """AI Agent for optimizing resource allocation"""
    
    def __init__(self):
        self.resource_pool = {}
        self.demand_patterns = {}
        
    def allocate_resources(self, opportunities: List[Dict], available_resources: Dict) -> Dict:
        """Optimally allocate resources to opportunities based on impact potential"""
        # Sort opportunities by urgency and potential impact
        prioritized_ops = sorted(opportunities, 
                               key=lambda x: (x['urgency'], -len(x['required_skills'])), 
                               reverse=True)
        
        allocation = {}
        remaining_resources = available_resources.copy()
        
        for opportunity in prioritized_ops:
            op_allocation = {}
            for resource_type, needed in self.estimate_resource_needs(opportunity).items():
                allocated = min(needed, remaining_resources.get(resource_type, 0))
                if allocated > 0:
                    op_allocation[resource_type] = allocated
                    remaining_resources[resource_type] -= allocated
            
            if op_allocation:
                allocation[opportunity['id']] = op_allocation
        
        return allocation
    
    def estimate_resource_needs(self, opportunity: Dict) -> Dict:
        """Estimate resource requirements for an opportunity"""
        base_needs = {
            'volunteers': len(opportunity['required_skills']),
            'funding': opportunity['urgency'] * 100,  # Simplified calculation
            'equipment': max(len(opportunity['required_skills']) - 2, 1),
            'supervision': 1 if len(opportunity['required_skills']) > 3 else 0
        }
        return base_needs

class AgentForGoodSystem:
    """Main system coordinating all AI agents for social good"""
    
    def __init__(self):
        self.matching_agent = VolunteerMatchingAgent()
        self.impact_agent = ImpactTrackingAgent()
        self.optimization_agent = ResourceOptimizationAgent()
        self.is_trained = False
        
    def initialize_system(self):
        """Initialize the system with sample data and train models"""
        # Add sample volunteers
        self.matching_agent.add_volunteer(
            skills=['teaching', 'communication', 'first_aid'],
            availability={'weekends': True, 'weekdays': False},
            location='New York',
            interests=['education', 'children', 'community'],
            experience_level='intermediate'
        )
        
        self.matching_agent.add_volunteer(
            skills=['carpentry', 'construction', 'project_management'],
            availability={'weekends': True, 'weekdays': True},
            location='Chicago',
            interests=['housing', 'construction', 'elderly'],
            experience_level='expert'
        )
        
        # Add sample opportunities
        self.matching_agent.add_opportunity(
            title='After School Tutoring Program',
            required_skills=['teaching', 'communication', 'patience'],
            location='New York',
            timeframe={'start': '2024-01-15', 'end': '2024-06-15'},
            impact_area='education',
            organization='City Youth Program',
            urgency=2
        )
        
        self.matching_agent.add_opportunity(
            title='Community Garden Construction',
            required_skills=['construction', 'project_management', 'teamwork'],
            location='Chicago',
            timeframe={'start': '2024-02-01', 'end': '2024-03-01'},
            impact_area='environment',
            organization='Green Earth Initiative',
            urgency=3
        )
        
        # Train the matching models
        self.matching_agent.train_interest_model()
        self.is_trained = True
        
    async def process_volunteer_signup(self, volunteer_data: Dict) -> List[Dict]:
        """Process new volunteer signup and return recommendations"""
        if not self.is_trained:
            self.initialize_system()
        
        # Add volunteer to system
        volunteer = self.matching_agent.add_volunteer(**volunteer_data)
        
        # Get matches
        matches = self.matching_agent.find_best_matches(volunteer['id'])
        
        # Format recommendations
        recommendations = []
        for opportunity, score in matches:
            recommendations.append({
                'opportunity': opportunity['title'],
                'organization': opportunity['organization'],
                'match_score': round(score * 100, 1),
                'reasoning': self.generate_match_reasoning(volunteer, opportunity, score),
                'next_steps': f"Contact {opportunity['organization']} to get started!"
            })
        
        return recommendations
    
    def generate_match_reasoning(self, volunteer: Dict, opportunity: Dict, score: float) -> str:
        """Generate human-readable reasoning for the match"""
        reasons = []
        
        # Skill overlap
        skill_overlap = set(volunteer['skills']) & set(opportunity['required_skills'])
        if skill_overlap:
            reasons.append(f"Your skills in {', '.join(skill_overlap)} are needed")
        
        # Location match
        if volunteer['location'] == opportunity['location']:
            reasons.append("Perfect location match")
        
        # Interest alignment
        if any(interest in opportunity['impact_area'] for interest in volunteer['interests']):
            reasons.append("Aligns with your interests")
        
        return ". ".join(reasons) + f". Overall match: {score:.0%}"
    
    def get_system_analytics(self) -> Dict:
        """Get comprehensive system analytics"""
        impact_report = self.impact_agent.generate_impact_report()
        
        analytics = {
            'total_volunteers': len(self.matching_agent.volunteer_profiles),
            'total_opportunities': len(self.matching_agent.opportunities),
            'impact_metrics': impact_report,
            'matching_efficiency': self.calculate_matching_efficiency(),
            'system_health': 'Optimal'
        }
        
        return analytics
    
    def calculate_matching_efficiency(self) -> float:
        """Calculate overall matching efficiency of the system"""
        if not self.matching_agent.volunteer_profiles or not self.matching_agent.opportunities:
            return 0.0
        
        total_potential_matches = len(self.matching_agent.volunteer_profiles) * len(self.matching_agent.opportunities)
        if total_potential_matches == 0:
            return 0.0
            
        # Simplified efficiency calculation
        avg_scores = []
        for volunteer in self.matching_agent.volunteer_profiles:
            matches = self.matching_agent.find_best_matches(volunteer['id'], top_n=1)
            if matches:
                avg_scores.append(matches[0][1])
        
        return np.mean(avg_scores) if avg_scores else 0.0

# Example usage and demonstration
async def demo_agent_for_good():
    """Demonstrate the Agent for Good system"""
    print("=== Agent for Good System Demo ===\n")
    
    # Initialize system
    system = AgentForGoodSystem()
    system.initialize_system()
    
    # Demo: New volunteer signup
    new_volunteer = {
        'skills': ['teaching', 'mentoring', 'public_speaking'],
        'availability': {'weekends': True, 'weekdays': True},
        'location': 'New York',
        'interests': ['education', 'career_development', 'youth'],
        'experience_level': 'intermediate'
    }
    
    print("1. Processing new volunteer signup...")
    recommendations = await system.process_volunteer_signup(new_volunteer)
    
    print("2. Personalized recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec['opportunity']}")
        print(f"      Match Score: {rec['match_score']}%")
        print(f"      Reasoning: {rec['reasoning']}")
        print(f"      Next: {rec['next_steps']}\n")
    
    # Demo: Record impact
    print("3. Recording volunteer impact...")
    completion = system.impact_agent.record_completion(
        volunteer_id=1,
        opportunity_id=1,
        hours_contributed=8.5,
        outcomes={
            'people_helped': 15,
            'educational_impact': 8,
            'feedback_score': 4.8
        }
    )
    print(f"   Recorded: {completion['hours_contributed']} hours")
    print(f"   Impact Score: {completion['impact_score']:.2f}")
    
    # Demo: System analytics
    print("\n4. System Analytics:")
    analytics = system.get_system_analytics()
    for key, value in analytics.items():
        print(f"   {key}: {value}")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_agent_for_good())
