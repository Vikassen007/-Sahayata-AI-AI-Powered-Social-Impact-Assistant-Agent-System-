from typing import List, Dict, Any, Tuple
import numpy as np
from agent import BaseAgent, Volunteer, Opportunity, MatchResult
from config import AgentConfig, ImpactArea
from agent.utils import AgentUtils

class MatchingAgent(BaseAgent):
    """AI Agent for intelligent volunteer-opportunity matching"""
    
    def __init__(self):
        super().__init__("MatchingAgent")
        self.skill_weights = AgentConfig.MATCHING_WEIGHTS
    
    async def find_matches(self, volunteer: Volunteer, opportunities: List[Opportunity]) -> List[MatchResult]:
        """Find best matches for a volunteer"""
        matches = []
        
        for opportunity in opportunities:
            score, reasoning, confidence = await self._calculate_compatibility(volunteer, opportunity)
            
            if score >= AgentConfig.MIN_MATCH_SCORE:
                matches.append(MatchResult(
                    volunteer=volunteer,
                    opportunity=opportunity,
                    match_score=score,
                    reasoning=reasoning,
                    confidence=confidence
                ))
        
        matches.sort(key=lambda x: x.match_score, reverse=True)
        return matches[:AgentConfig.MAX_RECOMMENDATIONS]
    
    async def find_volunteers(self, opportunity: Opportunity, volunteers: List[Volunteer]) -> List[MatchResult]:
        """Find suitable volunteers for an opportunity"""
        matches = []
        
        for volunteer in volunteers:
            score, reasoning, confidence = await self._calculate_compatibility(volunteer, opportunity)
            
            if score >= AgentConfig.MIN_MATCH_SCORE + 0.1:  # Higher threshold for opportunity matching
                matches.append(MatchResult(
                    volunteer=volunteer,
                    opportunity=opportunity,
                    match_score=score,
                    reasoning=reasoning,
                    confidence=confidence
                ))
        
        matches.sort(key=lambda x: x.match_score, reverse=True)
        return matches[:opportunity.volunteers_needed]
    
    async def _calculate_compatibility(self, volunteer: Volunteer, opportunity: Opportunity) -> Tuple[float, List[str], float]:
        """Calculate comprehensive compatibility score"""
        score = 0.0
        reasoning = []
        max_score = 0.0
        
        # Skill matching
        skill_score = self._calculate_skill_match(volunteer.skills, opportunity.required_skills)
        score += skill_score * self.skill_weights["skills"]
        max_score += self.skill_weights["skills"]
        if skill_score > 0.6:
            reasoning.append("Strong skill alignment")
        
        # Location matching
        location_score = 1.0 if volunteer.location == opportunity.location else 0.3
        score += location_score * self.skill_weights["location"]
        max_score += self.skill_weights["location"]
        if location_score == 1.0:
            reasoning.append("Perfect location match")
        
        # Interest alignment
        interest_score = 1.0 if opportunity.impact_area in volunteer.interests else 0.2
        score += interest_score * self.skill_weights["interests"]
        max_score += self.skill_weights["interests"]
        if interest_score == 1.0:
            reasoning.append("Matches interests")
        
        # Urgency consideration
        urgency_score = opportunity.urgency.value * 0.25
        score += min(urgency_score, self.skill_weights["urgency"])
        max_score += self.skill_weights["urgency"]
        if opportunity.urgency.value >= 3:
            reasoning.append("High urgency need")
        
        # Experience level
        exp_score = self._calculate_experience_score(volunteer.experience_level)
        score += exp_score * self.skill_weights["experience"]
        max_score += self.skill_weights["experience"]
        
        # Availability
        avail_score = self._calculate_availability_match(volunteer.availability, opportunity.timeframe)
        score += avail_score * self.skill_weights["availability"]
        max_score += self.skill_weights["availability"]
        
        # Normalize and calculate confidence
        normalized_score = score / max_score if max_score > 0 else 0
        confidence = min(normalized_score * 1.2, 1.0)
        
        return normalized_score, reasoning, confidence
    
    def _calculate_skill_match(self, volunteer_skills: List[str], required_skills: List[str]) -> float:
        """Calculate weighted skill matching"""
        if not required_skills:
            return 0.5
        
        matched_skills = set(volunteer_skills) & set(required_skills)
        if not matched_skills:
            return 0.0
        
        # Use weights from config
        total_weight = sum(self.skill_weights.get(skill, 1.0) for skill in matched_skills)
        max_possible = sum(self.skill_weights.get(skill, 1.0) for skill in required_skills)
        
        return total_weight / max_possible
    
    def _calculate_experience_score(self, experience_level: str) -> float:
        """Calculate experience score"""
        levels = {'beginner': 0.3, 'intermediate': 0.7, 'expert': 1.0}
        return levels.get(experience_level, 0.5)
    
    def _calculate_availability_match(self, availability: Dict, timeframe: Dict) -> float:
        """Calculate availability match score"""
        # Simplified implementation
        return 0.8 if any(availability.values()) else 0.2
