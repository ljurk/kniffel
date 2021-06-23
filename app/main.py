from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, Api, reqparse
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField, IntegerField, SelectMultipleField, DateTimeField, FieldList, FormField, Form
from wtforms.validators import Optional
from json2table import convert
from datetime import datetime

class AdvandcedGame(Form):
    name = StringField('name')
    nr1= IntegerField('1er', default=0, validators=[Optional()])
    nr2= IntegerField('2er', default=0, validators=[Optional()])
    nr3= IntegerField('3er', default=0, validators=[Optional()])
    nr4= IntegerField('4er', default=0, validators=[Optional()])
    nr5= IntegerField('5er', default=0, validators=[Optional()])
    nr6= IntegerField('6er', default=0, validators=[Optional()])


class Ui(FlaskForm):
    """
    class with all used urls
    """
    spiel = IntegerField('spielId')
    spieler = SelectField('spielerIn')
    date = DateTimeField('Datum', format='%d/%m/%Y %H:%M', default=datetime.now())
    submit = SubmitField('abschicken')
    games = FieldList(FormField(AdvandcedGame), min_entries=3)




format='%d/%m/%Y %H:%M'
# Instantiate the app
app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = "303"


connection = psycopg2.connect( "dbname='kniffel' user='kniffel' host='db' password='docker'")
connection.autocommit = True
cursor = connection.cursor(cursor_factory=RealDictCursor)

def getPlayers():
    spieler = []
    cursor.execute("SELECT * FROM spieler;")
    output = cursor.fetchall()
    for o in output:
        spieler.append((o['id'], o['name']))
    return spieler

@app.route('/', methods=['GET', 'POST'])
def getUiStudent():
    form = Ui()
    form.spieler.choices = getPlayers()

    if form.validate_on_submit():
        app.logger.info(request.form)
        for i, tempGame in enumerate(form.games.entries):

            tempGame = tempGame.form
            sqlCommand = f"INSERT INTO spiel(id, advancedId, spielerId, datum, nr1, nr2, nr3, nr4, nr5, nr6) VALUES({form.spiel.data}, {i}, {form.spieler.data}, TO_TIMESTAMP('{form.date.data.strftime(format)}', 'DD/MM/YYYY HH24:MI'), {tempGame.nr1.data}, {tempGame.nr2.data}, {tempGame.nr3.data}, {tempGame.nr4.data}, {tempGame.nr5.data}, {tempGame.nr6.data});"
            app.logger.info(sqlCommand)
            cursor.execute(sqlCommand)
    #read new entry
    cursor.execute("SELECT spieler.name, spiel.* FROM spiel left join spieler on spiel.spielerId = spieler.id;")
    output = cursor.fetchall()
    return render_template('index.html', form=form, table=convert({'data': output}))



# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
