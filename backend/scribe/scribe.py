#!/usr/bin/env python3
"""
Scribe - AI Documentation & Workflow Assistant
============================================
Specializes in form generation, document creation, and process guidance.
Part of the APEX Legal Assistant Suite.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import re

class ScribeAgent:
    """
    Scribe Agent - Documentation & Workflow Specialist
    
    Features:
    - Generates pre-filled legal forms (maternity leave, transfer requests, etc.)
    - Provides step-by-step workflow guidance
    - Creates document templates and submission packages
    - Tracks document submission processes
    - Offers compliance checking and validation
    """
    
    def __init__(self):
        """Initialize the Scribe agent with API and document templates."""
        print("🔄 Initializing Scribe Documentation Assistant...")
        
        # Load API configuration
        self.api_key = self.load_api_key()
        self.api_available = False
        
        if self.api_key:
            self.api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            self.api_available = self.test_api_connection()
        
        if not self.api_available:
            print("⚠️  API temporarily unavailable - running in offline mode")
        
        # Initialize document templates and workflows
        self.load_document_templates()
        self.load_workflow_guides()
        
        # Conversation management
        self.conversation_history = []
        self.current_session = {
            'start_time': datetime.now(),
            'documents_generated': 0,
            'workflows_accessed': 0,
            'forms_created': 0
        }
        
        print("✅ Scribe Documentation Assistant ready!")
        
    def load_api_key(self) -> Optional[str]:
        """Load Google API key from .env file."""
        try:
            env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
            
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('GOOGLE_API_KEY='):
                            key = line.split('=', 1)[1].strip().strip('"\'')
                            print(f"✅ API key loaded: {key[:12]}...")
                            return key
            
            print("⚠️  No API key found in .env file")
            return None
            
        except Exception as e:
            print(f"❌ Error loading API key: {e}")
            return None
    
    def test_api_connection(self) -> bool:
        """Test if the Gemini API is available."""
        try:
            test_payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": "Hello, please respond with just 'API working'"}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 10
                }
            }
            
            response = requests.post(
                self.api_url, 
                json=test_payload, 
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                print("🌐 API connection successful!")
                return True
            else:
                print(f"⚠️  API returned status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️  API connection failed: {e}")
            return False
    
    def load_document_templates(self):
        """Load document templates for form generation."""
        self.document_templates = {
            'maternity_leave': {
                'title': 'Maternity Leave Application',
                'required_fields': [
                    'employee_name', 'employee_id', 'department', 
                    'designation', 'due_date', 'leave_start_date', 
                    'leave_end_date', 'total_days', 'supervisor_name'
                ],
                'optional_fields': [
                    'medical_certificate', 'previous_leaves', 'contact_during_leave'
                ],
                'template': """
MATERNITY LEAVE APPLICATION

To: The HR Manager / Supervisor
From: {employee_name} (ID: {employee_id})
Department: {department}
Designation: {designation}
Date: {application_date}

Subject: Application for Maternity Leave

Dear Sir/Madam,

I am writing to formally request maternity leave as I am expecting a child. 
My expected due date is {due_date}.

Details of Leave Requested:
- Leave Start Date: {leave_start_date}
- Expected Return Date: {leave_end_date}
- Total Leave Duration: {total_days} days
- Supervisor/Manager: {supervisor_name}

I have attached the medical certificate confirming my pregnancy and due date.
During my leave, I can be contacted at {contact_during_leave} for any urgent matters.

I will ensure all my current responsibilities are properly handed over before 
my leave begins. I am committed to a smooth transition and will coordinate 
with my team and supervisor.

Thank you for your consideration of this request.

Respectfully yours,
{employee_name}
Employee ID: {employee_id}
Date: {application_date}

