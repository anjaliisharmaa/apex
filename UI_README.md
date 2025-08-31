# Project Apex: Complete UI/UX Specification

This document provides comprehensive specifications for the user interface (UI) structure, features, and pages for Project Apex. The UI will be built using Next.js with TailwindCSS and is designed to be clean, professional, and trustworthy, ensuring user safety and confidentiality.

## 1. Design System & Core UI Principles

### 1.1. Color Scheme
- **Primary Colors**: 
  - Deep Blue (#1e3a8a) - Trust, security
  - Soft Teal (#14b8a6) - Calm, support
  - Warm Purple (#7c3aed) - Empowerment
- **Status Colors**:
  - Success: #10b981 (Green)
  - Warning: #f59e0b (Amber) 
  - Error: #ef4444 (Red)
  - Info: #3b82f6 (Blue)
- **Neutral Colors**:
  - Background: #f8fafc (Light gray)
  - Text Primary: #1f2937 (Dark gray)
  - Text Secondary: #6b7280 (Medium gray)
  - Border: #e5e7eb (Light border)

### 1.2. Typography
- **Font Family**: Inter (clean, professional)
- **Heading Sizes**: text-3xl, text-2xl, text-xl, text-lg
- **Body Text**: text-base (16px)
- **Small Text**: text-sm (14px)

### 1.3. Core Principles
- **Confidentiality**: All sensitive areas have visual security indicators
- **Clarity**: Maximum 7±2 items per screen, clear hierarchy
- **Accessibility**: WCAG 2.1 AA compliance, keyboard navigation
- **Empowerment**: Positive, encouraging language and visual feedback

## 2. Global Components

### 2.1. Header Component
**Location**: Present on all authenticated pages
**Elements**:
- Logo (left): "Apex" with tagline "Your Confidential Companion"
- Navigation (center): Dashboard, Chat, Cases, Forms, Resources
- User Actions (right):
  - Anonymous Mode Toggle (switch with indicator)
  - Notifications Bell (with red dot for new items)
  - User Avatar/Menu Dropdown
  - Emergency SOS Button (red, always visible)

### 2.2. Navigation Menu
**Desktop**: Horizontal top navigation
**Mobile**: Hamburger menu with slide-out drawer
**Items**: Each nav item shows active state with underline/background

### 2.3. Emergency SOS Button 🆘
**Design**: Fixed position floating button (bottom-right corner)
**States**: 
- Normal: Red circle with white SOS text
- Hover: Slightly larger with shadow
- Click: Shows confirmation modal
**Modal Content**:
- "Are you in immediate danger?"
- "Call Security" button (links to helpline)
- "Anonymous Report" button
- "Cancel" button

### 2.4. Anonymous Mode Toggle
**Design**: Toggle switch with lock icon
**States**:
- Off: Gray background, "Standard Mode"
- On: Purple background, "Anonymous Mode Active"
**Behavior**: When on, shows persistent banner and changes chat interface colors

## 3. Detailed Page Specifications

### 3.1. Login Page (/login)

**Layout**: Centered card on gradient background
**Elements**:
- **Header**: Apex logo and tagline
- **Login Form**:
  - Email field (required, validation)
  - Password field (required, show/hide toggle)
  - "Remember me" checkbox
  - "Login" button (full width, disabled until valid)
  - "Forgot Password?" link
- **MFA Section** (appears after initial login):
  - "Enter verification code sent to your phone"
  - 6-digit OTP input (auto-focus, auto-submit)
  - "Resend Code" link (disabled for 60s countdown)
  - "Verify" button
- **Footer**: "Need help? Contact Support"

**Validation**:
- Real-time email format validation
- Password strength indicator
- Error messages below each field
- Loading states during submission

### 3.2. Dashboard Page (/dashboard)

**Layout**: Grid layout (2x2 on desktop, 1x4 on mobile)
**Header Section**:
- Welcome message: "Welcome back, [Name]" or "Welcome, Anonymous User"
- Quick stats: "You have X active cases, Y new notifications"

**Main Cards** (each 300px wide, 200px tall):

#### 3.2.1. Ask a Question Card
- **Icon**: Chat bubble with question mark
- **Title**: "Ask a Question"
- **Description**: "Get instant answers about policies, rights, and procedures"
- **Button**: "Start Conversation"
- **Badge**: "24/7 Available" (green)

#### 3.2.2. Generate a Form Card
- **Icon**: Document with pen
- **Title**: "Generate a Form"
- **Description**: "Create official documents and applications"
- **Quick Actions**: 
  - "Maternity Leave" button
  - "Transfer Request" button
  - "View All Forms" link

#### 3.2.3. Track My Cases Card
- **Icon**: Clipboard with checkmark
- **Title**: "Track My Cases"
- **Description**: "Monitor your submissions and requests"
- **Stats**: "X Active, Y Completed"
- **Button**: "View All Cases"
- **Recent**: Shows 2 most recent case titles

#### 3.2.4. Resource Hub Card
- **Icon**: Book/Library
- **Title**: "Resource Hub"
- **Description**: "Policies, articles, and success stories"
- **Quick Links**:
  - "POSH Act Guide"
  - "Maternity Benefits"
  - "Recent Updates"

**Sidebar** (right side, 300px wide):
- **Recent Activity** section showing last 5 actions
- **Notifications** panel with unread items
- **Quick Tips** rotating helpful information

### 3.3. Chat Page (/chat)

**Layout**: Full-height split layout
**Left Sidebar** (300px, collapsible):
- **Header**: "Conversations" with new chat button
- **Anonymous Toggle**: Prominent toggle switch
- **Chat History**: List of previous conversations with timestamps
- **Filters**: "All", "Anonymous", "Recent"

**Main Chat Area**:
- **Header**: Shows current agent name and status
- **Messages Container** (scrollable):
  - User messages (right-aligned, blue background)
  - AI messages (left-aligned, gray background)
  - System messages (centered, small text)
  - Interactive buttons (when AI provides options)
  - File attachments (with download/preview)
  - Typing indicators

**Message Input Area**:
- **Text Area**: Auto-expanding, placeholder text
- **Attachment Button**: Paper clip icon for file upload
- **Send Button**: Arrow icon, disabled when empty
- **Voice Note Button**: Microphone icon (future feature)

**Interactive Elements**:
- **Quick Actions Bar**: Common questions as clickable pills
- **Suggestion Chips**: AI-generated follow-up questions
- **Action Buttons**: "Generate Form", "Schedule Call", etc.

### 3.4. Cases Page (/cases)

**Layout**: Table view with filters and search
**Header Section**:
- **Title**: "My Cases"
- **Filters**: Dropdown for status (All, Active, Completed, etc.)
- **Search Bar**: Search by case title or reference number
- **New Case Button**: "Create New Case"

**Cases Table**:
- **Columns**: Reference #, Title, Type, Status, Created Date, Last Update, Actions
- **Status Indicators**: Color-coded badges
- **Actions**: View, Edit, Download, Delete (with confirmations)
- **Pagination**: Page numbers with items per page selector

**Case Status Options**:
- Draft (gray)
- Submitted (blue)
- Under Review (yellow)
- Additional Info Required (orange)
- Approved (green)
- Rejected (red)
- Completed (purple)

### 3.5. Individual Case Page (/cases/[id])

**Layout**: Two-column layout
**Left Column** (main content):
- **Case Header**: Title, reference number, current status
- **Timeline**: Vertical timeline showing all case updates
- **Documents Section**: List of all related documents
- **Comments/Notes**: Internal notes and communications
- **Actions Panel**: Edit, Submit, Withdraw, etc.

**Right Column** (sidebar):
- **Case Summary**: Key details in a card
- **Status Progress**: Visual progress indicator
- **Contact Information**: Relevant department/officer
- **Related Resources**: Links to relevant policies

### 3.6. Forms Page (/forms)

**Layout**: Category-based grid
**Header**:
- **Title**: "Document Generator"
- **Search Bar**: Search forms by name or category
- **Filter**: Dropdown for categories

**Form Categories**:
#### 3.6.1. Leave Applications
- Maternity Leave Application
- Child Care Leave Application
- Medical Leave Application
- Personal Leave Application

#### 3.6.2. Transfer Requests
- Spouse Ground Transfer
- Medical Ground Transfer
- General Transfer Request
- Posting Preference Form

#### 3.6.3. Grievance Forms
- Harassment Complaint (with anonymous option)
- Workplace Issue Report
- Policy Clarification Request
- Suggestion/Feedback Form

#### 3.6.4. Administrative Forms
- Address Change Notification
- Emergency Contact Update
- Dependent Information Update
- Salary Certificate Request

**Each Form Card Contains**:
- Form icon and title
- Brief description
- Estimated completion time
- "Start Form" button
- "Preview Sample" link

### 3.7. Form Generation Process (/forms/[type])

**Layout**: Multi-step wizard
**Progress Indicator**: Step numbers and completion percentage
**Steps**:
1. **Information Gathering**: Form fields with validation
2. **Document Upload**: Drag-and-drop area for supporting documents
3. **Review & Preview**: Generated document preview
4. **Submission Options**: Submit now, save as draft, or download

**Form Fields** (common patterns):
- Text inputs with labels and help text
- Date pickers for dates
- Dropdown selections for predefined options
- File upload areas with progress indicators
- Radio buttons for single choices
- Checkboxes for multiple selections
- Rich text areas for detailed descriptions

### 3.8. Resources Page (/resources)

**Layout**: Three-column layout
**Left Sidebar** (200px):
- **Categories**:
  - Policies & Guidelines
  - Legal Rights
  - Success Stories
  - FAQs
  - News & Updates

**Main Content Area**:
- **Search Bar**: Full-text search across all resources
- **Featured Content**: Highlighted articles/updates
- **Resource Cards**: Each showing title, summary, category, and read time
- **Pagination**: Load more or page-based navigation

**Right Sidebar** (200px):
- **Quick Links**: Most accessed resources
- **Recent Updates**: Latest additions
- **Bookmark**: Save articles for later

### 3.9. Profile Page (/profile)

**Layout**: Tabbed interface
**Tabs**:
#### 3.9.1. Personal Information
- Name, email, phone (with edit capability)
- Organization and designation
- Emergency contacts
- Communication preferences

#### 3.9.2. Security Settings
- Change password form
- Two-factor authentication setup
- Active sessions view
- Login history

#### 3.9.3. Privacy Settings
- Data retention preferences
- Anonymous mode default settings
- Notification preferences
- Account deletion option

#### 3.9.4. Support
- Contact support form
- FAQ section
- User guide links
- System status

## 4. Responsive Design Specifications

### 4.1. Desktop (1024px+)
- Full multi-column layouts
- Hover states and tooltips
- Keyboard shortcuts displayed

### 4.2. Tablet (768px - 1023px)
- Simplified two-column layouts
- Touch-friendly buttons (44px minimum)
- Collapsible sidebars

### 4.3. Mobile (320px - 767px)
- Single-column layouts
- Bottom navigation instead of top
- Swipe gestures for navigation
- Condensed information display

## 5. Interaction Patterns

### 5.1. Loading States
- Skeleton screens for content loading
- Progress bars for file uploads
- Spinner animations for quick actions
- "Typing..." indicators in chat

### 5.2. Error Handling
- Inline validation messages
- Toast notifications for system errors
- Retry buttons for failed actions
- Offline state indicators

### 5.3. Confirmation Dialogs
- Delete confirmations with item details
- Form submission confirmations
- Navigation away from unsaved forms
- Anonymous mode toggle confirmations

### 5.4. Accessibility Features
- Focus indicators for keyboard navigation
- Screen reader friendly labels
- High contrast mode option
- Text size adjustment controls

## 6. Security Indicators

### 6.1. Visual Security Cues
- Lock icons for secure sections
- SSL certificate indicator
- Session timeout warnings
- Anonymous mode visual changes

### 6.2. Data Handling
- Clear indication of what data is being collected
- Options to download personal data
- Clear deletion confirmations
- Privacy policy links throughout

This comprehensive specification provides all the necessary details for implementing the frontend application with consistent user experience and complete functionality.
