#!/usr/bin/env python3
"""
APEX Orchestrator Agent
======================
Central intelligence hub that coordinates ASHA, Athena, and Scribe agents.
Manages complex conversations, multi-agent workflows, and intelligent routing.

This agent acts as the "brain" of the APEX system, making intelligent decisions
about which agents to use, when to combine responses, and how to manage
sophisticated user journeys that require coordination between multiple specialists.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class ConversationState(Enum):
    """Conversation states for tracking user journey"""
    GREETING = "greeting"
    INFORMATION_GATHERING = "info_gathering"
    PROBLEM_ANALYSIS = "problem_analysis"
    SOLUTION_PROVIDING = "solution_providing"
    DOCUMENT_CREATION = "document_creation"
    FOLLOW_UP = "follow_up"
    CLOSURE = "closure"


class AgentType(Enum):
    """Available agent types"""
    ASHA = "asha"       # Emotional support
    ATHENA = "athena"   # Legal guidance
    SCRIBE = "scribe"   # Document generation
    ORCHESTRATOR = "orchestrator"  # This agent


@dataclass
class ConversationTurn:
    """Single turn in a conversation"""
    timestamp: datetime
    user_message: str
    agent_used: AgentType
    agent_response: str
    confidence_score: float
    context_tags: List[str]
    workflow_step: Optional[str] = None


@dataclass
class UserSession:
    """Complete user session with conversation history and context"""
    session_id: str
    user_id: Optional[str]
    started_at: datetime
    last_activity: datetime
    conversation_state: ConversationState
    turns: List[ConversationTurn]
    user_profile: Dict[str, Any]
    active_workflows: List[str]
    preferences: Dict[str, Any]


class OrchestratorAgent:
    """
    Advanced orchestration agent that manages multi-agent interactions
    and provides intelligent conversation management for APEX system
    """
    
    def __init__(self, api_key: str = None):
        """Initialize the orchestrator agent"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.sessions: Dict[str, UserSession] = {}
        
        # Agent instances (lazy loaded)
        self._asha_agent = None
        self._athena_agent = None
        self._scribe_agent = None
        
        # Conversation patterns and workflows
        self._load_conversation_patterns()
        
        print("🎯 Orchestrator Agent initialized - Ready for intelligent coordination")
    
    def _load_conversation_patterns(self):
        """Load conversation patterns and workflow definitions"""
        self.conversation_patterns = {
            # Legal + Emotional Support Patterns
            "harassment_support": {
                "agents": ["athena", "asha"],
                "sequence": ["athena", "asha"],
                "triggers": ["harassment", "discrimination", "hostile", "uncomfortable"],
                "description": "Legal guidance followed by emotional support"
            },
            
            # Documentation + Legal Patterns  
            "legal_documentation": {
                "agents": ["athena", "scribe"],
                "sequence": ["athena", "scribe"],
                "triggers": ["create", "generate", "draft", "legal document"],
                "description": "Legal guidance before document creation"
            },
            
            # Complex Employment Issues
            "employment_comprehensive": {
                "agents": ["athena", "asha", "scribe"],
                "sequence": ["athena", "asha", "scribe"],
                "triggers": ["termination", "wrongful dismissal", "unfair treatment"],
                "description": "Legal + emotional + documentation support"
            },
            
            # Maternity/Pregnancy Support
            "maternity_support": {
                "agents": ["athena", "asha", "scribe"],
                "sequence": ["athena", "asha", "scribe"],
                "triggers": ["maternity", "pregnancy", "pregnant", "baby"],
                "description": "Comprehensive maternity support workflow"
            }
        }
        
        # Intent classification keywords
        self.intent_keywords = {
            "legal": [
                "rights", "law", "legal", "harassment", "discrimination", 
                "wage", "salary", "employment", "termination", "contract",
                "labor", "workplace", "policy", "regulation", "act",
                "court", "litigation", "compliance", "violation"
            ],
            "emotional": [
                "stressed", "anxiety", "worried", "scared", "overwhelmed",
                "depressed", "upset", "frustrated", "angry", "sad",
                "support", "help me cope", "emotional", "feeling",
                "mental health", "wellbeing", "counseling", "guidance"
            ],
            "documentation": [
                "generate", "create", "write", "draft", "compose",
                "application", "form", "letter", "email", "message",
                "document", "report", "proposal", "contract", "agreement"
            ]
        }
    
    def _get_asha_agent(self):
        """Lazy load ASHA agent"""
        if self._asha_agent is None:
            try:
                sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'asha'))
                from asha import AshaAgent
                self._asha_agent = AshaAgent()
                print("✅ Orchestrator loaded ASHA agent")
            except Exception as e:
                print(f"❌ Orchestrator failed to load ASHA: {e}")
        return self._asha_agent
    
    def _get_athena_agent(self):
        """Lazy load Athena agent"""
        if self._athena_agent is None:
            try:
                sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'athena'))
                from athena import AthenaAgent
                self._athena_agent = AthenaAgent()
                print("✅ Orchestrator loaded Athena agent")
            except Exception as e:
                print(f"❌ Orchestrator failed to load Athena: {e}")
        return self._athena_agent
    
    def _get_scribe_agent(self):
        """Lazy load Scribe agent"""
        if self._scribe_agent is None:
            try:
                sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scribe'))
                from scribe import ScribeAgent
                self._scribe_agent = ScribeAgent()
                print("✅ Orchestrator loaded Scribe agent")
            except Exception as e:
                print(f"❌ Orchestrator failed to load Scribe: {e}")
        return self._scribe_agent
    
    def create_session(self, user_id: Optional[str] = None) -> str:
        """Create a new user session"""
        session_id = f"session_{datetime.now().timestamp()}"
        
        session = UserSession(
            session_id=session_id,
            user_id=user_id,
            started_at=datetime.now(),
            last_activity=datetime.now(),
            conversation_state=ConversationState.GREETING,
            turns=[],
            user_profile={},
            active_workflows=[],
            preferences={}
        )
        
        self.sessions[session_id] = session
        return session_id
    
    def analyze_intent_advanced(self, message: str, session_context: Optional[UserSession] = None) -> Dict[str, Any]:
        """
        Advanced intent analysis considering conversation history and context
        """
        message_lower = message.lower()
        
        # Calculate keyword scores
        intent_scores = {}
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            intent_scores[intent] = score
        
        # Check for conversation patterns
        matching_patterns = []
        for pattern_name, pattern in self.conversation_patterns.items():
            pattern_score = sum(1 for trigger in pattern["triggers"] if trigger in message_lower)
            if pattern_score > 0:
                matching_patterns.append({
                    "name": pattern_name,
                    "score": pattern_score,
                    "pattern": pattern
                })
        
        # Consider conversation history if available
        context_boost = {}
        if session_context and session_context.turns:
            recent_turns = session_context.turns[-3:]  # Last 3 turns
            for turn in recent_turns:
                for tag in turn.context_tags:
                    context_boost[tag] = context_boost.get(tag, 0) + 0.5
        
        # Apply context boost
        for intent in intent_scores:
            intent_scores[intent] += context_boost.get(intent, 0)
        
        # Determine primary intent
        primary_intent = max(intent_scores, key=intent_scores.get) if any(intent_scores.values()) else "general"
        
        # Check for multi-agent requirements
        needs_multiple_agents = False
        suggested_workflow = None
        
        if matching_patterns:
            best_pattern = max(matching_patterns, key=lambda x: x["score"])
            if best_pattern["score"] >= 1:
                needs_multiple_agents = True
                suggested_workflow = best_pattern
        
        return {
            "primary_intent": primary_intent,
            "intent_scores": intent_scores,
            "needs_multiple_agents": needs_multiple_agents,
            "suggested_workflow": suggested_workflow,
            "matching_patterns": matching_patterns,
            "confidence": max(intent_scores.values()) / (len(message.split()) / 10 + 1)
        }
    
    def route_to_agent(self, message: str, intent_analysis: Dict[str, Any]) -> str:
        """
        Route message to appropriate agent based on intent analysis
        """
        primary_intent = intent_analysis["primary_intent"]
        
        # Map intents to agents
        intent_to_agent = {
            "legal": "athena",
            "emotional": "asha", 
            "documentation": "scribe"
        }
        
        return intent_to_agent.get(primary_intent, "athena")  # Default to athena for legal guidance
    
    def execute_single_agent_workflow(self, message: str, agent_type: str, session_id: str) -> Dict[str, Any]:
        """
        Execute workflow with a single agent
        """
        try:
            agent = None
            response = None
            
            if agent_type == "asha":
                agent = self._get_asha_agent()
                if agent:
                    response = agent.get_response(message)
            
            elif agent_type == "athena":
                agent = self._get_athena_agent()
                if agent:
                    response = agent.get_response(message)
            
            elif agent_type == "scribe":
                agent = self._get_scribe_agent()
                if agent:
                    response = agent.process_user_input(message)
            
            if not response:
                response = f"I'm sorry, the {agent_type} assistant is currently unavailable. Please try again later."
            
            return {
                "success": True,
                "response": response,
                "agent_used": agent_type,
                "workflow_type": "single_agent"
            }
            
        except Exception as e:
            return {
                "success": False,
                "response": f"Error processing request: {str(e)}",
                "agent_used": agent_type,
                "workflow_type": "single_agent",
                "error": str(e)
            }
    
    def execute_multi_agent_workflow(self, message: str, workflow: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """
        Execute complex workflow involving multiple agents
        """
        try:
            pattern = workflow["pattern"]
            agent_sequence = pattern["sequence"]
            responses = []
            
            for i, agent_type in enumerate(agent_sequence):
                # Modify message context for subsequent agents
                if i > 0:
                    context_message = f"Previous context: {responses[-1]['response'][:200]}...\n\nUser question: {message}"
                else:
                    context_message = message
                
                # Execute with current agent
                result = self.execute_single_agent_workflow(context_message, agent_type, session_id)
                responses.append(result)
                
                # Break if an agent fails
                if not result["success"]:
                    break
            
            # Synthesize final response
            final_response = self._synthesize_multi_agent_response(responses, pattern)
            
            return {
                "success": True,
                "response": final_response,
                "agent_used": "orchestrator", 
                "workflow_type": "multi_agent",
                "agents_involved": agent_sequence,
                "individual_responses": responses
            }
            
        except Exception as e:
            return {
                "success": False,
                "response": f"Error in multi-agent workflow: {str(e)}",
                "agent_used": "orchestrator",
                "workflow_type": "multi_agent",
                "error": str(e)
            }
    
    def _synthesize_multi_agent_response(self, responses: List[Dict[str, Any]], pattern: Dict[str, Any]) -> str:
        """
        Synthesize responses from multiple agents into a coherent answer
        """
        if not responses or not any(r["success"] for r in responses):
            return "I apologize, but I encountered difficulties processing your request. Please try again."
        
        successful_responses = [r for r in responses if r["success"]]
        
        if len(successful_responses) == 1:
            return successful_responses[0]["response"]
        
        # Create synthesized response based on pattern
        pattern_name = pattern.get("description", "multi-agent response")
        
        synthesis = f"## {pattern_name.title()}\n\n"
        
        for i, response in enumerate(successful_responses):
            agent_name = response["agent_used"].upper()
            agent_response = response["response"]
            
            if agent_name == "ATHENA":
                synthesis += f"**🏛️ Legal Guidance:**\n{agent_response}\n\n"
            elif agent_name == "ASHA":
                synthesis += f"**💚 Emotional Support:**\n{agent_response}\n\n"
            elif agent_name == "SCRIBE":
                synthesis += f"**📝 Document Assistance:**\n{agent_response}\n\n"
        
        synthesis += "---\n*This comprehensive response combines insights from multiple APEX specialists to address your situation holistically.*"
        
        return synthesis
    
    def process_message(self, message: str, session_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Main entry point for processing user messages with orchestration
        """
        # Get or create session
        if session_id not in self.sessions:
            session_id = self.create_session(user_id)
        
        session = self.sessions[session_id]
        session.last_activity = datetime.now()
        
        # Analyze intent with conversation context
        intent_analysis = self.analyze_intent_advanced(message, session)
        
        # Determine execution path
        if intent_analysis["needs_multiple_agents"] and intent_analysis["suggested_workflow"]:
            # Execute multi-agent workflow
            result = self.execute_multi_agent_workflow(
                message, 
                intent_analysis["suggested_workflow"], 
                session_id
            )
        else:
            # Execute single agent workflow
            agent_type = self.route_to_agent(message, intent_analysis)
            result = self.execute_single_agent_workflow(message, agent_type, session_id)
        
        # Record conversation turn
        turn = ConversationTurn(
            timestamp=datetime.now(),
            user_message=message,
            agent_used=AgentType(result["agent_used"]),
            agent_response=result["response"],
            confidence_score=intent_analysis["confidence"],
            context_tags=[intent_analysis["primary_intent"]],
            workflow_step=result.get("workflow_type")
        )
        
        session.turns.append(turn)
        
        # Update conversation state
        self._update_conversation_state(session, intent_analysis)
        
        # Prepare response
        response = {
            "response": result["response"],
            "session_id": session_id,
            "agent_used": result["agent_used"],
            "workflow_type": result.get("workflow_type", "single_agent"),
            "conversation_state": session.conversation_state.value,
            "intent_analysis": intent_analysis,
            "timestamp": datetime.now().isoformat()
        }
        
        if "individual_responses" in result:
            response["individual_responses"] = result["individual_responses"]
        
        return response
    
    def _update_conversation_state(self, session: UserSession, intent_analysis: Dict[str, Any]):
        """Update conversation state based on interaction"""
        current_state = session.conversation_state
        primary_intent = intent_analysis["primary_intent"]
        
        # Simple state transitions
        if current_state == ConversationState.GREETING:
            if primary_intent in ["legal", "emotional", "documentation"]:
                session.conversation_state = ConversationState.PROBLEM_ANALYSIS
        
        elif current_state == ConversationState.PROBLEM_ANALYSIS:
            if intent_analysis["needs_multiple_agents"]:
                session.conversation_state = ConversationState.SOLUTION_PROVIDING
            elif primary_intent == "documentation":
                session.conversation_state = ConversationState.DOCUMENT_CREATION
        
        # Add more sophisticated state logic as needed
    
    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get summary of user session"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        return {
            "session_id": session_id,
            "user_id": session.user_id,
            "started_at": session.started_at.isoformat(),
            "last_activity": session.last_activity.isoformat(),
            "conversation_state": session.conversation_state.value,
            "total_turns": len(session.turns),
            "agents_used": list(set(turn.agent_used.value for turn in session.turns)),
            "active_workflows": session.active_workflows,
            "user_profile": session.user_profile
        }
    
    def cleanup_old_sessions(self, hours: int = 24):
        """Clean up sessions older than specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        old_sessions = [
            sid for sid, session in self.sessions.items() 
            if session.last_activity < cutoff_time
        ]
        
        for session_id in old_sessions:
            del self.sessions[session_id]
        
        print(f"🧹 Cleaned up {len(old_sessions)} old sessions")


# Convenience function for simple usage
def create_orchestrator(api_key: str = None) -> OrchestratorAgent:
    """Create and return a new orchestrator agent instance"""
    return OrchestratorAgent(api_key)


if __name__ == "__main__":
    # Demo usage
    print("🎯 APEX Orchestrator Agent Demo")
    
    orchestrator = create_orchestrator()
    
    # Test messages
    test_messages = [
        "I'm being harassed at work and need help",
        "What are my maternity leave rights?", 
        "Can you help me draft a complaint letter?",
        "I'm feeling overwhelmed with my legal situation"
    ]
    
    session_id = orchestrator.create_session("demo_user")
    
    for message in test_messages:
        print(f"\n👤 User: {message}")
        result = orchestrator.process_message(message, session_id)
        print(f"🤖 {result['agent_used'].upper()}: {result['response'][:150]}...")
        print(f"   Workflow: {result['workflow_type']}")