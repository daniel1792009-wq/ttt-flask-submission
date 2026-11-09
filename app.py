"""Flask TTT submission: random placeholder only; no learning Agent or Q-table."""
import random
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__, root_path=str(Path(__file__).resolve().parent))
LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
         (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


def winning_line(board, mark):
    for line in LINES:
        if all(board[i] == mark for i in line):
            return list(line)
    return None


def is_valid_board(board):
    if not isinstance(board, str) or len(board) != 9:
        return False
    if any(cell not in 'XO.' for cell in board):
        return False
    x, o = board.count('X'), board.count('O')
    x_wins = winning_line(board, 'X') is not None
    o_wins = winning_line(board, 'O') is not None
    if x_wins and o_wins:
        return False
    # Either mark can start. A winner must have just taken the last turn.
    for first in ('X', 'O'):
        first_count, second_count = (x, o) if first == 'X' else (o, x)
        if first_count not in (second_count, second_count + 1):
            continue
        if x_wins and x != o + (first == 'X'):
            continue
        if o_wins and o != x + (first == 'O'):
            continue
        return True
    return False


def result(board, move=None):
    for mark, status in (('X', 'agent_wins'), ('O', 'human_wins')):
        line = winning_line(board, mark)
        if line is not None:
            return {'board': board, 'agent_move': move,
                    'status': status, 'winning_line': line}
    return {'board': board, 'agent_move': move,
            'status': 'playing' if '.' in board else 'draw', 'winning_line': None}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/move', methods=['POST'])
def api_move():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or 'board' not in data or 'agent' not in data:
        return {'error': 'Send JSON with board and agent fields.'}, 400
    if data['agent'] != 'random':
        return {'error': f"Unknown agent: {data['agent']!r}"}, 400
    board = data['board']
    if not is_valid_board(board):
        return {'error': 'Invalid board: use nine X, O or . characters in a legal position.'}, 400
    current = result(board)
    if current['status'] != 'playing':
        return current
    if board.count('X') > board.count('O'):
        return {'error': 'It is the human turn. Play O before requesting an X move.'}, 400

    # TODO (later assignment): dispatch to a learned agent when qtable is supported.
    # This submission intentionally uses only a random-move placeholder.
    move = random.choice([i for i, cell in enumerate(board) if cell == '.'])
    updated = board[:move] + 'X' + board[move + 1:]
    return result(updated, move)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
