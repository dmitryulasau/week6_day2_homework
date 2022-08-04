
from flask import render_template, request, url_for, flash, redirect
from app import app

from flask import render_template, flash, redirect
from .forms import FindPokemon, LoginForm
import requests

from flask_login import current_user, login_user, logout_user, login_required
from app.models import Pokemon, User

from app import db
from app.forms import RegistrationForm

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # user = {'username': 'Kevin or Dylan'}
    form = FindPokemon()

    if request.method =='POST':
        
        name = request.form.get('name')
        url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
        response = requests.get(url)

        if not response.ok:
            error_message = "Please enter a valid name or number (1-905)"
            return render_template('index.html.j2', error=error_message, form=form)
        if not response.json():
            error_message = "We don't have this Pokemon's name"
            return render_template('index.html.j2', error=error_message, form=form)    
        data = response.json()
        
        pokemon_info = []
        
        pokemon_dict = {}
   
        pokemon_dict = {
            'name': data['name'],
            'ability': data['abilities'][0]['ability']['name'],
            'defense': data['stats'][2]['base_stat'],
            'attack': data['stats'][1]['base_stat'],
            'hp': data['stats'][0]['base_stat'],
            'image': data['sprites']['other']['official-artwork']['front_default'],
            'gif': data['sprites']['versions']['generation-v']['black-white']['animated']['front_shiny']
        }

        
        pokemon_info.append(pokemon_dict)

        return render_template('index.html.j2', info=pokemon_info, form=form, user=user)

    return render_template('index.html.j2', title='Home', user=user, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html.j2', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful!')
        return redirect(url_for('login'))
    return render_template('register.html.j2', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
   
    return render_template('user.html.j2', user=user)

# 
@app.route('/', methods=['GET', 'POST'])
@login_required
def poke():
    if request.method == 'POST':
        name = request.form.get('name')
        catched_pokemon = Pokemon(name = name, user_id = current_user.id)
        catched_pokemon.save()
        flash('CATCHED!', 'success')
        return redirect(url_for('index'))
    pokemons = current_user.followed_posts()
    return render_template('index.html.j2', pokemons=pokemons)

