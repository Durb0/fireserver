from flask import render_template
from app import app
import card as card


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/InterventionCards")
def getInterventionCards():
    return card.getInterventionCards().__str__()

@app.route("/InterventionCards/<int:id>")
def getInterventionCard(id):
    return card.getInterventionCard(id).__str__()