---
Required Attachments:
□ Medical Certificate
□ Previous Leave Records (if applicable)
□ Contact Information Form
                """,
                'compliance_notes': [
                    'Maternity leave is entitled for 26 weeks (6 months) under Maternity Benefit Act 2017',
                    'Medical certificate from registered practitioner required',
                    'Application should be submitted at least 6 weeks before expected delivery',
                    'Employee entitled to full pay during maternity leave'
                ]
            },
            
            'transfer_request': {
                'title': 'Employee Transfer Request',
                'required_fields': [
                    'employee_name', 'employee_id', 'current_department', 
                    'current_location', 'requested_department', 'requested_location',
                    'reason_for_transfer', 'supervisor_name'
                ],
                'optional_fields': [
                    'family_circumstances', 'skills_relevant', 'preferred_date'
                ],
                'template': """
EMPLOYEE TRANSFER REQUEST

To: The HR Manager / Transfer Committee
From: {employee_name} (ID: {employee_id})
Current Department: {current_department}
Current Location: {current_location}
Date: {application_date}

Subject: Request for Internal Transfer

Dear Sir/Madam,

I am writing to formally request a transfer from my current position to 
another department/location within the organization.

Current Position Details:
- Name: {employee_name}
- Employee ID: {employee_id}
- Department: {current_department}
- Location: {current_location}
- Current Supervisor: {supervisor_name}

Requested Transfer Details:
- Preferred Department: {requested_department}
- Preferred Location: {requested_location}
- Preferred Start Date: {preferred_date}

Reason for Transfer Request:
{reason_for_transfer}

Additional Information:
{family_circumstances}

Relevant Skills and Experience:
{skills_relevant}

I am committed to ensuring a smooth transition and will work with both 
departments to complete any necessary handovers and training.

Thank you for considering my request.

Respectfully yours,
{employee_name}
Employee ID: {employee_id}
Date: {application_date}

---
Required Process:
□ Supervisor Approval
□ Current Department Head Approval  
□ Receiving Department Head Approval
□ HR Final Approval
                """,
                'compliance_notes': [
                    'Transfer requests subject to organizational requirements',
                    'Minimum 6 months service in current role typically required',
                    'Performance evaluation may be considered',
                    'Business justification required for approval'
                ]
            },
            
            'grievance_form': {
                'title': 'Employee Grievance/Complaint Form',
                'required_fields': [
                    'employee_name', 'employee_id', 'department', 
                    'grievance_type', 'incident_date', 'detailed_complaint',
                    'witnesses', 'resolution_sought'
                ],
                'optional_fields': [
                    'supporting_documents', 'previous_attempts', 'urgency_level'
                ],
                'template': """
EMPLOYEE GRIEVANCE FORM

Employee Information:
- Name: {employee_name}
- Employee ID: {employee_id}
- Department: {department}
- Date of Complaint: {application_date}

Grievance Details:
- Type of Grievance: {grievance_type}
- Date of Incident: {incident_date}
- Urgency Level: {urgency_level}

Detailed Description of Grievance:
{detailed_complaint}

Witnesses (if any):
{witnesses}

Previous Attempts to Resolve:
{previous_attempts}

Resolution Sought:
{resolution_sought}

Supporting Documents Attached:
{supporting_documents}

I hereby declare that the information provided above is true and accurate 
to the best of my knowledge.

Employee Signature: _________________
Date: {application_date}

---
For HR Use Only:
Received Date: ___________
Reference No: ___________
Assigned to: ___________
Priority Level: ___________
                """,
                'compliance_notes': [
                    'Grievances must be addressed within 30 days as per policy',
                    'Employee has right to representation during proceedings',
                    'Confidentiality maintained throughout process',
                    'Appeal process available if unsatisfied with resolution'
                ]
            },
            
            'leave_application': {
                'title': 'General Leave Application',
                'required_fields': [
                    'employee_name', 'employee_id', 'department',
                    'leave_type', 'leave_start', 'leave_end', 'total_days', 'reason'
                ],
                'optional_fields': [
                    'emergency_contact', 'work_handover', 'supervisor_approval'
                ],
                'template': """
LEAVE APPLICATION

