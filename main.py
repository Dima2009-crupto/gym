from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            exercise TEXT NOT NULL,
            duration INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/workouts', methods=['GET'])
def get_workouts():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workouts')
    workouts = cursor.fetchall()
    conn.close()
    return jsonify(workouts)


@app.route('/api/workouts', methods=['POST'])
def add_workout():
    data = request.json
    date = data['date']
    exercise = data['exercise']
    duration = data['duration']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO workouts (date, exercise, duration) VALUES (?, ?, ?)', (date, exercise, duration))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Workout added successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
