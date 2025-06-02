from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import urllib.parse
import util

# --- MongoDB Setup ---
username = "bharathvaji57"
password = urllib.parse.quote_plus("Bharathvaji@123")  # Escape special chars like @
uri = f"mongodb+srv://{username}:{password}@cluster0.bsse3s7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)
db = client["user_db"]
users = db["users"]  # ✅ MongoDB collection
uri = os.environ.get("MONGO_URI")


# --- Flask Setup ---
app = Flask(__name__)
app.secret_key = 'replace_with_secure_random_key'

util.load_saved_artifacts()

# --- Routes ---

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('home'))

        return render_template('login.html', error='Invalid username or password.')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if users.find_one({'username': username}):
            return render_template('signup.html', error='Username already exists.')

        hashed_pw = generate_password_hash(password)
        users.insert_one({'username': username, 'password': hashed_pw})

        # Debug: Print all users
        print("All users in the DB:")
        for user in users.find():
            print(user)

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        sqft = float(request.form['sqft'])
        bath = int(request.form['bath'])
        bhk = int(request.form['bhk'])
        location = request.form['location']

        price = util.predict_price(location, sqft, bath, bhk)

        return render_template('index.html',
                               prediction_text=f"Estimated Price: ₹ {round(price, 2)} Lakhs",
                               username=session['username'])

    except Exception as e:
        return render_template('index.html',
                               prediction_text=f"Error: {str(e)}",
                               username=session['username'])

# --- Run ---
if __name__ == "__main__":
    app.run(debug=True)
