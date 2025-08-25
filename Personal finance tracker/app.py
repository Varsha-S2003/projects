from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict


app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/profile_pics'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ------------------- Models -------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    min_balance = db.Column(db.Float, default=2000.0)
    profile_pic = db.Column(db.String(100), default='default.png')

    transactions = db.relationship('Transaction', backref='user', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# ------------------- User Loader -------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------- Routes -------------------

@app.route('/')
@login_required
def dashboard():
    income = sum(t.amount for t in current_user.transactions if t.type == 'Income')
    expense = sum(t.amount for t in current_user.transactions if t.type == 'Expense')
    balance = income - expense
    show_warning = balance < current_user.min_balance
    return render_template('index.html', income=income, expense=expense, balance=balance, show_warning=show_warning)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        transaction = Transaction(
            type=request.form['type'],
            category=request.form['category'],
            amount=float(request.form['amount']),
            description=request.form.get('description', ''),
            user_id=current_user.id
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_transaction.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.min_balance = float(request.form['min_balance'])
        if 'profile_pic' in request.files:
            pic = request.files['profile_pic']
            if pic.filename:
                pic_path = os.path.join(app.config['UPLOAD_FOLDER'], pic.filename)
                pic.save(pic_path)
                current_user.profile_pic = pic.filename
        db.session.commit()
        flash("Profile updated!", "success")
        return redirect(url_for('profile'))
    
    return render_template('profile.html')


@app.route('/view')
@login_required
def view_transactions():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).all()
    return render_template('view_transactions.html', transactions=transactions)



@app.route('/reports')
@login_required
def reports():
    user_id = current_user.id
    transactions = Transaction.query.filter_by(user_id=user_id).all()

    if not transactions:
        flash("No transactions available to generate reports.", "warning")
        return render_template("reports.html")

    # Get only expense transactions
    expenses = [t for t in transactions if t.type.lower() == 'expense']

    if not expenses:
        flash("No expenses available to generate reports.", "warning")
        return render_template("reports.html")

    pie_chart, bar_chart = None, None

    # Generate Pie Chart (by category)
    category_totals = defaultdict(float)
    for t in expenses:
        category_totals[t.category] += t.amount

    if category_totals:
        labels = list(category_totals.keys())
        values = list(category_totals.values())

        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("Expense Breakdown by Category")
        pie_path = f'static/images/pie_chart_{user_id}.png'
        os.makedirs(os.path.dirname(pie_path), exist_ok=True)
        plt.savefig(pie_path)
        plt.close()
        pie_chart = f'images/pie_chart_{user_id}.png'

    # Generate Bar Chart (Monthly)
    monthly_totals = defaultdict(float)
    for t in expenses:
        if t.timestamp:
            month = t.timestamp.strftime("%Y-%m")
            monthly_totals[month] += t.amount

    if monthly_totals:
        months = sorted(monthly_totals)
        amounts = [monthly_totals[m] for m in months]

        plt.figure(figsize=(8, 4))
        plt.bar(months, amounts, color='skyblue')
        plt.title("Monthly Expenses")
        plt.xlabel("Month")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        bar_path = f'static/images/bar_chart_{user_id}.png'
        plt.tight_layout()
        plt.savefig(bar_path)
        plt.close()
        bar_chart = f'images/bar_chart_{user_id}.png'

    return render_template("reports.html", pie_chart=pie_chart, bar_chart=bar_chart)



# ------------------- Run -------------------

if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        db.create_all()
    app.run(debug=True)
