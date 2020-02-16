from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)

# setup spacy corpus
import spacy
from spacy.pipeline import EntityRuler

# initialise spacy corpus with additional rules to recognize custom kewords fleet, track, rails etc
def init():
    nlp = spacy.load("en_core_web_sm")
    ruler1 = EntityRuler(nlp)
    pattern1 = [{"label": "FLEET", "pattern": "Fleets"}, {"label": "FLEET", "pattern": "Fleet"},
                {"label": "FLEET", "pattern": "Trucks"}, {"label": "FLEET", "pattern": "Truck"},
                {"label": "FLEET", "pattern": "Rails"}, {"label": "FLEET", "pattern": "Rail"},
                {"label": "FLEET", "pattern": "Ships"}, {"label": "FLEET", "pattern": "Ship"},
                {"label": "FLEET", "pattern": "Cargos"}, {"label": "FLEET", "pattern": "Cargo"}]

    # add the rules to NLP engine
    ruler1.add_patterns(pattern1)
    nlp.add_pipe(ruler1, before='ner')
    return nlp

# Function to convert input text to SQL
def convert_text_sql(text):
    nlp = init()
    text = text.title()
    doc = nlp(text)
    query = u''
    LIST_FLEETS = ['truck', 'trucks', 'rail', 'rails', 'ship', 'ships', 'cargo', 'cargos']
    # extracting the named entities in the text
    for ent in doc.ents:
        exp = ent.text
        print(ent.text, ent.label_)
        exp = exp.lower()
        if exp in LIST_FLEETS:
            query = 'select * from fleet where fleet_type = ' + '\'' + exp.title() + '\''
            return query
        else:
            query = 'select * from fleet'
            return query
    return query

@app.route('/')
@app.route('/Home', methods = ['GET','POST'] )
def Home():
    if request.method == 'POST':
        query = convert_text_sql(request.form['Query'])
        if len(query) > 0:
            conn = sqlite3.connect('fleets.db')
            c = conn.cursor()
            conn.commit()
            print(query)
            c.execute(query)
            rows = c.fetchall()
            for row in rows:
                print(row)
            conn.close()
        return render_template('Tracks.html',len = len(rows) , rows = rows)
    return render_template("Home.html")

@app.route('/Track')
def Track():
    return render_template('Tracks.html')

@app.route('/shipping')
def shipping():
    return render_template('shipping.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/feed',methods = ['GET', 'POST'])
def feed():
    if request.method == 'POST':
        feed_user = request.form
        Name = feed_user['Name']
        email_id = feed_user['Email']
        feed_back = feed_user['feedbacks']
        conn = sqlite3.connect('feedback.db')
        c = conn.cursor()
        command = "INSERT INTO Feedback(Name, EmailID, Feedback) VALUES( ?, ?, ?)"
        vals = (Name,email_id,feed_back)
        c.execute(command,vals)
        conn.commit()
        conn.close()
        return render_template('Thank_you.html')
    return render_template('feedback.html')

@app.route('/Thank_you')
def Thank_you():
    return render_template('Thank_you.html')

if __name__ == "__main__":
    app.run(debug=True)
