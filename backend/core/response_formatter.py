#!/usr/bin/env python3
"""
Response Formatter - Convert markdown-style responses to HTML for better readability
"""

import re

def format_response_for_frontend(response: str) -> str:
    """
    Convert markdown-style formatting to HTML for better frontend display
    
    Args:
        response (str): Raw response with markdown formatting
        
    Returns:
        str: Formatted response with HTML
    """
    if not response:
        return response
    
    # Convert **bold text** to <strong>bold text</strong>
    response = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', response)
    
    # Convert *italic text* to <strong>italic text</strong> (treating as bold for better visibility)
    response = re.sub(r'\*(.*?)\*', r'<strong>\1</strong>', response)
    
    # Format numbered lists (1. 2. 3. etc.) to be on separate lines with better spacing
    response = re.sub(r'(\d+\.\s+)', r'<br><br>\1', response)
    
    # Format bullet points with dashes or asterisks
    response = re.sub(r'^[\-\*]\s+', r'<br>• ', response, flags=re.MULTILINE)
    
    # Clean up multiple consecutive <br> tags
    response = re.sub(r'(<br>\s*){3,}', r'<br><br>', response)
    
    # Remove leading <br> if it exists
    response = re.sub(r'^(<br>\s*)+', '', response)
    
    return response.strip()

def format_legal_response(response: str) -> str:
    """
    Format legal responses with proper structure and emphasis
    
    Args:
        response (str): Raw legal response
        
    Returns:
        str: Formatted legal response
    """
    formatted = format_response_for_frontend(response)
    
    # Add extra formatting for legal terms
    legal_terms = [
        'harassment', 'discrimination', 'legal rights', 'documentation', 
        'HR department', 'legal counsel', 'complaint', 'violation',
        'employment law', 'workplace policy', 'evidence', 'witness'
    ]
    
    for term in legal_terms:
        # Make legal terms bold (case insensitive)
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        formatted = pattern.sub(f'<strong>{term}</strong>', formatted)
    
    return formatted

def format_emotional_response(response: str) -> str:
    """
    Format emotional support responses with empathy and clarity
    
    Args:
        response (str): Raw emotional support response
        
    Returns:
        str: Formatted emotional support response
    """
    formatted = format_response_for_frontend(response)
    
    # Add gentle emphasis to supportive phrases
    supportive_phrases = [
        'you are not alone', 'here to support', 'courage to reach out',
        'immense courage', 'support you', 'here to listen'
    ]
    
    for phrase in supportive_phrases:
        pattern = re.compile(re.escape(phrase), re.IGNORECASE)
        formatted = pattern.sub(f'<strong>{phrase}</strong>', formatted)
    
    return formatted