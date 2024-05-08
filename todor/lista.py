from flask import Blueprint, render_template, request, redirect, url_for, g
from todor.auth import login_required
from .models import Lista, User
from todor import db
bp = Blueprint('lista', __name__, url_prefix='/lista/')



@bp.route('list/')
@login_required
def index():
    listas = Lista.query.all()
    return render_template('lista/index.html', listas = listas)

@bp.route('crear/', methods=('GET', 'POST'))
@login_required
def crear():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        
        lista = Lista(g.user.id, title, desc)
        db.session.add(lista)
        db.session.commit()
        return redirect(url_for('lista.index'))
        
    return render_template('lista/create.html')

def get_lista(id):
    lista = Lista.query.get_or_404(id)
    return lista


@bp.route('update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    
    lista = get_lista(id) 
    
    if request.method == 'POST':  
       
        
        lista.title = request.form['title']
        lista.desc = request.form['desc']
        lista.status = True if  request.form.get('status') == 'on' else False 
             
        db.session.commit()
        
        return redirect(url_for('lista.index'))
    return render_template('lista/update.html', lista = lista)



@bp.route('delete/<int:id>')
@login_required
def delete(id):
    lista = get_lista(id)
    db.session.delete(lista)
    db.session.commit()
    return redirect(url_for('lista.index'))

