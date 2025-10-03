from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Budget, LoanApplication, CrowdfundingCampaign, Donation, PovertyData
from werkzeug.security import check_password_hash
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Sample poverty data (in production, this would come from a database)
SAMPLE_POVERTY_DATA = [
    {'region': 'Downtown Eastside', 'poverty_rate': 24.5, 'population': 18000, 
     'median_income': 28000, 'unemployment_rate': 15.2, 'lat': 49.283, 'lng': -123.100},
    {'region': 'Hastings-Sunrise', 'poverty_rate': 18.2, 'population': 22000,
     'median_income': 32000, 'unemployment_rate': 12.1, 'lat': 49.281, 'lng': -123.055},
    {'region': 'Strathcona', 'poverty_rate': 22.7, 'population': 12000,
     'median_income': 29500, 'unemployment_rate': 14.5, 'lat': 49.273, 'lng': -123.085}
]

@app.route('/')
def index():
    if current_user.is_authenticated:
        # Get user's recent budgets
        recent_budgets = Budget.query.filter_by(user_id=current_user.id)\
                                   .order_by(Budget.created_at.desc()).limit(3).all()
        
        # Get active campaigns
        active_campaigns = CrowdfundingCampaign.query.filter_by(is_active=True)\
                                                   .order_by(CrowdfundingCampaign.created_at.desc()).limit(3).all()
        
        return render_template('index.html', 
                             budgets=recent_budgets,
                             campaigns=active_campaigns,
                             poverty_data=SAMPLE_POVERTY_DATA)
    return render_template('index.html', poverty_data=SAMPLE_POVERTY_DATA)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/budget')
@login_required
def budget():
    budgets = Budget.query.filter_by(user_id=current_user.id)\
                         .order_by(Budget.created_at.desc()).all()
    return render_template('budget.html', budgets=budgets)

@app.route('/api/budget', methods=['POST'])
@login_required
def create_budget():
    data = request.get_json()
    
    budget = Budget(
        user_id=current_user.id,
        month=data['month'],
        income=float(data['income']),
        housing=float(data.get('housing', 0)),
        food=float(data.get('food', 0)),
        transportation=float(data.get('transportation', 0)),
        healthcare=float(data.get('healthcare', 0)),
        education=float(data.get('education', 0)),
        savings=float(data.get('savings', 0)),
        other=float(data.get('other', 0))
    )
    
    db.session.add(budget)
    db.session.commit()
    
    return jsonify({'message': 'Budget created successfully', 'id': budget.id})

@app.route('/api/budget/<int:budget_id>', methods=['DELETE'])
@login_required
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    
    if budget.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(budget)
    db.session.commit()
    
    return jsonify({'message': 'Budget deleted successfully'})

@app.route('/crowdfunding')
def crowdfunding():
    campaigns = CrowdfundingCampaign.query.filter_by(is_active=True)\
                                        .order_by(CrowdfundingCampaign.created_at.desc()).all()
    return render_template('crowdfunding.html', campaigns=campaigns)

@app.route('/api/campaigns', methods=['POST'])
@login_required
def create_campaign():
    data = request.form
    
    campaign = CrowdfundingCampaign(
        title=data['title'],
        description=data['description'],
        target_amount=float(data['target_amount']),
        organizer_name=data['organizer_name'],
        location=data['location'],
        category=data['category']
    )
    
    db.session.add(campaign)
    db.session.commit()
    
    flash('Campaign created successfully!', 'success')
    return redirect(url_for('crowdfunding'))

@app.route('/api/donate', methods=['POST'])
@login_required
def make_donation():
    data = request.get_json()
    
    donation = Donation(
        user_id=current_user.id,
        campaign_id=int(data['campaign_id']),
        amount=float(data['amount']),
        anonymous=data.get('anonymous', False),
        message=data.get('message', '')
    )
    
    # Update campaign current amount
    campaign = CrowdfundingCampaign.query.get(data['campaign_id'])
    campaign.current_amount += donation.amount
    
    db.session.add(donation)
    db.session.commit()
    
    return jsonify({'message': 'Donation successful!'})

@app.route('/microloan')
@login_required
def microloan():
    applications = LoanApplication.query.filter_by(user_id=current_user.id)\
                                      .order_by(LoanApplication.created_at.desc()).all()
    return render_template('microloan.html', applications=applications)

@app.route('/api/loan-application', methods=['POST'])
@login_required
def submit_loan_application():
    data = request.get_json()
    
    application = LoanApplication(
        user_id=current_user.id,
        amount=float(data['amount']),
        purpose=data['purpose'],
        business_plan=data.get('business_plan', ''),
        repayment_period=int(data['repayment_period'])
    )
    
    db.session.add(application)
    db.session.commit()
    
    return jsonify({'message': 'Loan application submitted successfully!'})

@app.route('/map')
def map():
    return render_template('map.html', poverty_data=SAMPLE_POVERTY_DATA)

@app.route('/api/poverty-data')
def get_poverty_data():
    return jsonify(SAMPLE_POVERTY_DATA)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Add sample poverty data
        if not PovertyData.query.first():
            for data in SAMPLE_POVERTY_DATA:
                poverty_data = PovertyData(
                    region=data['region'],
                    poverty_rate=data['poverty_rate'],
                    population=data['population'],
                    median_income=data['median_income'],
                    unemployment_rate=data['unemployment_rate'],
                    latitude=data['lat'],
                    longitude=data['lng']
                )
                db.session.add(poverty_data)
            db.session.commit()
    
    app.run(debug=True)
    # Add these routes to your existing app.py

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))