# 🍽️ MyKittchen

**MyKittchen** is a smart meal planning and recipe submission platform built using Flask. It helps users manage meals, explore community recipes, upload their own, and store data securely using Firebase and SQL databases. It supports authentication, cloud image uploads, and integrates multiple databases for flexibility.

---

## ✨ Key Features

🔐 **Authentication**
- Sign up and login using Firebase Authentication
- Secure access and session management

📋 **Recipe Management**
- Submit new recipes with title, ingredients, steps, and images
- View recipes stored in Firebase Firestore
- Search recipes by name or keyword

🍛 **Meal Planning**
- Users can plan meals by selecting recipes
- Meal plans are stored and fetched from MySQL

📸 **Image Upload**
- Upload recipe images to Firebase Storage
- Display images in the recipe view

🛡️ **Secure Secret Handling**
- Uses `.env` file to manage secrets and API keys
- No hardcoded secrets

🔍 **Search & Filter**
- Search recipes by title
- Filter recipes (optional feature to be extended)

📂 **Multi-Database Integration**
- Firebase Firestore: Store user-submitted recipes
- MySQL: Store meal planning data
- SQLite: Used for local backups or fallback data

---

## 🛠️ Tech Stack

| Layer          | Technologies Used |
|----------------|-------------------|
| **Frontend**   | HTML, CSS, JavaScript, Bootstrap |
| **Backend**    | Python, Flask |
| **Authentication** | Firebase Auth |
| **Database**   | Firebase Firestore, MySQL, SQLite |
| **Image Upload** | Firebase Storage |
| **Others**     | dotenv, Flask extensions |

---

## 🖼️ Screenshots (Coming Soon)

> Add your screenshots later:

```markdown
![Login Page](screenshots/login.png)
![Submit Recipe](screenshots/submit_recipe.png)
![Meal Planner](screenshots/meal_planner.png)
🧩 Folder Structure
bash
Copy
Edit
flask-mykittchen-project/
│
├── static/                # CSS, JS, Images
├── templates/             # HTML templates
├── app.py                 # Main Flask app
├── firebase_config.py     # Firebase connection setup
├── mysql_config.py        # MySQL DB connection
├── recipe_routes.py       # Route logic
├── .env                   # Environment variables
├── requirements.txt       # Dependencies
└── README.md              # This file
⚙️ Setup & Installation
📦 Prerequisites
Python 3.x

pip

Firebase Project (Firestore + Auth + Storage)

MySQL server

🔧 Installation Steps
bash
Copy
Edit
# Clone the repository
git clone https://github.com/ragineedarade/flask-mykittchen-project.git
cd flask-mykittchen-project

# Create virtual environment
python -m venv venv
# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
🔐 Firebase Setup
Create a Firebase project with:

Firestore database

Authentication (Email/Password)

Storage (for image uploads)

🔑 Environment Variables
Create a .env file at the root:

env
Copy
Edit
FIREBASE_API_KEY=your_api_key
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_storage_bucket
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=mykittchen
SECRET_KEY=your_flask_secret_key
▶️ Run the App
bash
Copy
Edit
flask run
Visit: http://127.0.0.1:5000

📊 Future Improvements
User Profile Page

Meal Plan Calendar View

Like / Favorite Recipes

AI-based Recipe Suggestions

Admin Panel for Moderation

