import os
from flask import Flask, flash, render_template, redirect, request, session
from flask_app import model
import datetime
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import BooleanField, StringField, SelectField, PasswordField, DateField, TimeField, IntegerField, EmailField, validators
from flask_session import Session
from functools import wraps
from flask_talisman import Talisman
import pyotp
from flask_qrcode import QRcode

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['WTF_CSRF_ENABLED'] = True
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Talisman(app, content_security_policy={
    'default-src': '\'none\'',
    'style-src': ['https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css'],
    'img-src': ['\'self\'', 'data:'],
    'script-src': ['\'unsafe-inline\'','https://cdn.jsdelivr.net/npm/chart.js','https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns']
})
CSRFProtect(app)
Session(app)
QRcode(app)



def login_required(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if not 'user' in session:
      return redirect('/login')
    return func(*args, **kwargs)
  return wrapper


@app.route('/', methods=['GET'])
def home():
    connection = model.connect()
    activity = None
    if 'user' in session:
      user = session['user']
      activity = model.get_status(connection,user)
    basket_list = model.basket_list(connection)
    connection.close()
    return render_template('home.html', basket_list=basket_list, activity=activity)

@app.route('/alldata', methods=['GET'])
def alldata():
    connection = model.connect()
    activity = None
    if 'user' in session:
      user = session['user']
      activity = model.get_status(connection,user)
    basket_list = model.basket_list(connection)
    user_list = model.user_list(connection)
    reservation_list = model.reservation_list(connection)
    connection.close()
    return render_template('alldata.html', activity=activity, basket_list=basket_list, user_list=user_list, reservation_list=reservation_list)


class LoginForm(FlaskForm):
  email = EmailField('email', validators=[validators.DataRequired()])
  password = PasswordField('password', validators=[validators.DataRequired()])


@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    try:
      connection = model.connect()
      user = model.get_user(connection, form.email.data, form.password.data)
      if model.totp_enabled(connection, user):
        session['totp_user'] = user
        return redirect('/totp')
      session['user'] = user
      return redirect('/account')
    except Exception as exception:
      app.log_exception(exception)
  return render_template('login.html', form=form)


@app.route('/logout', methods = ['POST'])
@login_required
def logout():
  session.pop('user')
  flash('Déconnexion réussie !')
  return redirect('/')


class PasswordChangeForm(FlaskForm):
  old_password = PasswordField('old_password', validators=[validators.DataRequired()])
  new_password = PasswordField('new_password', validators=[validators.DataRequired(), 
                                                           validators.EqualTo('password_confirm')])
  password_confirm = PasswordField('password_confirm', validators=[validators.DataRequired()])
  totp_enabled = BooleanField('totp_enabled')


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
  form = PasswordChangeForm()
  connection = model.connect()
  user = session['user']
  activity = model.get_status(connection,user)
  if form.validate_on_submit():
    try:
      connection = model.connect()
      email = session['user']['email']
      model.change_password(connection, email, form.old_password.data, form.new_password.data)
      totp_secret = session['totp_secret'] if form.totp_enabled.data else None
      model.update_totp_secret(connection, session['user']['id'], totp_secret)
      flash('Mot de passe modifié !')
      return redirect('/')
    except Exception as exception:
      app.log_exception(exception)
  totp_secret = pyotp.random_base32()
  session['totp_secret'] = totp_secret
  totp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(
    name=session['user']['email'], issuer_name='Soccer')
  return render_template('change_password.html', activity=activity, form=form, totp_uri=totp_uri)


class UserCreationForm(FlaskForm):
  email = EmailField('email', validators=[validators.DataRequired()])
  password = PasswordField('password', validators=[validators.DataRequired(), 
                                                   validators.EqualTo('confirm')])
  confirm = PasswordField('confirm', validators=[validators.DataRequired()])
  activity = StringField('activity', validators=[validators.DataRequired()])


@app.route('/create_user', methods=['GET', 'POST'])
# @login_required
def create_user():
  form = UserCreationForm()
  activity = None
  if 'user' in session:
    user = session['user']
    connection = model.connect()
    activity = model.get_status(connection,user)
  if form.validate_on_submit():
    try:
      connection = model.connect()
      model.add_user(connection, form.email.data, form.password.data, form.activity.data)
      flash('Nouvel utilisateur créé !')
      return redirect('/')
    except Exception as exception:
      app.log_exception(exception)
  return render_template('create_user.html', activity=activity, form=form)


class TotpForm(FlaskForm):
  totp = StringField('totp', validators=[
     validators.DataRequired(), 
     validators.Length(min=6, max=6)])


@app.route('/totp', methods=['GET', 'POST'])
def totp():
  if 'totp_user' not in session:
    return redirect('/')
  user = session['totp_user']
  connection = model.connect()
  activity = None
  if 'user' in session:
    user = session['user']
    activity = model.get_status(connection,user)
  if not model.totp_enabled(connection, user):
    return redirect('/')
  form = TotpForm()
  if form.validate_on_submit():
    try:
      totp_secret = model.totp_secret(connection, user)
      totp_code = form.totp.data
      if pyotp.TOTP(totp_secret).verify(totp_code):
        session['user'] = user
        return redirect('/')
    except Exception as exception:
      app.log_exception(exception)
  return render_template('totp.html', activity=activity, form=form)

@app.route('/account', methods=['GET'])
@login_required
def account():
  user = session['user']
  connection = model.connect()
  basket_list_user = model.get_panier_user(connection, user)
  basket_commande_user = model.get_commande_user(connection, user)
  activity = model.get_status(connection,user)
  command_todo = model.get_command_todo(connection,user)
  connection.close()
  return render_template('account.html', basket_list_user=basket_list_user, activity=activity, basket_commande_user=basket_commande_user, command_todo=command_todo)

@app.route('/panier/<int:id>', methods=['GET'])
def panier(id):
  activity = None
  connection = model.connect()
  if 'user' in session:
    user = session['user']
    activity = model.get_status(connection,user)
  detail_panier = model.get_panier(connection, id)
  return render_template('panier.html', activity=activity, detail_panier=detail_panier)

@app.route('/panier/r/<string:basket>', methods=['GET'])
def redirect_panier(basket):
  connection = model.connect()
  id = model.get_id(connection, basket)
  url = "/panier/" + str(id)
  return redirect(url)

class BasketForm(FlaskForm):
  title = StringField("Nom du panier", validators=[validators.data_required()])
  information = StringField("Description du panier", validators=[validators.data_required()])
  price = IntegerField("Prix", validators=[validators.DataRequired()])

@app.route('/panier/new', methods=['GET', 'POST'])
@login_required
def new_panier():
  connection = model.connect()
  user = session['user']
  activity = model.get_status(connection,user)
  if activity != 'agriculteur':
    return redirect('/')
  form = BasketForm()
  if form.validate_on_submit():
    title = form.title.data
    information = form.information.data
    price = form.price.data
    model.add_basket(connection, title, information, price, user['email'])
    return redirect('/account')
  return render_template('new_panier.html', activity=activity, form=form)

class CommandForm(FlaskForm):
    basket = SelectField("Panier", validators=[validators.DataRequired()])
    quantity = IntegerField( "Quantité", validators=[validators.DataRequired()], render_kw={"placeholder": "Entrez une quantité"})
    jour = DateField("date", validators=[validators.DataRequired()])

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super(CommandForm, self).__init__(*args, **kwargs)
        self.basket.choices = [(opt['title'], opt['title']) for opt in choices]

@app.route('/command/new', methods=['GET', 'POST'])
@login_required
def new_cmd():
  user = session['user']
  connection = model.connect()
  activity = model.get_status(connection,user)
  form = CommandForm(choices=model.basket_list(connection))
  if form.validate_on_submit():
    basket = form.basket.data
    quantity = form.quantity.data
    jour = form.jour.data
    model.add_reservation(connection, user['email'], basket, quantity, jour)
    return redirect('/account')
  return render_template('new_command.html', activity=activity, form=form)