# 🗳️ Polls App

A full-stack web application that allows users to vote on polls, view results, and for admins to manage polls and users.

---

## 🔧 Tech Stack

- **Backend**: Flask, SQLAlchemy, JWT, PostgreSQL
- **Frontend**: React, Bootstrap
- **Authentication**: Token-based (JWT)
- **Deployment**: Vercel (Frontend), Flask (Backend)

---

## 📦 Features

### 🔐 User Features
- Signup / Login / Logout
- View **active** polls and vote with optional justification
- View **previous polls** and their results

### 🛠️ Admin Features
- Create new polls with multiple options
- Activate / Deactivate polls
- Delete polls
- View all users
- Promote users to admin
- View all votes and justifications

---

## 🖥️ Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/polls-app.git
cd polls-app

### BBACKEND SET UP
cd polls-backend
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
pip install -r requirements.txt

### Set environment variable
export FLASK_APP=app.py      # On Windows: set FLASK_APP=app.py

# Initialize DB
flask db init
flask db migrate
flask db upgrade

# Run the server
flask run --port=5001


###3. Frontend Setup (React)
bash
Copy code
cd polls-frontend
npm install
npm start

🚀 Deployment
Frontend: Vercel
vercel --prod

Backend: Can be deployed to Render, Railway, or any cloud platform supporting Flask + PostgreSQL.

👨‍💻 Contributors
@wachira mwangi

@Simon Mungai