To: The Manager/Supervisor
From: {employee_name} (ID: {employee_id})
Department: {department}
Date: {application_date}

Subject: Application for {leave_type}

Dear Sir/Madam,

I would like to request {leave_type} for the following period:

Leave Details:
- Type of Leave: {leave_type}
- Start Date: {leave_start}
- End Date: {leave_end}
- Total Days: {total_days}
- Reason: {reason}

Work Handover Arrangements:
{work_handover}

Emergency Contact During Leave:
{emergency_contact}

I have ensured that all urgent tasks will be completed before my leave, 
and have made arrangements for coverage of my responsibilities.

Thank you for your consideration.

Respectfully yours,
{employee_name}
Employee ID: {employee_id}

Supervisor Approval: ________________
Date: ___________
                """,
                'compliance_notes': [
                    'Leave balance should be checked before application',
                    'Advance notice required: 1 day for sick leave, 7 days for planned leave',
                    'Medical certificate required for sick leave >3 days',
                    'Leave without pay if insufficient balance'
                ]
            }
        }
    
    def load_workflow_guides(self):
        """Load workflow guides for different processes."""
        self.workflow_guides = {
            'maternity_leave_process': {
                'title': 'Maternity Leave Application Process',
                'estimated_time': '2-3 weeks',
                'steps': [
                    {
                        'step': 1,
                        'title': 'Medical Consultation',
                        'description': 'Consult with registered medical practitioner',
                        'documents': ['Medical certificate with due date'],
                        'timeline': '6-8 weeks before due date'
                    },
                    {
                        'step': 2,
                        'title': 'Application Preparation',
                        'description': 'Complete maternity leave application form',
                        'documents': ['Filled application form', 'Medical certificate'],
                        'timeline': '6 weeks before due date'
                    },
                    {
                        'step': 3,
                        'title': 'Supervisor Discussion',
                        'description': 'Discuss leave plans with immediate supervisor',
                        'documents': ['Draft application', 'Work handover plan'],
                        'timeline': '5-6 weeks before due date'
                    },
                    {
                        'step': 4,
                        'title': 'HR Submission',
                        'description': 'Submit complete application to HR department',
                        'documents': ['Signed application', 'Medical certificate', 'Supervisor approval'],
                        'timeline': '4-5 weeks before due date'
                    },
                    {
                        'step': 5,
                        'title': 'Approval & Documentation',
                        'description': 'Receive approval and complete documentation',
                        'documents': ['Approval letter', 'Leave schedule', 'Return to work plan'],
                        'timeline': '2-3 weeks before due date'
                    }
                ],
                'contacts': {
                    'HR Department': 'hr@company.com',
                    'Medical Department': 'medical@company.com',
                    'Employee Relations': 'relations@company.com'
                },
                'legal_references': [
                    'Maternity Benefit Act, 2017',
                    'Company Maternity Leave Policy',
                    'Employee Handbook Section 4.2'
                ]
            },
            
            'transfer_process': {
                'title': 'Internal Transfer Request Process',
                'estimated_time': '4-6 weeks',
                'steps': [
                    {
                        'step': 1,
                        'title': 'Self Assessment',
                        'description': 'Evaluate reasons and eligibility for transfer',
                        'documents': ['Performance reviews', 'Skill assessment'],
                        'timeline': 'Before application'
                    },
                    {
                        'step': 2,
                        'title': 'Supervisor Discussion',
                        'description': 'Discuss transfer intentions with current supervisor',
                        'documents': ['Transfer request draft'],
                        'timeline': 'Week 1'
                    },
                    {
                        'step': 3,
                        'title': 'Application Submission',
                        'description': 'Submit formal transfer request to HR',
                        'documents': ['Complete application', 'Supervisor acknowledgment'],
                        'timeline': 'Week 2'
                    },
                    {
                        'step': 4,
                        'title': 'Review Process',
                        'description': 'HR and department heads review application',
                        'documents': ['Additional documentation if requested'],
                        'timeline': 'Week 3-4'
                    },
                    {
                        'step': 5,
                        'title': 'Decision & Transition',
                        'description': 'Receive decision and plan transition if approved',
                        'documents': ['Approval/rejection letter', 'Transition plan'],
                        'timeline': 'Week 5-6'
                    }
                ],
                'contacts': {
                    'HR Transfers': 'transfers@company.com',
                    'Employee Relations': 'relations@company.com'
                },
                'legal_references': [
                    'Company Transfer Policy',
                    'Employee Handbook Section 3.5'
                ]
            },
            
            'grievance_process': {
                'title': 'Employee Grievance Resolution Process',
                'estimated_time': '30 days maximum',
                'steps': [
                    {
                        'step': 1,
                        'title': 'Document the Issue',
                        'description': 'Record details of the grievance with dates and evidence',
                        'documents': ['Incident documentation', 'Supporting evidence'],
                        'timeline': 'Immediately'
                    },
                    {
                        'step': 2,
                        'title': 'Informal Resolution Attempt',
                        'description': 'Try to resolve with immediate supervisor if appropriate',
                        'documents': ['Discussion notes'],
                        'timeline': 'Day 1-7'
                    },
                    {
                        'step': 3,
                        'title': 'Formal Complaint Filing',
                        'description': 'Submit formal grievance form to HR',
                        'documents': ['Completed grievance form', 'Supporting evidence'],
                        'timeline': 'Day 8-10'
                    },
                    {
                        'step': 4,
                        'title': 'Investigation',
                        'description': 'HR investigates the complaint',
                        'documents': ['Additional information if requested'],
                        'timeline': 'Day 11-25'
                    },
                    {
                        'step': 5,
                        'title': 'Resolution',
                        'description': 'Receive investigation results and resolution',
                        'documents': ['Investigation report', 'Resolution plan'],
                        'timeline': 'Day 26-30'
                    }
                ],
                'contacts': {
                    'HR Grievance Officer': 'grievance@company.com',
                    'Employee Ombudsman': 'ombudsman@company.com',
                    'Legal Compliance': 'legal@company.com'
                },
                'legal_references': [
                    'Industrial Disputes Act, 1947',
                    'Company Grievance Policy',
                    'Employee Code of Conduct'
                ]
            }
        }
    
    def generate_document(self, doc_type: str, user_data: Dict[str, Any]) -> str:
        """Generate a document based on template and user data."""
        try:
            if doc_type not in self.document_templates:
                return f"❌ Document type '{doc_type}' not available. Available types: {', '.join(self.document_templates.keys())}"
            
            template = self.document_templates[doc_type]
            
            # Add current date
            user_data['application_date'] = datetime.now().strftime("%B %d, %Y")
            
            # Fill in the template
            filled_document = template['template'].format(**user_data)
            
            # Add compliance information
            compliance_info = "\n\n" + "="*50 + "\n"
            compliance_info += "📋 COMPLIANCE INFORMATION:\n"
            compliance_info += "="*50 + "\n"
            
            for note in template['compliance_notes']:
                compliance_info += f"• {note}\n"
            
            filled_document += compliance_info
            
            self.current_session['documents_generated'] += 1
            self.current_session['forms_created'] += 1
            
            return filled_document
            
        except KeyError as e:
            return f"❌ Missing required field: {e}. Please provide all required information."
        except Exception as e:
            return f"❌ Error generating document: {e}"
    
    def get_workflow_guide(self, process_name: str) -> str:
        """Get step-by-step workflow guide for a process."""
        try:
            if process_name not in self.workflow_guides:
                available = ', '.join(self.workflow_guides.keys())
                return f"❌ Process '{process_name}' not found. Available processes: {available}"
            
            guide = self.workflow_guides[process_name]
            
            workflow_text = f"""
