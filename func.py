import random
from f_database import Card, Engine, InfoCard, InterventionCard, NextCard
from sqlalchemy.orm import Session
from model import  CardType,PositionCard, RelationLevel


def getInterventionBaseCard():
    with Session(Engine) as session:
        basecards = session.query(Card).filter(Card.position == PositionCard.BASE).all()
        #get random card
        card = random.choice(basecards)
        #get intervention card
        intervention_card = session.query(InterventionCard).filter(InterventionCard.card_id == card.id).first()
        print(intervention_card)

def getInfoBaseCard():
    with Session(Engine) as session:
        info_card:InfoCard = session.query(InfoCard).filter(InfoCard.position == PositionCard.BASE).first()
        print(info_card)

def getCardById(id:int):
    with Session(Engine) as session:
        card:Card = session.query(Card).filter(Card.id == id).first()
        if card.type == CardType.INTERVENTION:
            return session.query(InterventionCard).filter(InterventionCard.card_id == card.id).first()
        elif card.type == CardType.INFO:
            return session.query(InfoCard).filter(InfoCard.card_id == card.id).first()
        else:
            return None

def getNextCard(id:int, level:RelationLevel):
    with Session(Engine) as session:
        next_card:NextCard = session.query(NextCard).filter(NextCard.previous_card_id == id, NextCard.level == level).first()
        return getCardById(next_card.next_card_id)


if __name__ == "__main__":
    getInterventionBaseCard()
    getInfoBaseCard()