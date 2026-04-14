# DBMS Project

This repository contains the Database Management System project, including both the React frontend and Node.js/Express backend. This README primarily serves as a guide for developers working on the frontend application.

## 📁 Repository Structure
- `frontend/` - React frontend powered by Vite
- `backend/` - Node.js Express server
- `DBMS Report.docx` - Full project report

---

## 🎨 Frontend Developer Guide

The frontend is a modern single-page application built using **React 19** and bundled with **Vite** for blazing fast performance.

### Tech Stack
- **Framework**: React 19 
- **Bundler**: Vite
- **Routing**: React Router DOM v7
- **Icons**: Lucide React
- **Data Visualization**: Recharts

### 🚀 Getting Started

#### Prerequisites
- Node.js (v18 or higher recommended)
- npm (Node Package Manager)

#### 1. Installation
Navigate into the `frontend` directory and install the dependencies:
```bash
cd frontend
npm install
```

#### 2. Running the Development Server
Start the Vite development server with Hot Module Replacement (HMR):
```bash
npm run dev
```
The application will typically be available at `http://localhost:5173`.

### 📜 Available Scripts

Inside the `frontend` directory, you can run:

- `npm run dev` - Starts the local development server.
- `npm run build` - Builds the app for production to the `dist` folder.
- `npm run preview` - Locally preview the production build.
- `npm run lint` - Runs ESLint to catch syntax and style errors.

### 🧩 Frontend Architecture & Navigation

The frontend code lives in `frontend/src/`. Here's a quick map:

- **`App.jsx`**: The root component where the React Router layout is typically defined.
- **`main.jsx`**: The entry point where the React app binds to the DOM (`index.html`).
- **`index.css` & `App.css`**: Global styles and layout definitions.
- **`assets/`**: Static assets like SVGs and images used within the React components.

### 🔌 Connecting to the Backend
When building features, assume the backend runs on a separate port (e.g., `http://localhost:5000`). 
Ensure that your API calls in React components reference the correct backend URL. If you create environmental variables, store them in a `.env` file within the `frontend` directory (using the `VITE_` prefix, e.g., `VITE_API_URL`).

---
*Happy coding! Feel free to refer to the included DBMS report for exact schema and data requirements.*
