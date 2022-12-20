from typing import List
from model.main import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from sqlalchemy import and_

import random


def getCategories():
    """
        Cette fonction permet de recuperer la liste des categories

        Returns:
            List[Category]: la liste des categories
    """
    from model.category import Category
    list = []
    with Session(Engine) as session:
        categories = session.query(Category).all()
        for category in categories:
            list.append(category.toJson())
    return list


def getTruck(str):
    """
        Cette fonction permet de recuperer un camion en fonction de son nom

        Args:
            str (str): le nom du camion

        Returns:
            Truck: le camion
    """
    from model.truck import Truck

    with Session(Engine) as session:
        truck = session.query(Truck).filter(Truck.name == str).first()
        return truck.toJson()


def getListOfTruckName():
    """
        Cette fonction permet de recuperer la liste des noms des camions

        Returns:
            List[str]: la liste des noms des camions
    """
    from model.truck import Truck

    with Session(Engine) as session:
        trucks:List[Truck] = session.query(Truck).all()
        return [truck.name for truck in trucks]

def getListOfTruckFile():
    """
        Cette fonction permet de recuperer la liste des noms des fichiers des camions

        Returns:
            List[str]: la liste des noms des fichiers des camions
    """
    import os
    return [f.split('.')[0] for f in os.listdir('static/truck') if os.path.isfile(os.path.join('static/truck', f))]

def drawInterventionBaseCard(blackList):
    """
        Cette fonction permet de tirer une carte de base d'intervention en fonction de la liste des cartes deja tirees

        Args:
            blackList (List[str]): la liste des cartes deja tirees

        Returns:
            InterventionCard: la carte tiree
    """
    from model.card import InterventionCard
    from model.enums import PositionCard

    with Session(Engine) as session:
        basecards = session.query(InterventionCard).filter(
            and_(
                InterventionCard.position == PositionCard.BASE,
                InterventionCard.title.notin_(blackList)
            )
            ).order_by(func.random()).all()
        if len(basecards) == 0:
            return None
        card = random.choice(basecards) 
        return card.toJson()

def drawNextCard(id:int, level:int):
    """
        Cette fonction permet de tirer une carte suivante en fonction de la carte precedente et du niveau de relation
        
        Args:
            id (int): l'id de la carte precedente
            level (int): le niveau de relation
        
        Returns:
            Card: la carte tiree

    """
    from model.card import InterventionCard, AssociationNextCard, InformationCard, DilemmeCard
    from model.enums import RelationLevel

    lvl = RelationLevel.intToStr(level)
    with Session(Engine) as session:
        nextCards = session.query(AssociationNextCard).filter(AssociationNextCard.card_id == id, AssociationNextCard.level == lvl).all()
        print("next cards", nextCards)
        if len(nextCards) == 0:
            return None, None
        nextCard = random.choice(nextCards)
        card = session.query(InterventionCard).filter(InterventionCard.id == nextCard.next_card_id).first() or session.query(InformationCard).filter(InformationCard.id == nextCard.next_card_id).first() or session.query(DilemmeCard).filter(DilemmeCard.id == nextCard.next_card_id).first()
        return card.toJson(), card.__tablename__