🔄 {guide['title']}
{'='*60}
⏱️  Estimated Timeline: {guide['estimated_time']}

📋 STEP-BY-STEP PROCESS:
"""
            
            for step in guide['steps']:
                workflow_text += f"""
Step {step['step']}: {step['title']}
{'-'*40}
📝 Description: {step['description']}
📄 Required Documents: {', '.join(step['documents'])}
⏰ Timeline: {step['timeline']}
"""
            
            workflow_text += f"""
📞 IMPORTANT CONTACTS:
{'-'*30}
"""
            for contact, info in guide['contacts'].items():
                workflow_text += f"• {contact}: {info}\n"
            
            workflow_text += f"""
📚 LEGAL REFERENCES:
{'-'*30}
"""
            for ref in guide['legal_references']:
                workflow_text += f"• {ref}\n"
            
            self.current_session['workflows_accessed'] += 1
            
            return workflow_text
            
        except Exception as e:
            return f"❌ Error retrieving workflow guide: {e}"
    
    def get_document_requirements(self, doc_type: str) -> str:
        """Get requirements and fields needed for a document type."""
        try:
            if doc_type not in self.document_templates:
                available = ', '.join(self.document_templates.keys())
                return f"❌ Document type '{doc_type}' not found. Available types: {available}"
            
            template = self.document_templates[doc_type]
            
            requirements = f"""
