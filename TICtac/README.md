# Tic-Tac-Toe (TICtac) ❌⭕️

A simple and interactive **Tic-Tac-Toe game built with React**.  
The app supports turn-based play, win detection, draw detection, move history, and game reset, all wrapped in a clean, centered UI.

---

## 📌 Description

This project is a classic Tic-Tac-Toe implementation designed to practice React fundamentals such as state management, component composition, and conditional rendering. The game tracks every move, allows players to jump back in time, and correctly detects wins and draws.

---

## ✨ Features

- Two-player turn-based gameplay (X and O)
- Automatic win detection
- **Draw detection** when the board is full
- Move history with time-travel (jump to previous moves)
- Reset button to restart the game
- Centered, modern UI with hover effects
- Responsive layout for smaller screens

---

## 🛠️ Tech Stack

- **React**
- **JavaScript (ES6+)**
- **Vite**
- **HTML & CSS**

---

## 📂 Project Structure

TICtac/
├── src/
│ ├── App.jsx # Game logic and UI
│ ├── main.jsx # React entry point
│ └── index.css # Styling
├── index.html
├── package.json
└── README.md

---

## ▶️ How to Run Locally

### Prerequisites

- Node.js (v18+ recommended)
- npm

### Steps

npm install
npm run dev

hen open the local URL shown in the terminal (usually http://localhost:5173).

⸻

🧠 How It Works (Simple)
• The game board is stored as an array of 9 values.
• Each move updates the board state.
• A helper function checks all winning combinations.
• If no winner exists and all squares are filled, the game is declared a draw.
• Move history allows players to jump back to any previous state.

⸻

🚀 Possible Improvements
• Highlight the winning line
• Add player score tracking
• Add single-player mode (AI)
• Animate moves and transitions
• Add theme toggle (light/dark)

👤 Author

David Ajaero
GitHub: https://github.com/DavidTertial
