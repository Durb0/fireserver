from flask import render_template
from app import app
import f_database


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/InterventionCards")
def getInterventionCards():
    return f_database.getInterventionCards().__str__()

@app.route("/InterventionCards/<int:id>")
def getInterventionCard(id):
    return f_database.getInterventionCard(id).__str__()