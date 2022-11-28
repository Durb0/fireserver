from sqlalchemy import Column, Integer, Enum, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Session


from . import main
from . import enums
from . import category



class Card(main.Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    position:enums.PositionCard = Column(Enum(enums.PositionCard))
    time_before_trigger = Column(Integer)

    def __repr__(self):
        return f'Card({self.id}, {self.title}, {self.description}, {self.position})'

    def toJson(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'position': self.position.value,
            'time_before_trigger': self.time_before_trigger
        }

class InformationCard(Card):
    __tablename__ = 'information_cards'

    id = Column(Integer, ForeignKey(Card.id), primary_key=True)
    #TODO: add actions

    def __repr__(self):
        return f'InformationCard({self.id})'
    
    def toJson(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'position': self.position.value,
            'time_before_trigger': self.time_before_trigger
        }

association_intervention_category = Table(
    'association_intervention_category', main.Base.metadata,
    Column('category_name', String, ForeignKey(category.Category.name)),
    Column('card_id', Integer, ForeignKey(Card.id))
)

class InterventionCard(Card):
    __tablename__ = 'intervention_cards'

    id = Column(Integer, ForeignKey(Card.id), primary_key=True)
    ratio_success = Column(Integer)
    ratio_critical_success = Column(Integer)
    ratio_critical_failure = Column(Integer)
    categories = relationship("Category", secondary=association_intervention_category)

    def __repr__(self):
        return f'InterventionCard({self.id})'

    def toJson(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'position': self.position.value,
            'time_before_trigger': self.time_before_trigger,
            'ratio_success': self.ratio_success,
            'ratio_critical_success': self.ratio_critical_success,
            'ratio_critical_failure': self.ratio_critical_failure,
            'categories': [category.toJson() for category in self.categories]
        }


class DilemmeCard(Card):
    __tablename__ = 'dilemme_cards'

    id = Column(Integer, ForeignKey(Card.id), primary_key=True)

    def __repr__(self):
        return f'DilemmeCard({self.id})'

    def toJson(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'position': self.position.value,
            'time_before_trigger': self.time_before_trigger
        }

class AssociationNextCard(main.Base):
    __tablename__ = 'association_next_card'

    card_id = Column(Integer, ForeignKey(Card.id), primary_key=True)
    level = Column(Enum(enums.RelationLevel))
    next_card_id = Column(Integer, ForeignKey(Card.id), primary_key=True)


def createSomeCard():

    #create 1 information card, 1 intervention card and 1 dilemme card
    cards = [
        InformationCard(title = 'OPE_TEST', description = 'CRITICAL_SUCCESS', position = enums.PositionCard.END, time_before_trigger = 0),
        InformationCard(title = 'OPE_TEST', description = 'CRITICAL_FAILURE', position = enums.PositionCard.END, time_before_trigger = 0),
        InformationCard(title = 'OPE_TEST', description = 'FAILURE', position = enums.PositionCard.END, time_before_trigger = 2),
        InformationCard(title = 'OPE_TEST', description = 'SUCCESS', position = enums.PositionCard.END, time_before_trigger = 2),
        InformationCard(title = 'OPE_TEST', description = 'REFUSAL', position = enums.PositionCard.END, time_before_trigger = 2),
        InformationCard(title = 'OPE_TEST', description = 'CRITICAL_REFUSAL', position = enums.PositionCard.END, time_before_trigger = 0),
        InterventionCard(title = 'OPE_TEST', description = 'GOGOGO', position = enums.PositionCard.BASE, time_before_trigger = 0, ratio_success = 50, ratio_critical_success = 20, ratio_critical_failure = 50, categories = [category.Category.get('FIRE'), category.Category.get('ROAD_ACCIDENT')]),
    ]

    with Session(main.Engine) as session:
        for card in cards:
            session.add(card)
            print(f'Added {card.title}')
        session.commit()


def createSomeRelation():

    #get id of intervention card with title = 'OPE_TEST'
    with Session(main.Engine) as session:
        intervention_card = session.query(InterventionCard).filter_by(title='OPE_TEST').first()

        #get id of informations cards with title = 'OPE_TEST'
        information_cards = session.query(InformationCard).filter_by(title='OPE_TEST').all()

        for information_card in information_cards:
            print(enums.RelationLevel[information_card.description])
            #create relation between intervention card and informations cards
            session.add(AssociationNextCard(card_id = intervention_card.id, level = enums.RelationLevel[information_card.description], next_card_id = information_card.id))
        session.commit()


def removeOpTest():
    

    #remove all cards with title = 'OPE_TEST' and all 
    with Session(main.Engine) as session:


        intervention_cards = session.query(InterventionCard).filter_by(title='OPE_TEST').all()
        information_cards = session.query(InformationCard).filter_by(title='OPE_TEST').all()

        #remove all relations between intervention cards and informations cards
        for intervention_card in intervention_cards:
            session.query(AssociationNextCard).filter_by(card_id = intervention_card.id).delete()
        
        for information_card in information_cards:
            session.query(AssociationNextCard).filter_by(next_card_id = information_card.id).delete()

        for intervention_card in intervention_cards:
            session.delete(intervention_card)
        session.commit()

        
        for information_card in information_cards:
            session.delete(information_card)
        session.commit()

if __name__ == "__main__":
    removeOpTest()
    createSomeCard()
    createSomeRelation()

