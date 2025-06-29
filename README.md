# 🧑‍🏫 AI Tutor – Personalized Quiz & Feedback Web App

**AI Tutor** is an intelligent Django + MySQL based web app that allows students to take quizzes on topics like Python, AI, ML, DSA, Maths, and DBMS. It provides personalized feedback with topic-wise strengths and weaknesses using an ML model, and includes an admin dashboard for analytics. Built with ❤️ using VS Code!

---

## 🚀 Features

- 🔐 User Registration & Login
- ✅ Random & Topic-wise Quizzes
- 🧠 Topic Strength/Weakness Analysis
- 🤖 ML-based Personalized Feedback
- 📊 Admin Dashboard with Analytics
- 💾 MySQL Database Integration
- 💻 Clean UI optimized for VS Code development

---

## 🛠 Technologies

- **Backend:** Django 4.x
- **Database:** MySQL
- **Machine Learning:** scikit-learn
- **Frontend:** HTML + Bootstrap 5
- **IDE:** Visual Studio Code

---

## 📦 Project Setup in VS Code

1️⃣ **Clone the Repository**

```bash
git clone https://github.com/Priyanshi43/ai-tutor.git
cd ai-tutor

2️⃣ Open in VS Code
code .

3️⃣ Create Virtual Environment
python -m venv venv


4️⃣ Activate Virtual Environment
venv\Scripts\activate


5️⃣ Install Requirements
pip install -r requirements.txt


6️⃣ Configure Database
In your settings.py, set up your MySQL credentials.

Create database in MySQL:
CREATE DATABASE ai_tutor_db;

Apply migrations:
python manage.py makemigrations
python manage.py migrate


7️⃣ Run Server
python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser 🎉