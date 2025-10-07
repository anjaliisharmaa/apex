#!/usr/bin/env python3
"""
ASHA Agent - AI Support and Help Assistant
This version uses direct HTTP requests to Google's Gemini API for maximum compatibility
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

class AshaAgent:
    """
    ASHA (AI Support and Help Assistant) - A compassionate AI agent for support and guidance
    """
    
    def __init__(self):
        # Load API key from environment or file
        self.api_key = self.load_api_key()
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in .env file or environment variables")
        
        # Gemini API endpoint
        self.api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={self.api_key}"
        
        # System prompt for ASHA
        self.system_prompt = """
        You are ASHA (AI Support and Help Assistant), a compassionate and knowledgeable AI agent designed to provide:
        
        1. **Emotional Support**: Listen with empathy and provide comfort during difficult times
        2. **Resource Guidance**: Help users find appropriate resources, services, and support systems
        3. **Crisis Support**: Recognize crisis situations and provide immediate guidance and resources
        4. **Information**: Provide accurate, helpful information on various topics
        5. **Practical Assistance**: Help with problem-solving and decision-making
        
        **Your personality traits:**
        - Empathetic and understanding
        - Non-judgmental and supportive
        - Professional yet warm
        - Culturally sensitive
        - Solution-oriented
        
        **Guidelines:**
        - Always prioritize user safety and well-being
        - Provide appropriate resources when needed
        - Maintain confidentiality and privacy
        - Be clear about your limitations as an AI
        - Encourage professional help when appropriate
        - Use inclusive and accessible language
        
        **Crisis situations:**
        If someone mentions suicide, self-harm, or immediate danger:
        - Take it seriously
        - Provide crisis helpline numbers
        - Encourage immediate professional help
        - Don't try to provide therapy or professional counseling
        
        Remember: You are here to support, guide, and provide resources, but you are not a replacement for professional mental health services, medical care, or emergency services.
        
        Please respond in a caring, helpful manner to the following message:
        """
        
        self.conversation_history = []
    
    def load_api_key(self):
        """Load API key from environment or .env file"""
        # First try environment variable
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            return api_key
        
        # Try to load from .env file
        env_file_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_file_path):
            with open(env_file_path, 'r') as f:
                for line in f:
                    if line.startswith('GOOGLE_API_KEY='):
                        return line.split('=', 1)[1].strip().strip('"\'')
        
        return None
    
    def get_response(self, user_message: str) -> str:
        """
        Generate a response from ASHA based on user input
        
        Args:
            user_message (str): The user's message
            
        Returns:
            str: ASHA's response
        """
        try:
            # Prepare the request payload
            prompt = self.system_prompt + "\n\nUser message: " + user_message
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }
            
            # Convert to JSON
            data = json.dumps(payload).encode('utf-8')
            
            # Create request
            req = urllib.request.Request(
                self.api_url,
                data=data,
                headers={
                    'Content-Type': 'application/json',
                }
            )
            
            # Make the request
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode())
            
            # Extract the response text
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                content = response_data['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    asha_response = content['parts'][0]['text']
                    
                    # Add to conversation history
                    self.conversation_history.append({
                        "role": "user",
                        "content": user_message,
                        "timestamp": datetime.now().isoformat()
                    })
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": asha_response,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    return asha_response
            
            return "I apologize, but I'm having trouble generating a response right now. Please try again."
            
        except Exception as e:
            error_response = f"I apologize, but I'm experiencing some technical difficulties right now. Error: {str(e)}"
            return error_response
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
        return "Conversation history has been reset. How can I help you today?"
    
    def get_conversation_summary(self):
        """Get a summary of the current conversation"""
        if not self.conversation_history:
            return "No conversation history available."
        
        summary = f"Conversation started: {self.conversation_history[0]['timestamp']}\n"
        summary += f"Total messages: {len(self.conversation_history)}\n"
        summary += f"Last message: {self.conversation_history[-1]['timestamp']}"
        
        return summary

def main():
    """
    Main function to run ASHA in interactive mode
    """
    print("🌟 Welcome to ASHA - AI Support and Help Assistant 🌟")
    print("=" * 50)
    print("I'm here to provide support, guidance, and resources.")
    print("Type 'quit' or 'exit' to end our conversation.")
    print("Type 'reset' to start a new conversation.")
    print("Type 'summary' to see conversation statistics.")
    print("=" * 50)
    
    try:
        # Initialize ASHA
        asha = AshaAgent()
        print("✅ ASHA is ready to help!")
        
        while True:
            print("\n" + "-" * 30)
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("\nASHA: Take care! Remember, I'm here whenever you need support. 💙")
                break
            
            elif user_input.lower() == 'reset':
                response = asha.reset_conversation()
                print(f"\nASHA: {response}")
                continue
            
            elif user_input.lower() == 'summary':
                summary = asha.get_conversation_summary()
                print(f"\nConversation Summary:\n{summary}")
                continue
            
            elif not user_input:
                print("\nASHA: I'm here to listen. Please share what's on your mind.")
                continue
            
            # Get response from ASHA
            print("\nASHA: ", end="", flush=True)
            response = asha.get_response(user_input)
            print(response)
            
    except KeyboardInterrupt:
        print("\n\nASHA: Take care! Remember, support is always available when you need it. 💙")
    except Exception as e:
        print(f"\n❌ Error initializing ASHA: {e}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main()

def main():
    """
    Main function to run ASHA in interactive mode
    """
    print("🌟 Welcome to ASHA - AI Support and Help Assistant 🌟")
    print("=" * 50)
    print("I'm here to provide support, guidance, and resources.")
    print("Type 'quit' or 'exit' to end our conversation.")
    print("Type 'reset' to start a new conversation.")
    print("Type 'summary' to see conversation statistics.")
    print("=" * 50)
    
    try:
        # Initialize ASHA
        asha = AshaAgent()
        print("✅ ASHA is ready to help!")
        
        while True:
            print("\n" + "-" * 30)
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("\nASHA: Take care! Remember, I'm here whenever you need support. 💙")
                break
            
            elif user_input.lower() == 'reset':
                response = asha.reset_conversation()
                print(f"\nASHA: {response}")
                continue
            
            elif user_input.lower() == 'summary':
                summary = asha.get_conversation_summary()
                print(f"\nConversation Summary:\n{summary}")
                continue
            
            elif not user_input:
                print("\nASHA: I'm here to listen. Please share what's on your mind.")
                continue
            
            # Get response from ASHA
            print("\nASHA: ", end="", flush=True)
            response = asha.get_response(user_input)
            print(response)
            
    except KeyboardInterrupt:
        print("\n\nASHA: Take care! Remember, support is always available when you need it. 💙")
    except Exception as e:
        print(f"\n❌ Error initializing ASHA: {e}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main()
