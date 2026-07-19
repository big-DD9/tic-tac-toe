import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = [""] * 9
current_player = "X"
mode = "pvp"        # "pvp" or "ai"
difficulty = "hard" # "easy" or "hard"

def check_winner(b=None):
    b = b if b is not None else board
    win_positions = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for pos in win_positions:
        if b[pos[0]] == b[pos[1]] == b[pos[2]] != "":
            return b[pos[0]]
    return None

def minimax(b, depth, is_maximizing):
    winner = check_winner(b)
    if winner == "O":
        return 10 - depth
    if winner == "X":
        return depth - 10
    if "" not in b:
        return 0

    if is_maximizing:
        best = -float("inf")
        for i in range(9):
            if b[i] == "":
                b[i] = "O"
                best = max(best, minimax(b, depth + 1, False))
                b[i] = ""
        return best
    else:
        best = float("inf")
        for i in range(9):
            if b[i] == "":
                b[i] = "X"
                best = min(best, minimax(b, depth + 1, True))
                b[i] = ""
        return best

def best_move_hard():
    best_score = -float("inf")
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

def ai_move():
    empty = [i for i in range(9) if board[i] == ""]
    if difficulty == "easy":
        # 70% random, 30% smart move
        if random.random() < 0.7:
            return random.choice(empty)
        return best_move_hard()
    return best_move_hard()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/set_mode", methods=["POST"])
def set_mode():
    global mode, difficulty, board, current_player
    data = request.json
    mode = data.get("mode", "pvp")
    difficulty = data.get("difficulty", "hard")
    board = [""] * 9
    current_player = "X"
    return jsonify({"status": "ok", "mode": mode, "difficulty": difficulty})

@app.route("/move", methods=["POST"])
def move():
    global current_player
    data = request.json
    position = data["position"]

    if board[position] != "":
        return jsonify({"status": "invalid"})

    board[position] = current_player
    winner = check_winner()
    draw = "" not in board

    if winner:
        return jsonify({"status": "win", "winner": winner, "board": board})
    if draw:
        return jsonify({"status": "draw", "board": board})

    current_player = "O" if current_player == "X" else "X"

    if mode == "ai" and current_player == "O":
        pos = ai_move()
        board[pos] = "O"
        winner = check_winner()
        draw = "" not in board
        current_player = "X"

        if winner:
            return jsonify({"status": "win", "winner": winner, "board": board})
        if draw:
            return jsonify({"status": "draw", "board": board})
        return jsonify({"status": "continue", "player": current_player, "board": board})

    return jsonify({"status": "continue", "player": current_player, "board": board})

@app.route("/reset", methods=["POST"])
def reset():
    global board, current_player
    board = [""] * 9
    current_player = "X"
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    app.run(debug=True)