from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instruments.db'

db = SQLAlchemy(app)

# TABLE
class Instrument(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    price = db.Column('price', db.Float)

    # PARAMETERS
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f'{self.name} --> R$ {self.price}'


# APP

# READ
@app.route('/')
def index():
    instruments = Instrument.query.all()
    return render_template('index.html', instruments=instruments)


# CREATE
@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        instrument = Instrument(request.form['name'], request.form['price'])
        db.session.add(instrument)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


# DELETE
@app.route('/delete/<int:id>')
def delete(id):
    with db.session as session:
        instrument = session.query(Instrument).get(id)
        session.delete(instrument)
        session.commit()
    return redirect(url_for('index'))

# UPDATE
@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    instrument = Instrument.query.get(id)
    if request.method == 'POST':
        instrument.name = request.form['name']
        instrument.price = request.form['price']
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('edit.html', instrument=instrument)


if __name__ == '__main__':    
    with app.app_context():
        db.create_all()
        app.run(debug=True)