📋 {template['title']} - Requirements
{'='*50}

✅ REQUIRED FIELDS:
"""
            for field in template['required_fields']:
                requirements += f"• {field.replace('_', ' ').title()}\n"
            
            requirements += f"""
🔶 OPTIONAL FIELDS:
"""
            for field in template['optional_fields']:
                requirements += f"• {field.replace('_', ' ').title()}\n"
            
            requirements += f"""
📄 COMPLIANCE NOTES:
{'-'*30}
"""
            for note in template['compliance_notes']:
                requirements += f"• {note}\n"
            
            return requirements
            
        except Exception as e:
            return f"❌ Error retrieving document requirements: {e}"
    
    def query_api(self, user_input: str) -> str:
        """Query the Gemini API for document and workflow assistance."""
        try:
            # Enhanced system prompt for Scribe
            system_prompt = """You are Scribe, an AI Documentation and Workflow Assistant specializing in:

1. **Document Generation**: Creating legal forms, applications, and official documents
2. **Process Guidance**: Providing step-by-step workflows for organizational processes  
3. **Compliance Assistance**: Ensuring documents meet legal and policy requirements
4. **Form Validation**: Checking completeness and accuracy of submitted information

Your expertise includes:
- Indian labor law compliance
- HR processes and procedures
- Official document formatting
- Workflow management
- Form validation and submission guidance

Provide clear, professional, and legally compliant responses. Always prioritize accuracy and include relevant compliance information when discussing legal documents or processes.

Focus on being helpful with document creation, form filling guidance, process workflows, and ensuring all documentation meets required standards."""

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"{system_prompt}\n\nUser Query: {user_input}"}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.3,  # Lower temperature for more consistent, professional responses
                    "topP": 0.8,
                    "topK": 40,
                    "maxOutputTokens": 1024
                }
            }
            
            response = requests.post(
                self.api_url, 
                json=payload, 
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    return content.strip()
                else:
                    return "❌ No response generated from API"
            else:
                return f"❌ API Error {response.status_code}: {response.text}"
                
        except Exception as e:
            return f"❌ API query failed: {e}"
    
    def get_offline_response(self, user_input: str) -> str:
        """Provide offline responses for common document and workflow queries."""
        
        # Convert to lowercase for matching
        query = user_input.lower()
        
        # Document generation queries
        if any(word in query for word in ['maternity', 'pregnancy', 'child', 'baby']):
            return self.get_document_requirements('maternity_leave') + "\n\n" + self.get_workflow_guide('maternity_leave_process')
        
        if any(word in query for word in ['transfer', 'change department', 'relocate', 'move']):
            return self.get_document_requirements('transfer_request') + "\n\n" + self.get_workflow_guide('transfer_process')
        
        if any(word in query for word in ['grievance', 'complaint', 'issue', 'problem', 'harassment']):
            return self.get_document_requirements('grievance_form') + "\n\n" + self.get_workflow_guide('grievance_process')
        
        if any(word in query for word in ['leave', 'vacation', 'absent', 'off']):
            return self.get_document_requirements('leave_application')
        
        # Workflow queries
        if 'workflow' in query or 'process' in query or 'steps' in query:
            return """
