from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Dictionary to store game states by room
games = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def make_move():
    data = request.get_json()
    room = data['room']
    move = data['move']
    player = data['player']

    # If the room doesn't exist, return an error
    if room not in games:
        return jsonify(success=False, error="Room not found"), 404

    game_state = games[room]

    # Check if it's the player's turn
    if (game_state['turn'] == 'w' and player != 'white') or (game_state['turn'] == 'b' and player != 'black'):
        return jsonify(success=False, error="It's not your turn"), 403

    # Add the move to the room's move history
    game_state['moves'].append(move)

    # Toggle the turn (from white to black, or black to white)
    game_state['turn'] = 'b' if game_state['turn'] == 'w' else 'w'

    return jsonify(success=True)

@app.route('/state/<room>', methods=['GET'])
def get_game_state(room):
    if room in games:
        return jsonify(moves=games[room]['moves'], turn=games[room]['turn'])
    else:
        return jsonify(moves=[], turn='w')

@app.route('/create_room', methods=['POST'])
def create_room():
    data = request.get_json()
    room = data['room']

    # Create a new room if it doesn't exist, initialize the first turn as white
    if room not in games:
        games[room] = {
            'moves': [],
            'turn': 'w',  # white starts first
            'players': {'white': None, 'black': None}  # Keep track of players
        }
        return jsonify(success=True)
    else:
        return jsonify(success=False, error="Room already exists"), 400

@app.route('/join_room', methods=['POST'])
def join_room():
    data = request.get_json()
    room = data['room']
    player = data['player']

    if room not in games:
        return jsonify(success=False, error="Room not found"), 404

    # Assign the player to a color if the spot is available
    if games[room]['players']['white'] is None:
        games[room]['players']['white'] = player
        return jsonify(success=True, color='white')
    elif games[room]['players']['black'] is None:
        games[room]['players']['black'] = player
        return jsonify(success=True, color='black')
    else:
        return jsonify(success=False, error="Room is full"), 400

if __name__ == '__main__':
    app.run(debug=True)
