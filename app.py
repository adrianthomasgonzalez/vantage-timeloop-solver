from flask import Flask, request, jsonify, render_template
from solver import solve

app = Flask(__name__)

# Store the last solution in memory (simple approach)
last_solution = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    global last_solution
    data = request.json
    circles = data['circles']
    starting_colors = set(c for circle in circles for c in circle)
    last_solution = solve(circles, starting_colors)
    solvable = len(last_solution) > 0  # True if at least one solution exists
    return jsonify({'solvable': solvable})


@app.route('/solution', methods=['POST'])
def solution():
    global last_solution
    if last_solution:
        return jsonify({'solution': last_solution})  # ✅ return as-is
    else:
        return jsonify({'solution': []})


if __name__ == '__main__':
    app.run(debug=True)
