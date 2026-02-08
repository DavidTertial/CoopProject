# C Digital Clock App ⏰

A simple terminal-based digital clock written in C that displays the current system time and updates every second.

---

## 🎥 Demo

Below is a short demo video showing the clock running in real time and updating every second in the terminal.

📁 Demo location: demo/
🎬 File format: .mp4 (managed via Git LFS)

---

## 📌 Description

This program uses standard C libraries to fetch the current system time and continuously display it in `HH:MM:SS` format. The clock refreshes every second in the same terminal line, simulating a real-time digital clock.

---

## 🛠️ Features

- Displays real-time system clock
- Updates every second
- Uses 24-hour time format
- Runs continuously until manually stopped
- Lightweight and terminal-based

---

## 📂 Files

- `main.c` – Main C source file containing the clock logic

---

## ⚙️ Requirements

- C compiler (GCC recommended)
- Unix-based system (Linux or macOS)
  - Uses `unistd.h` for the `sleep()` function

---

## ▶️ How to Compile and Run

### Compile

gcc main.c -o clock

### Run

./clock

### Stop the clock

Ctrl + C
