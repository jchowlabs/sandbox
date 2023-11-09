from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# initializes flask app
app = Flask(__name__)

# hard coded secrets for demo purposes
app.config['SECRET_KEY'] = 'jchowlabs'
app.config['RECAPTCHA_PUBLIC_KEY'] = '< setup from your Google account >'
app.config['RECAPTCHA_PRIVATE_KEY'] = '< setup from your Google account >'
app.config['SESSION_TYPE'] = 'filesystem'

# initializes flask app session
from flask_session import Session
Session(app)

# hard coded username and password for demo purposes
def authenticate_user(username, password):
    return username == 'jason' and password == 'hello123!!'

# login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Login')

# index route for login
@app.route('/', methods=['GET', 'POST'])
def index():

    # if user is already logged in, redirect to dashboard
    form = LoginForm()

    # if user submits form, validate and authenticate
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # if user is authenticated, create session and redirect to dashboard
        if authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))

    return render_template('index.html', form=form)

# dashboard route for authenticated user
@app.route('/dashboard')
def dashboard():

    # if user is logged in, render dashboard
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
