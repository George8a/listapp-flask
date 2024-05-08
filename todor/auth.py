from flask import (Blueprint, render_template, request, url_for, redirect, flash, session, g)
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from todor import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('registrar/', methods = ('GET', 'POST'))
def registrar():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User(username, generate_password_hash(password))
        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El usuario {username} ya se encuentra registrado.'
        
        flash(error)
    return render_template('auth/registrar.html')

@bp.route('login/', methods = ('GET', 'POST'))
def login():   
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        error = None
        #validar datos
        user_name = User.query.filter_by(username = username).first()
        if user_name == None:
            error = 'El usuario es incorrecto.'
        elif not check_password_hash(user_name.password, password):            
            error = 'La contraseña es incorrecta'
        
        if error == None:
            session.clear()
            session['user_id'] = user_name.id
        
            return redirect(url_for('lista.index'))
      
      
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**Kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**Kwargs)
    return wrapped_view