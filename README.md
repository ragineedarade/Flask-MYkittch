🍽️ MyKittchen AI

MyKittchen AI is an intelligent AI-powered meal planning and recipe assistant platform built using Flask.
It helps users discover recipes, watch cooking videos, listen to recipes with voice control, download recipes as PDFs, analyze food nutrition using AI image recognition, and manage meal plans efficiently.

The platform combines Flask, Gemini AI, Firebase, SQLite/MySQL, and modern frontend technologies to create a smart cooking experience.

✨ Key Features
🔐 Authentication System
User Signup & Login
Firebase Authentication
Secure Session Handling
Google Login Integration
🍛 Smart Recipe Management

✅ Submit Recipes
✅ Upload Recipe Images
✅ Search Recipes
✅ Filter Recipes by:

Cuisine
Diet
Category

✅ Community Recipe Sharing

🤖 AI Nutrition Analyzer (NEW)

Upload a food image and AI will automatically detect:

Calories
Protein
Carbohydrates
Fiber
Fats
Vitamins
Food Quantity
Food Name

Powered by:

Gemini AI Vision Model
🎤 AI Voice Recipe Reader (NEW)

Users can:

Listen to recipes
Pause recipe using voice command
Resume recipe using voice command
Supported Commands
“Stop”
“Start”
“Resume”

Built using:

Speech Synthesis API
Speech Recognition API
📺 YouTube Recipe Video Integration (NEW)

Automatically searches and displays:

Recipe tutorial videos
Cooking instructions
Related recipe content

Integrated with:

YouTube Search & Embed
📄 Recipe PDF Download (NEW)

Users can:

Download recipes as PDF
Print recipes
Save recipes offline
📅 Meal Planning System

Users can:

Plan meals
Save meal schedules
Organize daily recipes

Meal plans stored in:

MySQL Database
📸 Image Upload System
Upload food images
Upload recipe thumbnails
Firebase Storage Integration
Local Upload Support
🔍 Search & Filtering

Search recipes by:

Recipe Name
Ingredients
Keywords

Advanced filtering:

Cuisine
Diet Type
Recipe Category
🛡️ Security Features

✅ Environment Variables (.env)
✅ API Key Protection
✅ Secure Authentication
✅ Session Management

🧠 AI Features Included
Feature	Technology
Nutrition Detection	Gemini AI
Food Image Analysis	Gemini Vision
Voice Commands	Web Speech API
Recipe Audio Reading	Speech Synthesis
YouTube Video Search	YouTube Embed
PDF Generation	JavaScript Print API
🛠️ Tech Stack
Layer	Technologies Used
Frontend	HTML, CSS, JavaScript, Bootstrap
Backend	Python, Flask
Database	SQLite, MySQL, Firebase Firestore
AI	Gemini AI
Authentication	Firebase Auth
Storage	Firebase Storage
ORM	Flask SQLAlchemy
APIs	YouTube API, Gemini API
Voice Features	Speech Recognition API
PDF Export	JavaScript Print API
📂 Folder Structure
MyKittchen/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│   ├── uploads/
│   └── recipe_pdfs/
│
├── templates/
│   ├── index.html
│   ├── recipes.html
│   ├── nutrition.html
│   ├── nutrition_result.html
│   ├── login.html
│   ├── dashboard.html
│   └── submit_recipe.html
│
├── app.py
├── users.db
├── recipes.db
├── requirements.txt
├── .env
└── README.md
⚙️ Installation & Setup
📦 Prerequisites
Python 3.x
pip
Firebase Project
Gemini API Key
MySQL Server
🔧 Clone Repository
git clone https://github.com/ragineedarade/flask-mykittchen-project.git

cd flask-mykittchen-project
🧪 Create Virtual Environment
Windows
python -m venv venv

venv\Scripts\activate
Mac/Linux
python3 -m venv venv

source venv/bin/activate
📥 Install Dependencies
pip install -r requirements.txt

OR

pip install flask flask_sqlalchemy pillow requests werkzeug firebase-admin google-genai
📁 Create Upload Folder

Inside static folder create:

static/uploads
🔑 Gemini AI Setup

Get API key from:

Google AI Studio

🔐 Environment Variables

Create .env

SECRET_KEY=your_secret_key

FIREBASE_API_KEY=your_firebase_key

MYSQL_USER=root

MYSQL_PASSWORD=your_password

MYSQL_DB=mykittchen

GEMINI_API_KEY=your_gemini_api_key
▶️ Run Application
python app.py

Visit:

http://127.0.0.1:5000
📸 Screenshots
Home Page
![Home](screenshots/home.png)
Recipe Page
![Recipes](screenshots/recipes.png)
Nutrition Analyzer
![Nutrition](screenshots/nutrition.png)
AI Recipe Reader
![Voice Assistant](screenshots/voice.png)
🚀 Future Improvements
AI Recipe Recommendation
AI Meal Planner
Daily Calorie Tracker
BMI Calculator
AI Diet Recommendation
AI Chatbot Cooking Assistant
Multi-language Voice Support
Dark Mode
Mobile App Version
👩‍💻 Developed By
Raginee Darade
Python Developer
AI Enthusiast
Full Stack Developer
Flask & AI Integration Developer

GitHub:
Raginee Darade GitHub

⭐ Support

If you like this project:

⭐ Star the repository
🍴 Fork the repository
🧠 Contribute new features
🚀 Share with others
