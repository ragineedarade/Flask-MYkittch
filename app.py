import sqlite3
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import uuid  # Import uuid for generating dummy passwords for Google users
import requests  # Import requests for making HTTP requests to Google APIs
import json  # Import json for handling JSON responses

app = Flask(__name__)
# IMPORTANT: Change this to a strong, random key in production!
app.secret_key = ' secrat key '

DATABASE = 'users.db'

# You'll need your Google Client ID and Client Secret
# It's best practice to load these from environment variables or a config file
# For demonstration, I'll put placeholders here:
GOOGLE_CLIENT_ID = ""
# Make sure to replace this with your actual complete client secret
GOOGLE_CLIENT_SECRET = " "
# Must match what you configured in Google Cloud Console
GOOGLE_REDIRECT_URI = ""


def init_db():
    """Initializes the SQLite database and creates the users table if it doesn't exist."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                google_id TEXT UNIQUE NULL
            )
        ''')
        conn.commit()
    print("Database initialized and 'users' table ensured.")


# Call init_db when the application starts
with app.app_context():
    init_db()


@app.route('/')
def index():
    """Renders the main index HTML page (MYKittech homepage)."""
    return render_template('index.html')  # Now renders your MYKittech index.html


@app.route('/login_signup')
def login_signup():
    """Renders the dedicated login/signup HTML page."""
    return render_template('login.html')  # This route will render your login.html


@app.route('/recipes')
def recipes():
    """Placeholder for the recipes page."""
    return render_template('recipe.html')  # This route will render your recipes.html


@app.route('/meal-planner')
def meal_planner():
    """Placeholder for the meal planner page."""
    return render_template('meal-planner.html')


@app.route('/submit_recipe')
def submit_recipe():
    return render_template('submit_recipe.html')


@app.route('/main')
def main():
    """Renders the main HTML page."""
    return render_template('main.html')


@app.route('/my_account')
def my_account():
    """Placeholder for the my account page."""
    # This page should ideally check if the user is logged in
    if 'user_id' in session:
        # Render a dashboard or account page
        return render_template('dashboard.html')
    # Redirect to login if not authenticated
    return redirect(url_for('login_signup'))


@app.route('/contact')
def contact():
    """Placeholder for the contact page."""
    return "<h1>Contact Us</h1><p>This is a placeholder for your contact information or form.</p>"


@app.route('/faq')
def faq():
    """Placeholder for the FAQ page."""
    return "<h1>Frequently Asked Questions</h1><p>This is a placeholder for your FAQ content.</p>"


@app.route('/privacy')
def privacy():
    """Placeholder for the Privacy Policy page."""
    return "<h1>Privacy Policy</h1><p>This is a placeholder for your Privacy Policy content.</p>"


@app.route('/terms')
def terms():
    """Placeholder for the Terms of Service page."""
    return "<h1>Terms of Service</h1><p>This is a placeholder for your Terms of Service content.</p>"


@app.route('/category/<name>')
def category(name):
    """Placeholder for recipe category pages."""
    return f"<h1>Category: {name.replace('-', ' ').title()}</h1><p>This is a placeholder for recipes in the {name.replace('-', ' ')} category.</p>"


@app.route('/api/signup', methods=['POST'])
def signup():
    """Handles user registration via email and password."""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'message': 'Missing required fields'}), 400

    # Hash the password before storing it
    password_hash = generate_password_hash(password)

    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, password_hash)
            )
            conn.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except sqlite3.IntegrityError:
        # This error occurs if the email (which is UNIQUE) already exists
        return jsonify({'message': 'Email already registered. Please use a different email or log in.'}), 409
    except Exception as e:
        print(f"Error during signup: {e}")
        return jsonify({'message': 'An error occurred during registration.'}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """Handles user login via email and password."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'message': 'Missing email or password'}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, email, password_hash FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

    # user[3] is password_hash
    if user and check_password_hash(user[3], password):
        # Store user info in session (for standard login)
        session['user_id'] = user[0]
        session['user_name'] = user[1]
        session['user_email'] = user[2]
        return jsonify({'message': 'Login successful!', 'user': {'name': user[1], 'email': user[2]}}), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


