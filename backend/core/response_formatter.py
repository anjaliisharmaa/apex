#!/usr/bin/env python3
"""
Response Formatter - Convert markdown-style responses to HTML for better readability
"""

import re

def format_response_for_frontend(response: str) -> str:
    """
    Convert markdown-style formatting to clean text for better frontend display
    
    Args:
        response (str): Raw response with markdown formatting
        
    Returns:
        str: Formatted response with clean text formatting
    """
    if not response:
        return response
    
    # First, protect existing bullet points by marking them
    response = response.replace('•', '###BULLET###')
    
    # Convert **bold text** to plain text (remove double asterisks)
    response = re.sub(r'\*\*(.*?)\*\*', r'\1', response)
    
    # Convert *italic text* to plain text only if it's clearly italic markup (not bullet points)
    # Only match asterisks that have text on both sides without spaces
    response = re.sub(r'(\w)\*(\w[^*]*?)\*(\w)', r'\1\2\3', response)
    
    # Convert standalone asterisks used as bullet points to proper bullets
    response = re.sub(r'\s*\*\s+([^*\n]+?)(?=\s*[\n*]|$)', r'\n    • \1', response)
    
    # Restore bullet points and ensure proper formatting
    response = response.replace('###BULLET###', '•')
    
    # Format numbered lists (1. 2. 3. etc.) to be on separate lines
    response = re.sub(r'(\d+\.\s+)', r'\n\n\1', response)
    
    # Ensure bullet points are on new lines when they follow text
    response = re.sub(r'([.:\w])\s*•\s*', r'\1\n\n• ', response)
    
    # Clean up multiple spaces and line breaks
    response = re.sub(r'\n{4,}', r'\n\n\n', response)
    response = re.sub(r'[ \t]+', r' ', response)
    
    # Remove leading/trailing whitespace
    response = response.strip()
    
    return response

def format_legal_response(response: str) -> str:
    """
    Format legal responses with proper structure and clean text
    
    Args:
        response (str): Raw legal response
        
    Returns:
        str: Formatted legal response with clean text
    """
    formatted = format_response_for_frontend(response)
    
    # No HTML formatting - just clean text formatting
    return formatted

def format_emotional_response(response: str) -> str:
    """
    Format emotional support responses with empathy and clear text formatting
    
    Args:
        response (str): Raw emotional support response
        
    Returns:
        str: Formatted emotional support response with clean text
    """
    formatted = format_response_for_frontend(response)
    
    # No HTML formatting - just clean text formatting
    return formatted