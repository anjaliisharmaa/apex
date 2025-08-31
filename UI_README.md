# Project Apex: UI/UX Structure

This document details the user interface (UI) structure, features, and pages for Project Apex. The UI will be built using Next.js and is designed to be clean, professional, and trustworthy, ensuring user safety and confidentiality.

## 1. Core UI Principles

*   **Confidentiality**: The design must inspire trust. All interactions should feel private and secure.
*   **Clarity**: The interface should be intuitive, with clear navigation and simple language.
*   **Accessibility**: The UI must be accessible to users with varying levels of digital literacy.
*   **Empowerment**: The design should empower users by making information and tools easy to access.

## 2. Key UI Components & Features

### 2.1. Secure & Simple Login
*   **Functionality**: Multi-factor authentication (MFA) to ensure data privacy and secure access.
*   **Components**: Login form with fields for credentials and a second factor (e.g., OTP).

### 2.2. Main Dashboard
This is the landing page after a user logs in. It provides quick access to all major functions.
*   **Layout**: A clean, card-based layout.
*   **Components**:
    *   **`Ask a Question` Card**: A prominent card that directs the user to the primary conversational AI interface.
    *   **`Generate a Form` Card**: A shortcut to a list of the most frequently needed applications (e.g., Child Care Leave, Transfer Request).
    *   **`Track My Cases` Card**: Leads to a confidential log of all submitted requests and their current status.
    *   **`Resource Hub` Card**: Opens a library of policies, articles, and success stories.

### 2.3. Conversational AI Interface
The core of the user interaction, designed like a modern messaging app.
*   **Layout**: A two-panel layout with a chat history sidebar (optional) and the main chat window.
*   **Components**:
    *   **Message Bubbles**: For user queries and AI responses.
    *   **Input Bar**: With a text area for typing, a send button, and a secure file upload button.
    *   **Interactive Buttons**: The AI can present options as buttons (e.g., "Learn my rights," "File a complaint") to guide the conversation.

### 2.4. Document & Case Center
A secure vault for all user-specific documents and cases.
*   **Layout**: A table or list view of all cases, which can be clicked to show details.
*   **Features**:
    *   **Case View**: A detailed view of a single case, showing a timeline of events, status updates, and all associated documents.
    *   **Document Management**: Users can view, edit, and download all generated documents.
    *   **Status Tracking**: Clear visual indicators for case status (e.g., "Submitted," "In Review," "Resolved").

### 2.5. Anonymous Mode
A critical feature for handling sensitive queries.
*   **Functionality**: A clearly visible toggle switch (e.g., in the header or chat interface) that allows the user to ask questions without associating the query with their personal profile.
*   **Visual Cue**: When active, the UI should change slightly (e.g., a different color theme or a persistent banner) to indicate that Anonymous Mode is on.

### 2.6. Emergency SOS Button 🆘
For immediate assistance.
*   **Design**: A discreet but easily accessible button, perhaps in the header or a floating action button.
*   **Functionality**: On click, it should present a confirmation dialog and then provide instant access to security helplines, quick-reporting features, or pre-defined emergency contacts.

## 3. Page Structure

The application will be structured into the following pages/routes:

*   **/login**: The secure login page.
*   **/dashboard**: The main dashboard, the default page after login.
*   **/chat**: The conversational AI interface where users interact with the Apex agents.
*   **/cases**: The Case Center, listing all of the user's active and past cases.
    *   **/cases/[id]**: A dynamic route to show the detailed view for a specific case.
*   **/forms**: A page dedicated to starting the document generation process.
*   **/resources**: The Resource Hub, containing a searchable library of documents, policies, and articles.
*   **/profile**: User profile and settings page.
