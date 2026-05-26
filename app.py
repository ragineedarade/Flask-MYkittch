 from PIL import Image
from google import genai
import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import requests
from flask import Flask, render_template, request
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import requests
import json
import os  # Import os for path handling
import datetime
app = Flask(__name__)
# IMPORTANT: Change this to a strong, random key in production!
app.secret_key = ' '

# --- Configuration for users.db (Direct sqlite3) ---
DATABASE = 'users.db'

# --- Configuration for recipes.db (Flask-SQLAlchemy) ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'recipes.db')
# Recommended to suppress warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy AFTER app config is set
db = SQLAlchemy(app)

# You'll need your Google Client ID and Client Secret
# It's best practice to load these from environment variables or a config file
# For demonstration, I'll put placeholders here:
GOOGLE_CLIENT_ID = " "
# Make sure to replace this with your actual complete client secret
GOOGLE_CLIENT_SECRET = " "
# Must match what you configured in Google Cloud Console
GOOGLE_REDIRECT_URI = " "


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


# --- Define the Recipe Model (Database Table) for SQLAlchemy ---p
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(255), nullable=True, default='')
    cuisine = db.Column(db.String(255), nullable=True, default='')
    diet = db.Column(db.String(255), nullable=True, default='')

    def __repr__(self):
        return f'<Recipe {self.title}>'


# Call init_db for users.db when the application starts
# And create tables for recipes.db using SQLAlchemy
with app.app_context():
    init_db()  # For users.db
    db.create_all()  # For recipes.db (and any other SQLAlchemy models)


# --- Flask Routes ---

@app.route('/')
def index():  # Renamed to avoid conflict with `main()` function in old code structure
    """Main homepage route."""
    return render_template('index.html')  # Now renders your MYKittech index.html


@app.route('/login_signup')
def login_signup():
    """Renders the dedicated login/signup HTML page."""
    return render_template('login.html')  # This route will render your login.html

# NOTE: The @app.route('/main') route below conflicts with the definition above
# if you intend for `/` to be the "main" page. I've renamed the top one to `main_page`.
# If you want `/main` to show something different, keep it.
# If `index.html` is your main page, then you might not need this `/main` route or
# you might want it to redirect to `/`


@app.route('/main')
def main():
    """Renders the main HTML page."""
    # This might be redundant if '/' leads to index.html
    # Assuming main.html is now index.html
    return render_template('main.html')


@app.route('/meal_planner')  # Changed from meal-planner for consistency
def meal_planner():
    """Placeholder for the meal planner page."""
    return render_template('meal-planner.html')  # Changed from meal-planner.html


@app.route('/my_account')
def my_account():
    """Placeholder for the my account page."""
    # This page should ideally check if the user is logged in
    if 'user_id' in session:
        # Render a dashboard or account page
        return render_template('dashboard.html')
    # Redirect to login if not authenticated
    return redirect(url_for('login_signup'))


@app.route('/chat')
def chat():
    """Placeholder for the FAQ page."""
    return render_template('chatbot.html')  # Changed from faq.html to chatbot.html


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


@app.route('/recipes')
def recipes():
    """Displays all submitted recipes with optional filtering and search."""
    # Get filter parameters from the URL query string
    selected_categories = request.args.getlist('category')
    selected_cuisine = request.args.getlist('cuisine')
    selected_diet = request.args.getlist('diet')
    search_query = request.args.get('search_query')  # NEW: Get search query

    # Start with all recipes
    query = Recipe.query

    # Apply search filter if present
    if search_query:
        # Use .ilike() for case-insensitive search
        query = query.filter(Recipe.title.ilike(f'%{search_query}%'))

    # Apply category filters if they are present
    if selected_categories:
        category_filters = []
        for cat in selected_categories:
            category_filters.append(Recipe.category.like(f'%{cat}%'))
        query = query.filter(db.or_(*category_filters))

    # Apply cuisine filters if they are present
    if selected_cuisine:
        cuisine_filters = []
        for cuis in selected_cuisine:
            cuisine_filters.append(Recipe.cuisine.like(f'%{cuis}%'))
        query = query.filter(db.or_(*cuisine_filters))

    # Apply diet filters if they are present
    if selected_diet:
        diet_filters = []
        for d in selected_diet:
            diet_filters.append(Recipe.diet.like(f'%{d}%'))
        query = query.filter(db.or_(*diet_filters))

    # Retrieve filtered recipes, ordered by ID (newest first)
    all_recipes = query.order_by(Recipe.id.desc()).all()

    # Pass all relevant data back to the template
    return render_template('recipes.html',
                           recipes=all_recipes,
                           selected_categories=selected_categories,
                           selected_cuisine=selected_cuisine,
                           selected_diet=selected_diet,
                           search_query=search_query)  # NEW: Pass search query back


