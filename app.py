from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = [""] * 9
current_player = "X"

def check_winner():
    win_conditions = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)  # FIXED
    ]
    for a, b, c in win_conditions:
        if board[a] == board[b] == board[c] != "":
            return board[a]
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global current_player, board

    data = request.get_json()
    index = data['index']

    if board[index] == "":
        board[index] = current_player
        winner = check_winner()

        if winner:
            return jsonify({"board": board, "winner": winner})

        current_player = "O" if current_player == "X" else "X"

    return jsonify({"board": board, "winner": None})

@app.route('/reset', methods=['POST'])
def reset():
    global board, current_player
    board = [""] * 9
    current_player = "X"
    return jsonify({"status": "reset"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
