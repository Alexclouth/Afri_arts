from flask import Flask, render_template, redirect, url_for, flash
from forms import SignUpForm, SignInForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # Here you would add code to create a new user in your database
        flash('Account created successfully!', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html', form=form)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        # Here you would add code to validate and sign in the user
        flash('Signed in successfully!', 'success')
        return redirect(url_for('dashboard'))  # Assuming you have a dashboard route
    return render_template('signin.html', form=form)

@app.route('/dashboard')
def dashboard():
    # Replace with your dashboard logic
    return 'Welcome to your dashboard!'

if __name__ == '__main__':
    app.run(debug=True)

