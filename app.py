from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = [""] * 9
current_player = "X"

def check_winner():
    win_positions = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # columns
        [0,4,8], [2,4,6]            # diagonals
    ]
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] != "":
            return board[pos[0]]
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global current_player
    data = request.json
    position = data["position"]

    if board[position] == "":
        board[position] = current_player
        winner = check_winner()
        draw = "" not in board

        if winner:
            response = {"status": "win", "winner": winner}
        elif draw:
            response = {"status": "draw"}
        else:
            current_player = "O" if current_player == "X" else "X"
            response = {"status": "continue", "player": current_player}

        return jsonify(response)

    return jsonify({"status": "invalid"})

@app.route("/reset", methods=["POST"])
def reset():
    global board, current_player
    board = [""] * 9
    current_player = "X"
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    app.run(debug=True)