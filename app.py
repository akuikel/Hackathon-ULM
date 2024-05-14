from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

# Initialize Flask app
app = Flask(__name__)

# Configure the SQLAlchemy part of the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lostandfound.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Folder where uploaded files will be stored, ensure it exists
app.config['UPLOAD_FOLDER'] = 'static/uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

app.config['PROOF_FOLDER'] = 'static/proofs'
if not os.path.exists(app.config['PROOF_FOLDER']):
    os.makedirs(app.config['PROOF_FOLDER'])

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

CATEGORIES = ["Pets", "Documents", "Phone", "Cash", "Debit/Credit Card", "Laptop", "Clothes", "Jewellery", "Purse", "Person", "Motorcycle", "Cycle", "Cars", "Others"]


db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Add the email field
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


from datetime import datetime


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50))
    receiver = db.Column(db.String(50))
    content = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    proof_image_path = db.Column(db.String(255))  # Store the relative path to the proof image
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    claimer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Define status choices and default status
    STATUS_CHOICES = {
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    }
    status = db.Column(db.String(50), nullable=False, default='pending', info={'choices': STATUS_CHOICES})

    item = db.relationship('Item', backref=db.backref('claims', lazy=True))
    claimer = db.relationship('User', backref=db.backref('claims', lazy=True))

    def __repr__(self):
        return f'<Claim {self.description} by {self.claimer_id} - Status: {self.status}>'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    image_path = db.Column(db.String(255))  # Stores the path relative to 'static/'

    category = db.Column(db.String(50), nullable=False)  # Add this line for category
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('items', lazy=True))

# Check if the file uploaded has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the main index page
@app.route('/')
def index():
    return render_template('home.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('items'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        content = request.form['content']
        sender = session['username']  # Get the sender from the session
        message = Message(sender=sender, content=content)  # Save message with sender
        db.session.add(message)
        db.session.commit()
    
    # Fetch all messages sent by both users
    messages = Message.query.all()
    
    return render_template('chat.html', messages=messages, User=User)  # Pass the User model to the template



# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if the username or email already exists
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        
        if existing_user:
            flash('Username already exists!', 'error')
        elif existing_email:
            flash('Email already in use!', 'error')
        else:
            # Create a new user if neither the username nor email exists
            new_user = User(name=name, username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')



@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']  # Get category from form
        file = request.files['image']
        print("Uploading:", name, description)  # Debugging upload details
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            print("File saved to:", file_path)  # Check the path where file is saved
            new_item = Item(name=name, description=description, category=category, user_id=session['user_id'], image_path=filename)  # Include category
            db.session.add(new_item)
            db.session.commit()
            print("New item added:", new_item)  # Verify the new item's details
            flash('Item added successfully!', 'success')
        else:
            flash('Invalid file type.', 'error')
        return redirect(url_for('items'))
    return render_template('add_item.html', categories=CATEGORIES)  # Pass categories to the template


@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'POST':
        selected_category = request.form.get('category')
        if selected_category:
            all_items = Item.query.filter_by(category=selected_category).all()
        else:
            all_items = Item.query.all()
    else:
        all_items = Item.query.all()
    
    return render_template('items.html', items=all_items, categories=CATEGORIES)

@app.route('/claim_item/<int:item_id>', methods=['GET', 'POST'])
def claim_item(item_id):
    item = Item.query.get(item_id)
    if request.method == 'POST':
        message = request.form['message']
        file = request.files['proof']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['PROOF_FOLDER'], filename)
            file.save(file_path)
            new_claim = Claim(description=message, proof_image_path=filename, item_id=item_id, claimer_id=session['user_id'])
            db.session.add(new_claim)
            db.session.commit()
            flash('Your claim has been submitted.', 'success')
            return redirect(url_for('items'))
        else:
            flash('Invalid file type.', 'error')
    return render_template('claims.html', item=item)

@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    # Check if the user is logged in and owns the item
    if 'user_id' not in session:
        # Handle not logged in error or redirect
        return redirect(url_for('login'))
    
    item = Item.query.get(item_id)
    if item and item.user_id == session['user_id']:
        db.session.delete(item)
        db.session.commit()
        # After deletion, redirect to a suitable page
        return redirect(url_for('items'))
    else:
        # Handle error if item does not exist or user does not own it
        return "Error: Item not found or user not authorized to delete this item", 403

@app.route('/history')
def history():
    if 'user_id' not in session:
        flash('You must be logged in to view this page.', 'error')
        return redirect(url_for('login'))

    # Query the claims along with the associated items and user information
    claims = Claim.query.filter_by(claimer_id=session['user_id']).all()

    return render_template('history.html', claims=claims)



@app.route('/messages')
def messages():
    if 'user_id' not in session:
        flash('You must be logged in to view this page.', 'error')
        return redirect(url_for('login'))
    user_items = Item.query.filter_by(user_id=session['user_id']).all()
    return render_template('messages.html', items=user_items, User=User)  # Pass the User model to the template


@app.route('/update_claim_status/<int:claim_id>/<status>', methods=['POST'])
def update_claim_status(claim_id, status):
    if 'user_id' not in session:
        flash('You must be logged in to perform this action.', 'error')
        return redirect(url_for('login'))
    claim = Claim.query.get(claim_id)
    if claim and claim.item.user_id == session['user_id']:  # Ensure only the item owner can update the status
        if status in ['approved', 'rejected']:  # Validating against accepted status values
            claim.status = status
            db.session.commit()
            flash('Claim status updated successfully.', 'success')
        else:
            flash('Invalid status update.', 'error')
    else:
        flash('You do not have permission to update this claim.', 'error')
    return redirect(url_for('messages'))


# Run the application
if __name__ == "__main__":
    with app.app_context():
     #   db.drop_all()
        db.create_all()
    app.run(debug=True)