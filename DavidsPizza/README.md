Project Structure

DavidsPizza/
│
├── api/ # Backend (Node + Express)
│ ├── server.js # API server
│ ├── pizza.sqlite # SQLite database
│ └── package.json
│
├── dominos/ # Frontend (React)
│ ├── src/
│ │ ├── routes/ # Route-based pages (lazy loaded)
│ │ ├── components/ # UI components (Pizza, Cart, Modal, etc.)
│ │ ├── contexts.js # Global state management
│ │ └── App.jsx
│ └── package.json

Features
• 🍕 Browse available pizzas
• ⭐ Pizza of the Day feature
• 🛒 Add items to cart and place orders
• 📜 View past orders
• ⚡ Fast client-side routing with lazy loading
• 🗄️ Persistent storage using SQLite
• 🔗 REST API backend

Tech Stack

Frontend
• React
• React Router
• Context API
• Vite

Backend
• Node.js
• Express
• SQLite

Setup Instructions

Clone the repository

git clone <your-repo-url>
cd DavidsPizza

Run the Backend (API)

cd api
npm install
node server.js

Run the Frontend (React App)

cd dominos
npm install
npm run dev

Using the App 1. Start both the backend and frontend servers 2. Open the frontend URL in your browser 3. Browse pizzas, add items to your cart, and place orders 4. Ensure the backend stays running for data to load properly

⸻

🧪 Notes
• The backend must be running for the frontend to function correctly
• SQLite database (pizza.sqlite) is included for persistence
• This project is intended for learning and demonstration purposes

⸻

📜 License

This project is for educational use.
Feel free to explore, modify, and learn from it.