@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    """Handles displaying the recipe submission form and processing submissions."""
    if request.method == 'POST':
        title = request.form.get('recipeTitle')
        image_url = request.form.get('imageUrl')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')

        categories = request.form.getlist('categories')
        cuisine = request.form.getlist('cuisine')
        diet = request.form.getlist('diet')

        category_str = ','.join(categories)
        cuisine_str = ','.join(cuisine)
        diet_str = ','.join(diet)

        if not title or not ingredients or not instructions:
            return "Missing required fields (Title, Ingredients, Instructions)", 400

        new_recipe = Recipe(
            title=title,
            image_url=image_url,
            ingredients=ingredients,
            instructions=instructions,
            category=category_str,
            cuisine=cuisine_str,
            diet=diet_str
        )

        db.session.add(new_recipe)
        db.session.commit()

        return redirect(url_for('recipes'))

    return render_template('submit_recipe.html')


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"ContactMessage('{self.name}', '{self.email}', '{self.date_submitted}')"


# Create database tables if they don't exist
with app.app_context():
    db.create_all()


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Basic validation (you'll want more robust validation in a real app)
        if not name or not email or not message:
            flash('Please fill in all fields!', 'error')
            return render_template('contact.html')

        # Create a new ContactMessage object
        new_message = ContactMessage(name=name, email=email, message=message)

        # Add to database session and commit
        try:
            db.session.add(new_message)
            db.session.commit()
            flash('Thanks! We’ll get back to you soon.', 'success')
            return redirect(url_for('contact'))  # Redirect to clear the form
        except Exception as e:
            db.session.rollback()  # Rollback on error
            flash(f'An error occurred: {e}', 'error')

    return render_template('contact.html')

# In your app.py file, make sure this route exists:


@app.route('/profile')
def profile():  # <--- This function name 'profile' is the endpoint name
    """Renders the user profile page."""
    if 'user_id' not in session:
        flash('You must be logged in to view your profile.', 'warning')
        return redirect(url_for('login_signup'))
    return render_template('profile.html', user_name=session['user_name'], user_email=session['user_email'])


YOUTUBE_API_KEY = " "


@app.route("/")
def home():

    query = request.args.get("query")

    video_id = None

    if query:

        url = (
            "https://www.googleapis.com/youtube/v3/search"
        )

       

        params = {
            "part": "snippet",
            "q": query + " recipe",
            "key": YOUTUBE_API_KEY,
            "maxResults": 1,
            "type": "video"
        }

        response = requests.get(url, params=params)

        data = response.json()

        if data["items"]:
            video_id = data["items"][0]["id"]["videoId"]

    return render_template(
        "index.html",
        video_id=video_id
    )


#  this is  a  function of a  neutrition

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

client = genai.Client(
    api_key=" "
)

# ===============================
# NUTRITION ANALYZER ROUTE
# ===============================


@app.route('/nutrition')
def nutrition():

    return render_template(
        'nutrition.html'
    )

# ===============================
# ANALYZE FOOD IMAGE
# ===============================


@app.route(
    '/analyze_food',
    methods=['POST']
)
def analyze_food():

    if 'food_image' not in request.files:

        return "No image uploaded"

    image = request.files['food_image']

    if image.filename == "":

        return "No image selected"

    # SAVE IMAGE
    image_path = os.path.join(
        app.config['UPLOAD_FOLDER'],
        image.filename
    )

    image.save(image_path)

    # OPEN IMAGE
    img = Image.open(image_path).convert("RGB")

    # ===============================
    # AI PROMPT
    # ===============================

    prompt = """

    Analyze this food image carefully.

    Tell me:

    1. Food Name
    2. Estimated Calories
    3. Protein
    4. Carbohydrates
    5. Fats
    6. Fiber
    7. Vitamins
    8. Estimated Quantity

    Return response in beautiful HTML format.

    """

    # ===============================
    # GEMINI RESPONSE
    # ===============================

    response = client.models.generate_content(

        model="gemini-2.0-flash",

        contents=[prompt, img]

    )

    nutrition_result = response.text

    return render_template(

        'nutrition_result.html',

        image_path=image_path,

        nutrition_result=nutrition_result

    )


if __name__ == "__main__":
    app.run(debug=True)
