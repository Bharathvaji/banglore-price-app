from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import util

app = Flask(__name__)
app.secret_key = 'replace_with_secure_random_key'
users = {}

util.load_saved_artifacts()

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
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid username or password.')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if username in users:
            return render_template('signup.html', error='Username already exists.')
        if password != confirm:
            return render_template('signup.html', error='Passwords do not match.')

        users[username] = {
            'email': email,
            'password': generate_password_hash(password)
        }
        session['username'] = username
        return redirect(url_for('home'))

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
        return render_template('index.html', prediction_text=f"Estimated Price: ₹ {round(price, 2)} Lakhs", username=session['username'])
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}", username=session['username'])

if __name__ == "__main__":
    app.run(debug=True)