🔄 Available Workflow Guides:
════════════════════════════

1. **maternity_leave_process** - Complete maternity leave application process
2. **transfer_process** - Internal transfer request workflow  
3. **grievance_process** - Employee grievance resolution process

Use: 'workflow [process_name]' to get detailed step-by-step guidance.
Example: 'workflow maternity_leave_process'
"""
        
        # Document type queries
        if 'documents' in query or 'forms' in query or 'types' in query:
            return """
📋 Available Document Types:
══════════════════════════

1. **maternity_leave** - Maternity leave application form
2. **transfer_request** - Employee transfer request form
3. **grievance_form** - Employee grievance/complaint form  
4. **leave_application** - General leave application form

Use: 'requirements [document_type]' to see what information is needed.
Example: 'requirements maternity_leave'
"""
        
        # Help queries
        if any(word in query for word in ['help', 'commands', 'what can', 'how to']):
            return """
📚 Scribe Documentation Assistant - Command Guide
═══════════════════════════════════════════════

🔧 **Document Generation Commands:**
• `generate [doc_type]` - Start interactive document creation
• `requirements [doc_type]` - See required fields for a document
• `documents` - List all available document types

🔄 **Workflow Commands:**  
• `workflow [process_name]` - Get step-by-step process guide
• `processes` - List all available workflow guides

📋 **Available Document Types:**
• maternity_leave, transfer_request, grievance_form, leave_application

🔄 **Available Processes:**
• maternity_leave_process, transfer_process, grievance_process

💡 **Examples:**
• "requirements maternity_leave"
• "workflow transfer_process"  
• "generate grievance_form"
• "How do I apply for maternity leave?"
• "What documents do I need for transfer?"

📞 **Session Commands:**
• `summary` - View session statistics
• `reset` - Start new session
• `quit`/`exit` - End session
"""
        
        # Default response for unrecognized queries
        return f"""
📋 I can help you with document generation and workflow guidance!

**Your query:** "{user_input}"

I specialize in:
• Creating official forms and applications
• Providing step-by-step process guidance  
• Document requirements and compliance
• Workflow management

Try asking about:
• "maternity leave application"
• "transfer request process" 
• "grievance procedure"
• "leave application requirements"