@app.route('/auth/google')
def google_auth():
    """Initiates the Google OAuth flow."""
    print("Redirecting to Google for authentication...")

    scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid"
    auth_url = (
        f"https://accounts.google.com/o/oauth2/auth?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        f"scope={scope}&"
        f"response_type=code&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    return redirect(auth_url)


@app.route('/auth/google/callback')
def google_callback():
    """Handles the callback from Google after successful authentication."""
    code = request.args.get('code')
    if not code:
        return jsonify({'message': 'Authorization code not found.'}), 400

    try:
        # 1. Exchange authorization code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        token_payload = {
            'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        token_response = requests.post(token_url, data=token_payload)
        token_data = token_response.json()

        if token_response.status_code != 200:
            print(
                f"Token exchange failed: {token_data.get('error_description', token_data)}")
            return jsonify({'message': 'Failed to exchange code for tokens.', 'details': token_data}), 400

        access_token = token_data.get('access_token')
        # id_token = token_data.get('id_token') # ID token contains user info, can be decoded directly

        if not access_token:
            return jsonify({'message': 'Access token not received.'}), 400

        # 2. Fetch user info using the access token
        userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        userinfo_headers = {'Authorization': f'Bearer {access_token}'}
        userinfo_response = requests.get(
            userinfo_url, headers=userinfo_headers)
        user_info = userinfo_response.json()

        if userinfo_response.status_code != 200:
            print(
                f"User info fetch failed: {user_info.get('error_description', user_info)}")
            return jsonify({'message': 'Failed to fetch user information.', 'details': user_info}), 400

        # Extract relevant user data
        google_id = user_info.get('sub')  # 'sub' is the unique Google ID
        email = user_info.get('email')
        # Use email as name if name is not provided
        name = user_info.get('name', email)

        if not email or not google_id:
            return jsonify({'message': 'Could not retrieve essential user info from Google.'}), 400

        # 3. Process user data: Check if user exists or register new user
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # Check if user exists by google_id. If not, check by email.
            cursor.execute("SELECT id, name, email FROM users WHERE google_id = ? OR email = ?",
                           (google_id, email))
            existing_user = cursor.fetchone()

            if existing_user:
                # User exists, log them in
                session['user_id'] = existing_user[0]
                session['user_name'] = existing_user[1]
                session['user_email'] = existing_user[2]
                print(f"User {email} logged in via Google.")
                return redirect(url_for('dashboard'))
            else:
                # User does not exist, register new user with Google info
                # Generate a dummy password hash as it's required by the schema,
                # but it won't be used for Google-authenticated users.
                password_hash = generate_password_hash(str(uuid.uuid4()))
                cursor.execute(
                    "INSERT INTO users (name, email, password_hash, google_id) VALUES (?, ?, ?, ?)",
                    (name, email, password_hash, google_id)
                )
                conn.commit()
                session['user_id'] = cursor.lastrowid
                session['user_name'] = name
                session['user_email'] = email
                print(f"New user {email} registered and logged in via Google.")
                return redirect(url_for('dashboard'))

    except requests.exceptions.RequestException as e:
        print(f"HTTP request error during Google OAuth: {e}")
        return jsonify({'message': 'Network error during Google authentication. Please try again.'}), 500
    except json.JSONDecodeError as e:
        print(f"JSON decode error during Google OAuth: {e}")
        return jsonify({'message': 'Invalid response from Google. Please try again.'}), 500
    except Exception as e:
        print(
            f"An unexpected error occurred during Google OAuth callback: {e}")
        return jsonify({'message': 'An unexpected error occurred during Google login.'}), 500


@app.route('/dashboard')
def dashboard():
    """A simple protected dashboard page."""
    if 'user_id' in session:
        return render_template('dashboard.html', user_name=session['user_name'])
    return render_template('login.html', error='You must be logged in to view this page.')


@app.route('/logout')
def logout():
    """Logs out the user by clearing the session."""
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_email', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    # You might need to install 'requests': pip install requests
    app.run(debug=True)
