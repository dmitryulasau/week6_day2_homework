from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    pokemon = db.relationship('Pokemon', backref='master', lazy='dynamic')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        db.session.add(self) # add the userr to the session
        db.session.commit() # save the stuff in the session to the database
    
    def delete(self):
        db.session.delete(self) # remove the user from the session
        db.session.commit() # save the stuff in the session to the database

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# POKEMON ######################################################################
class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    # ability = db.Column(db.String(50))
    # defense = db.Column(db.Integer)
    # attack = db.Column(db.Integer)
    # hp = db.Column(db.Integer)
    # gif = db.Column(db.String(500))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # def __repr__(self):
    #     return f'<Pokemon: {self.id} | {self.name} | ABILITY -{self.ability} | DEFENSE - {self.defense} | ATTACK - {self.attack} '
    
    def __repr__(self):
        return '<Pokemon {}>'.format(self.name)
   
        
    def save(self):
        db.session.add(self) 
        db.session.commit() 

    def delete(self):
        db.session.delete(self) 
        db.session.commit() 