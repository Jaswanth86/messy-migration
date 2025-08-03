from flask import Flask, request, jsonify
import sqlite3
import os
import hashlib
import hmac

app = Flask(__name__)
DATABASE = os.environ.get('DATABASE_URL', 'users.db')

##################
# Database Utils #
##################

def get_db():
    # Each request gets its own connection
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    ''')
    # Seed only if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            [
                ("John Doe", "john@example.com", hash_password("password123")),
                ("Jane Smith", "jane@example.com", hash_password("secret456")),
                ("Bob Johnson", "bob@example.com", hash_password("qwerty789")),
            ]
        )
    conn.commit()
    conn.close()


###############
#  Security   #
###############

def hash_password(password):
    """Hash password with a static salt for this demo. Use something better for production."""
    # For demonstration only! Use bcrypt or argon2 in production.
    salt = b'some_static_salt'
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

def verify_password(password, hashed):
    return hmac.compare_digest(hash_password(password), hashed)


#############################
# RESTful Endpoint Handlers #
#############################

@app.route('/')
def home():
    return jsonify({"message": "User Management System"}), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    conn = get_db()
    users = conn.execute("SELECT id, name, email FROM users").fetchall()
    conn.close()
    users_list = [dict(u) for u in users]
    return jsonify(users_list), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db()
    user = conn.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user)), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        # Validate input
        if not data or not all(k in data for k in ('name', 'email', 'password')):
            return jsonify({"error": "Missing required fields"}), 400
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']

        if len(password) < 6:
            return jsonify({"error": "Password too short"}), 400

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, hash_password(password))
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return jsonify({"error": "Email already exists"}), 409
        finally:
            conn.close()
        return jsonify({"message": "User created"}), 201
    except Exception as e:
        return jsonify({"error": "Invalid input"}), 400

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data or not ('name' in data or 'email' in data):
        return jsonify({"error": "No data to update"}), 400

    updates = []
    params = []
    if 'name' in data:
        updates.append("name = ?")
        params.append(data['name'])
    if 'email' in data:
        updates.append("email = ?")
        params.append(data['email'].lower())
    params.append(user_id)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", params)
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    conn.close()
    return jsonify({"message": "User updated"}), 200

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "User not found"}), 404
    conn.close()
    return jsonify({"message": f"User {user_id} deleted"}), 200

@app.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name', '').strip()
    if not name:
        return jsonify({"error": "Please provide a name to search"}), 400
    conn = get_db()
    # Uses parameterized query for LIKE search
    users = conn.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",)).fetchall()
    conn.close()
    users_list = [dict(u) for u in users]
    return jsonify(users_list), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ('email', 'password')):
        return jsonify({"status": "failed", "error": "Email and password required"}), 400
    email, password = data['email'].lower(), data['password']
    conn = get_db()
    user = conn.execute("SELECT id, password_hash FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    if user and verify_password(password, user['password_hash']):
        return jsonify({"status": "success", "user_id": user['id']}), 200
    else:
        return jsonify({"status": "failed"}), 401

# Initialize database before starting app
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
