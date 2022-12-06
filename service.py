from typing import List
from model.main import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

import random

def getCategories():
    from model.category import Category
    list = []
    with Session(Engine) as session:
        categories = session.query(Category).all()
        for category in categories:
            list.append(category.toJson())
    return list


def getTruck(str):
    from model.truck import Truck

    with Session(Engine) as session:
        truck = session.query(Truck).filter(Truck.name == str).first()
        return truck.toJson()


def getListOfTruckName():
    from model.truck import Truck

    with Session(Engine) as session:
        trucks:List[Truck] = session.query(Truck).all()
        return [truck.name for truck in trucks]

def getListOfTruckFile():
    #return the list of truck in static/truck
    import os
    return [f.split('.')[0] for f in os.listdir('static/truck') if os.path.isfile(os.path.join('static/truck', f))]

def drawInterventionBaseCard():
    from model.card import InterventionCard
    from model.enums import PositionCard

    with Session(Engine) as session:
        card = session.query(InterventionCard).filter(InterventionCard.position == PositionCard.BASE).order_by(func.random()).first()
        return card.toJson()

def drawNextCard(id:int, level:int):
    from model.card import InterventionCard, AssociationNextCard, InformationCard, DilemmeCard
    from model.enums import PositionCard, RelationLevel

    lvl = RelationLevel.intToStr(level)
    with Session(Engine) as session:
        nextCards = session.query(AssociationNextCard).filter(AssociationNextCard.card_id == id, AssociationNextCard.level == lvl).all()
        nextCard = random.choice(nextCards)
        #the card can be an interventionCard, a InformationCard or a DilemmeCard
        card = session.query(InterventionCard).filter(InterventionCard.id == nextCard.next_card_id).first() or session.query(InformationCard).filter(InformationCard.id == nextCard.next_card_id).first() or session.query(DilemmeCard).filter(DilemmeCard.id == nextCard.next_card_id).first()
        return card.toJson(), card.__tablename__



if __name__ == "__main__":
    print(getCategories())
    print('###################################"')
    print(drawInterventionBaseCard())
    print('###################################"')
    print(getTruck('VSAV'))