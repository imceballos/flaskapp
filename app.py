from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms_fields import  *
import json

app = Flask(__name__)
app.secret_key ='replace_later'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/piezas.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    largo = db.Column(db.String(200))
    diametro = db.Column(db.String(200))
    cantidad = db.Column(db.String(200))
    proyecto = db.Column(db.String(200))
    etiqueta = db.Column(db.String(200))
    fecha = db.Column(db.String(200))
    done = db.Column(db.Boolean)


@app.route('/')
def home():
    reg_form = RegistrationForm()
    tasks = Task.query.all()
    return render_template('index.html', tasks = tasks, form = reg_form)

@app.route('/create-task', methods = ['POST'])
def create():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        task = Task(largo = request.form['largo'], diametro = request.form['diametro'], 
                    cantidad = request.form['cantidad'], proyecto = request.form['proyecto'],
                    etiqueta = request.form['etiqueta'], fecha = request.form['fecha'], done = False)
        db.session.add(task)
        db.session.commit()
    else:
        flash('{}'.format(reg_form.errors))
    return redirect(url_for('home'))


@app.route('/done/<id>')
def done(id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/donenew/<fecha>/<proyecto>/<diametro>/<id>')
def donenew(fecha, proyecto, diametro, id):
    task = Task.query.filter_by(id=int(id)).first()
    task.done = not(task.done)
    db.session.commit()
    return redirect(url_for('viewproyect_diam', fecha = fecha, proyecto = proyecto, diametro = diametro))

@app.route('/delete/<id>')
def delete(id):
    task = Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/deletef/<fecha>')
def delete_fecha(fecha):
    task = Task.query.filter_by(fecha= fecha).delete()
    db.session.commit()
    return redirect(url_for('filter'))

@app.route('/deletefp/<fecha>/<proyecto>')
def delete_fecha_proy(fecha, proyecto):
    task = Task.query.filter_by(fecha= fecha, proyecto = proyecto).delete()
    db.session.commit()
    return redirect(url_for('view', fecha = fecha))

@app.route('/deletefpd/<fecha>/<proyecto>/<diametro>')
def delete_fecha_proy_diam(fecha, proyecto, diametro):
    task = Task.query.filter_by(fecha = fecha, proyecto = proyecto, diametro = diametro).delete()
    db.session.commit()
    return redirect(url_for('viewproyect', fecha = fecha, proyecto = proyecto))

@app.route('/deletefpdi/<fecha>/<proyecto>/<diametro>/<id>')
def delete_fecha_proy_diam_id(fecha, proyecto, diametro, id):
    task = Task.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('viewproyect_diam', fecha = fecha, proyecto = proyecto, diametro = diametro))

@app.route('/filter')
def filter():
    task = Task.query.with_entities(Task.fecha).filter_by(done = False).distinct()
    return render_template('filter.html', filter = task)

@app.route('/filter/view/<fecha>')
def view(fecha):
    task = Task.query.with_entities(Task.proyecto).filter_by(fecha = fecha, done = False).distinct()
    return render_template('selected.html', selected = task, fecha = fecha)


@app.route('/filter/view/<fecha>/<proyecto>')
def viewproyect(fecha, proyecto):
    task = Task.query.with_entities(Task.diametro).filter_by(proyecto = proyecto, fecha = fecha, done = False).distinct()
    return render_template('selected_proy.html', selected = task, proyecto = proyecto, fecha = fecha)

@app.route('/filter/view/<fecha>/<proyecto>/<diametro>')
def viewproyect_diam(fecha, proyecto, diametro):
    task = Task.query.filter_by(proyecto = proyecto, fecha = fecha, diametro = diametro, done = False)
    return render_template('selected_proy_diam.html', selected = task)


if __name__ =='__main__':
    app.run(debug = True)