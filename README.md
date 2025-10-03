# 🌍 Poverty Hub

Poverty Hub is a web-based platform built with **Flask (Python)** to support **SDG 1: No Poverty**.  
It provides tools for **financial literacy, crowdfunding, and microloan support** for low-income families and small businesses.

---

## 🚀 Features
- 📊 **Financial Literacy Module** – Learn how to budget and save.
- 🤖 **AI-Powered Budgeting Suggestions** – Personalized tips for households.
- 💰 **Crowdfunding Platform** – Communities can directly support individuals in need.
- 🏦 **Microloan System** – Simple loan requests and repayments.
- 🗺 **Geospatial Analysis** – Map poverty-stricken areas and guide interventions.

---

## 🛠 Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (default), easily upgradable to PostgreSQL/MySQL
- **Templating:** Jinja2
- **Version Control:** Git & GitHub

---

## 📂 Project Structure
poverty_hub/
│── app.py # Main Flask app
│── models.py # Database models
│── requirements.txt # Dependencies
│── README.md # Project documentation
│
├── templates/ # HTML Templates
│ ├── base.html # Layout template
│ ├── home.html # Homepage
│ ├── projects.html # List of SDG projects
│ ├── donate.html # Donation page
│ └── microloans.html # Microloan management
│
├── static/ # CSS, JS, Images
│ ├── css/
│ ├── js/
│ └── img/


---

## ⚙️ Installation & Setup
**Clone the repository**
   ```bash
   git clone https://github.com/your-username/poverty-hub.git
   cd poverty-hub

**Create a virtual environment**
 ```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

**Install dependencies**
 ```bash
pip install -r requirements.txt

**Run the application**
 ```bash
flask run

http://127.0.0.1:5000