Type 'help' for a complete command guide.
"""
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input and provide appropriate response."""
        
        # Add to conversation history
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user_input': user_input,
            'type': 'user'
        })
        
        # Handle special commands
        if user_input.lower() in ['quit', 'exit']:
            return self.end_session()
        
        if user_input.lower() == 'reset':
            return self.reset_session()
        
        if user_input.lower() == 'summary':
            return self.get_session_summary()
        
        if user_input.lower() in ['documents', 'forms']:
            return self.list_available_documents()
        
        if user_input.lower() in ['processes', 'workflows']:
            return self.list_available_workflows()
        
        # Handle command-style inputs
        if user_input.lower().startswith('requirements '):
            doc_type = user_input[13:].strip()
            response = self.get_document_requirements(doc_type)
        elif user_input.lower().startswith('workflow '):
            process_name = user_input[9:].strip()
            response = self.get_workflow_guide(process_name)
        elif user_input.lower().startswith('generate '):
            doc_type = user_input[9:].strip()
            response = f"To generate a {doc_type}, I need the following information:\n\n"
            response += self.get_document_requirements(doc_type)
            response += f"\n\nPlease provide the required information and I'll create the document for you."
        else:
            # Use API if available, otherwise offline response
            if self.api_available:
                response = self.query_api(user_input)
            else:
                response = self.get_offline_response(user_input)
        
        # Add response to conversation history
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'response': response,
            'type': 'assistant'
        })
        
        return response
    
    def list_available_documents(self) -> str:
        """List all available document templates."""
        doc_list = """
📋 Available Document Templates:
════════════════════════════════

"""
        for doc_type, template in self.document_templates.items():
            doc_list += f"📄 **{doc_type}**\n"
            doc_list += f"   Title: {template['title']}\n"
            doc_list += f"   Required Fields: {len(template['required_fields'])}\n"
            doc_list += f"   Optional Fields: {len(template['optional_fields'])}\n"
            doc_list += f"   Use: 'requirements {doc_type}'\n\n"
        
        return doc_list
    
    def list_available_workflows(self) -> str:
        """List all available workflow guides."""
        workflow_list = """
🔄 Available Workflow Guides:
══════════════════════════════

"""
        for process_name, guide in self.workflow_guides.items():
            workflow_list += f"⚙️ **{process_name}**\n"
            workflow_list += f"   Title: {guide['title']}\n"
            workflow_list += f"   Timeline: {guide['estimated_time']}\n"
            workflow_list += f"   Steps: {len(guide['steps'])}\n"
            workflow_list += f"   Use: 'workflow {process_name}'\n\n"
        
        return workflow_list
    
    def get_session_summary(self) -> str:
        """Get summary of current session statistics."""
        duration = datetime.now() - self.current_session['start_time']
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)
        
        return f"""
📊 Scribe Session Summary
═══════════════════════════════

⏱️  Session Duration: {int(hours)}h {int(minutes)}m
💬 Conversations: {len([h for h in self.conversation_history if h['type'] == 'user'])}
📄 Documents Generated: {self.current_session['documents_generated']}
📋 Forms Created: {self.current_session['forms_created']}
🔄 Workflows Accessed: {self.current_session['workflows_accessed']}
🕒 Session Start: {self.current_session['start_time'].strftime('%Y-%m-%d %H:%M:%S')}

💡 Tip: Type 'documents' to see available forms, 'workflows' for processes!
"""
    
    def reset_session(self) -> str:
        """Reset the current session."""
        self.conversation_history = []
        self.current_session = {
            'start_time': datetime.now(),
            'documents_generated': 0,
            'workflows_accessed': 0,
            'forms_created': 0
        }
        
        return """
🔄 Session Reset Complete!
═══════════════════════════════

New session started. Previous conversation history cleared.
Ready to assist with document generation and workflow guidance!

Type 'help' for available commands.
"""
    
    def end_session(self) -> str:
        """End the current session."""
        summary = self.get_session_summary()
        
        end_message = f"""
{summary}

👋 Thank you for using Scribe Documentation Assistant!
═════════════════════════════════════════════════

Your documents and workflows are ready when you need them.
Remember to save any generated documents for your records.

Have a productive day! 📋✨
"""
        return end_message
    
    def run(self):
        """Main interactive loop for the Scribe agent."""
        print("""
📋 Welcome to Scribe - AI Documentation Assistant 📋
══════════════════════════════════════════════════════
I help create legal forms, applications, and guide you through workflows.
Type 'quit' or 'exit' to end our session.
Type 'reset' to start a new conversation.
Type 'summary' to see session statistics.
Type 'help' to see available commands.
══════════════════════════════════════════════════════
""")
        
        while True:
            try:
                user_input = input("\n📝 You: ").strip()
                
                if not user_input:
                    continue
                
                print("\n🤖 Scribe:")
                response = self.process_user_input(user_input)
                print(response)
                
                if user_input.lower() in ['quit', 'exit']:
                    break
                    
            except KeyboardInterrupt:
                print("\n\n👋 Session ended by user. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'help' for assistance.")

def main():
    """Main entry point for the Scribe Documentation Assistant."""
    try:
        scribe = ScribeAgent()
        scribe.run()
    except Exception as e:
        print(f"❌ Failed to start Scribe agent: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
