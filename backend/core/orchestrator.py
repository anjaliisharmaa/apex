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
        
        # Agent instances (preloaded for faster responses)
        self._asha_agent = None
        self._athena_agent = None
        self._scribe_agent = None
        
        # Response cache for common queries
        self._response_cache = {}
        self._cache_hits = 0
        
        # Performance optimization flags
        self._fast_mode = True
        self._single_agent_preference = True
        
        # Conversation patterns and workflows
        self._load_conversation_patterns()
        
        print("🎯 Orchestrator Agent initialized - Ready for intelligent coordination")
        print("⚡ Fast mode enabled - prioritizing speed while maintaining context")
        
        # Preload all agents in background for instant responses
        self.preload_all_agents()
    
    def preload_all_agents(self):
        """Preload all agents for instant responses"""
        print("🚀 Preloading all agents for optimized performance...")
        
        # Preload in order of likely usage frequency
        try:
            # 1. Athena (most used for legal queries)
            athena = self._get_athena_agent()
            if athena:
                # Check if Athena has a readiness method
                try:
                    if hasattr(athena, 'is_ready') and athena.is_ready():
                        print("✅ Athena agent preloaded with documents - ready for fast queries")
                    else:
                        print("✅ Athena agent preloaded - legal queries ready")
                except:
                    print("✅ Athena agent preloaded - legal queries ready")
            
            # 2. ASHA (emotional support)  
            asha = self._get_asha_agent()
            if asha:
                print("✅ ASHA agent preloaded - emotional support ready")
            
            # 3. Scribe (document generation)
            scribe = self._get_scribe_agent()
            if scribe:
                print("✅ Scribe agent preloaded - document generation ready")
            
            print("⚡ All agents preloaded - ready for instant responses!")
            
        except Exception as e:
            print(f"⚠️ Some agents could not be preloaded: {e}")
            print("   📝 Agents will be loaded on-demand with slight delay")
    
    def preload_athena_agent(self):
        """Preload Athena agent to cache documents for faster responses"""
        try:
            print("🚀 Preloading Athena agent for optimized performance...")
            athena = self._get_athena_agent()
            if athena:
                # Check if Athena has a readiness method
                try:
                    if hasattr(athena, 'is_ready') and athena.is_ready():
                        print("✅ Athena agent preloaded with cached documents - ready for fast queries!")
                    else:
                        print("✅ Athena agent preloaded - ready for legal queries!")
                except:
                    print("✅ Athena agent preloaded - ready for legal queries!")
            else:
                print("⚠️ Athena agent could not be loaded")
        except Exception as e:
            print(f"⚠️ Could not preload Athena agent: {e}")
            print("   📝 Athena will be loaded on-demand during first legal query")
    
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
    
    def analyze_intent_fast(self, message: str, session_context: Optional[UserSession] = None) -> Dict[str, Any]:
        """
        Fast intent analysis optimized for speed while maintaining accuracy
        """
        message_lower = message.lower()
        
        # Quick keyword scoring (optimized)
        legal_score = sum(1 for k in ["rights", "law", "legal", "maternity", "leave", "transfer", "workplace policy", "contract"] if k in message_lower)
        emotional_score = sum(1 for k in ["stressed", "help", "support", "worried", "overwhelmed", "feeling", "trauma", "traumatic", "traumatising", "traumatizing", "anxiety", "depression", "mental health", "burnout", "emotional", "cope", "coping", "difficult", "struggling", "upset", "hurt", "pain", "distressed", "afraid", "scared", "nervous"] if k in message_lower)
        document_score = sum(1 for k in ["generate", "create", "write", "draft", "form", "application"] if k in message_lower)
        
        # Determine primary intent quickly - prioritize emotional support
        scores = {"legal": legal_score, "emotional": emotional_score, "documentation": document_score}
        
        # Special handling for emotional/trauma queries
        trauma_indicators = ["trauma", "traumatic", "traumatising", "traumatizing", "feels", "feeling"]
        if any(indicator in message_lower for indicator in trauma_indicators):
            emotional_score += 3  # Boost emotional score for trauma-related queries
            scores["emotional"] = emotional_score
        
        # Default to emotional support if no clear intent (workplace support context)
        primary_intent = max(scores, key=scores.get) if any(scores.values()) else "emotional"
        
        # Fast multi-agent check - only for high-complexity cases
        needs_multiple = False
        if legal_score >= 2 and emotional_score >= 1:
            needs_multiple = True
        elif any(word in message_lower for word in ["harassment", "discrimination", "unfair treatment"]):
            needs_multiple = True
        
        return {
            "primary_intent": primary_intent,
            "intent_scores": scores,
            "needs_multiple_agents": needs_multiple,
            "confidence": max(scores.values()) / (len(message.split()) / 8 + 1),
            "fast_mode": True
        }
    
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
        
        return intent_to_agent.get(primary_intent, "asha")  # Default to asha for emotional support
    
    def execute_single_agent_workflow(self, message: str, agent_type: str, session_id: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Execute workflow with a single agent - optimized for speed
        """
        try:
            # Check cache first for faster responses
            cache_key = f"{agent_type}:{hash(message[:100])}"
            if cache_key in self._response_cache:
                self._cache_hits += 1
                cached_response = self._response_cache[cache_key]
                print(f"⚡ Cache hit #{self._cache_hits} - instant response")
                return {
                    "success": True,
                    "response": cached_response,
                    "agent_used": agent_type,
                    "workflow_type": "single_agent",
                    "cached": True
                }
            
            agent = None
            response = None
            start_time = datetime.now()
            
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
            
            # Calculate response time
            response_time = (datetime.now() - start_time).total_seconds()
            
            if not response:
                response = f"I'm sorry, the {agent_type} assistant is currently unavailable. Please try again later."
            
            # Cache successful responses (limit cache size)
            if response and len(self._response_cache) < 100:
                self._response_cache[cache_key] = response
            
            print(f"⚡ Response generated in {response_time:.1f}s")
            
            return {
                "success": True,
                "response": response,
                "agent_used": agent_type,
                "workflow_type": "single_agent",
                "response_time": response_time,
                "cached": False
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
        Execute complex workflow involving multiple agents - optimized for speed
        """
        try:
            pattern = workflow["pattern"]
            agent_sequence = pattern["sequence"]
            
            # Fast mode: Return primary agent response immediately if enabled
            if self._fast_mode and len(agent_sequence) > 1:
                primary_agent = agent_sequence[0]
                print(f"⚡ Fast mode: Using primary agent {primary_agent} for quick response")
                result = self.execute_single_agent_workflow(message, primary_agent, session_id)
                
                # Add note about comprehensive support available
                if result["success"]:
                    result["response"] += f"\n\n*Note: For comprehensive support combining {', '.join(agent_sequence)} specialists, please let me know if you need additional assistance.*"
                    result["workflow_type"] = "fast_multi_agent"
                    result["agents_available"] = agent_sequence
                
                return result
            
            # Full multi-agent workflow (fallback)
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
            
            # Clean up the response by removing excessive markdown
            cleaned_response = self._clean_response_formatting(agent_response)
            
            if agent_name == "ATHENA":
                synthesis += f"Legal Guidance:\n{cleaned_response}\n\n"
            elif agent_name == "ASHA":
                synthesis += f"Emotional Support:\n{cleaned_response}\n\n"
            elif agent_name == "SCRIBE":
                synthesis += f"Document Assistance:\n{cleaned_response}\n\n"
        
        synthesis += "This comprehensive response combines insights from multiple APEX specialists to address your situation holistically."
        
        return synthesis
    
    def _clean_response_formatting(self, response: str) -> str:
        """Clean up excessive markdown formatting from responses"""
        import re
        
        # Remove excessive markdown headers (## and ###)
        response = re.sub(r'^#{2,3}\s*', '', response, flags=re.MULTILINE)
        
        # Convert **bold** to simple bold formatting
        response = re.sub(r'\*\*(.*?)\*\*', r'\1', response)
        
        # Remove emoji headers like 🏛️, 💚, 📝, etc.
        response = re.sub(r'^[🏛️💚📝⚖️🔶📄🔄⏱️📋📞📚]\s*', '', response, flags=re.MULTILINE)
        
        # Clean up multiple asterisks and dashes
        response = re.sub(r'\*{3,}', '---', response)
        response = re.sub(r'-{4,}', '---', response)
        response = re.sub(r'={4,}', '---', response)
        
        # Remove excessive newlines
        response = re.sub(r'\n{3,}', '\n\n', response)
        
        # Clean up list formatting
        response = re.sub(r'^[•✅🔶]\s*', '• ', response, flags=re.MULTILINE)
        
        return response.strip()
    
    def process_message(self, message: str, session_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Main entry point for processing user messages with orchestration - optimized for speed
        """
        start_time = datetime.now()
        
        # Get or create session
        if session_id not in self.sessions:
            session_id = self.create_session(user_id)
        
        session = self.sessions[session_id]
        session.last_activity = datetime.now()
        
        # Use fast intent analysis for speed
        if self._fast_mode:
            intent_analysis = self.analyze_intent_fast(message, session)
        else:
            intent_analysis = self.analyze_intent_advanced(message, session)
        
        # Speed optimization: Prefer single agent unless clearly multi-agent needed
        if self._single_agent_preference and not intent_analysis.get("needs_multiple_agents", False):
            # Route to best single agent
            agent_type = self.route_to_agent(message, intent_analysis)
            result = self.execute_single_agent_workflow(message, agent_type, session_id)
        elif intent_analysis["needs_multiple_agents"] and intent_analysis.get("suggested_workflow"):
            # Execute multi-agent workflow
            result = self.execute_multi_agent_workflow(
                message, 
                intent_analysis["suggested_workflow"], 
                session_id
            )
        else:
            # Fallback to single agent
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
        
        # Calculate total response time
        total_time = (datetime.now() - start_time).total_seconds()
        
        # Prepare response
        response = {
            "response": result["response"],
            "session_id": session_id,
            "agent_used": result["agent_used"],
            "workflow_type": result.get("workflow_type", "single_agent"),
            "conversation_state": session.conversation_state.value,
            "intent_analysis": intent_analysis,
            "timestamp": datetime.now().isoformat(),
            "response_time": total_time,
            "fast_mode": self._fast_mode,
            "cached": result.get("cached", False)
        }
        
        if "individual_responses" in result:
            response["individual_responses"] = result["individual_responses"]
        
        if "agents_available" in result:
            response["agents_available"] = result["agents_available"]
        
        print(f"⚡ Total orchestration time: {total_time:.1f}s")
        
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
    
    def set_performance_mode(self, fast_mode: bool = True, single_agent_preference: bool = True):
        """
        Configure performance settings
        
        Args:
            fast_mode: Enable fast response mode (single agent priority)
            single_agent_preference: Prefer single agent responses over multi-agent workflows
        """
        self._fast_mode = fast_mode
        self._single_agent_preference = single_agent_preference
        
        mode_desc = "fast" if fast_mode else "comprehensive"
        agent_desc = "single-agent priority" if single_agent_preference else "multi-agent workflows"
        
        print(f"⚡ Performance mode set to: {mode_desc} with {agent_desc}")
    
    def clear_cache(self):
        """Clear response cache"""
        cache_size = len(self._response_cache)
        self._response_cache.clear()
        self._cache_hits = 0
        print(f"🧹 Cleared {cache_size} cached responses")
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return {
            "fast_mode": self._fast_mode,
            "single_agent_preference": self._single_agent_preference,
            "cache_size": len(self._response_cache),
            "cache_hits": self._cache_hits,
            "active_sessions": len(self.sessions),
            "agents_preloaded": {
                "asha": self._asha_agent is not None,
                "athena": self._athena_agent is not None,
                "scribe": self._scribe_agent is not None
            }
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
    
    def get_all_agents_status(self):
        """Get status of all agents including their readiness"""
        status = {
            "orchestrator": {
                "status": "ready",
                "sessions_active": len(self.sessions),
                "description": "Coordination agent managing all specialists"
            }
        }
        
        # Check Athena status
        try:
            athena = self._get_athena_agent()
            if athena:
                # Try to get status if method exists
                try:
                    if hasattr(athena, 'get_status'):
                        athena_status = athena.get_status()
                        status["athena"] = {
                            "status": athena_status.get("status", "ready"),
                            "documents_loaded": athena_status.get("documents_loaded", "unknown"),
                            "embeddings_ready": athena_status.get("embeddings_ready", "unknown"),
                            "description": "Legal guidance specialist with document analysis"
                        }
                    else:
                        status["athena"] = {
                            "status": "ready",
                            "description": "Legal guidance specialist"
                        }
                except Exception as e:
                    status["athena"] = {
                        "status": "ready",
                        "description": "Legal guidance specialist",
                        "note": "Status details unavailable"
                    }
            else:
                status["athena"] = {
                    "status": "not_loaded",
                    "description": "Legal guidance specialist (loading on demand)"
                }
        except Exception as e:
            status["athena"] = {
                "status": "error",
                "error": str(e),
                "description": "Legal guidance specialist (error)"
            }
        
        # Check ASHA and Scribe (basic status)
        for agent_name, getter in [("asha", self._get_asha_agent), ("scribe", self._get_scribe_agent)]:
            try:
                agent = getter()
                status[agent_name] = {
                    "status": "ready" if agent else "not_loaded",
                    "description": f"{agent_name.upper()} specialist"
                }
            except Exception as e:
                status[agent_name] = {
                    "status": "error", 
                    "error": str(e),
                    "description": f"{agent_name.upper()} specialist (error)"
                }
        
        return status


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