# CAD File Manager

The CAD File Manager is a full-stack web application designed to help users upload, organize, and manage CAD files in a structured and user-friendly way. It supports authentication, file tracking, and job-based processing to improve organization and workflow visibility.

## Features
- User registration and login
- Upload and manage CAD files
- View file details and metadata
- Track processing jobs related to uploaded files
- Organized file listing interface
- REST API-based backend communication

## Project Structure
cad-file-manager/
│
├── frontend/          # React (Vite) frontend
│   ├── src/
│   │   ├── pages/     # Upload, Files, Jobs, FileDetail, Login, Register
│   │   └── services/  # API service layer (Axios)
│   └── package.json
│
├── backend/           # Node.js / Express backend
│   ├── node_modules/
│   ├── routes/
│   ├── controllers/
│   └── package.json

## Tech Stack

### Frontend
- React (Vite)
- JavaScript (ES6+)
- HTML & CSS
- Axios

### Backend
- Node.js
- Express
- MongoDB
- JWT-based authentication

## How It Works
1. Users register or log in to the application.
2. Authenticated users can upload CAD files through the web interface.
3. Uploaded files are stored and tracked with metadata in the database.
4. Users can view uploaded files, inspect file details, and monitor processing jobs.
5. The frontend communicates with the backend using REST APIs.

## Setup Instructions

### Prerequisites
- Node.js
- npm
- MongoDB

### Backend Setup
cd backend
npm install
npm run dev

### Frontend Setup
cd frontend
npm install
npm run dev
