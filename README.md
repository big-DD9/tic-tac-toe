# Flask Tic Tac Toe 🎮

A web-based Tic Tac Toe game built with Flask, featuring an unbeatable AI opponent powered by the **minimax algorithm**.

🔗 **[Play it live](https://tic-tac-toe-uhai.onrender.com)**

## Features

- **2 Player mode** — classic local head-to-head
- **vs AI mode** — play against a computer opponent using minimax with two difficulty levels:
  - **Easy** — mostly random moves, beatable
  - **Hard** — full minimax search, plays perfectly (best you can do is draw)
- **Persistent scoreboard** — tracks X wins, O wins, and draws across sessions
- **Win/draw detection** with a confetti celebration on every win
- **Clean, responsive UI** with a custom color theme

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, vanilla JavaScript (fetch API, no frameworks)
- **AI**: Minimax algorithm with game tree search
- **Deployment**: Render (Gunicorn WSGI server)

## How It Works

The AI opponent evaluates every