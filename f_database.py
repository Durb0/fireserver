from sqlalchemy import Column, Integer, Enum, String, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, declarative_base, Session
from model import BonusType, CardType, RessourceType, RelationLevel, PositionCard

Base = declarative_base()
Engine = create_engine('sqlite:///db.sqlite3')


class Ressource(Base):
    __tablename__ = 'ressources'

    
    id = Column(Integer, primary_key=True)
    type = Column(Enum(RessourceType))
    quantity = Column(Integer)
    info_card_id = Column(Integer, ForeignKey('info_cards.id'))

    def __repr__(self):
        return f'Ressource({self.id}, {self.name}, {self.type}, {self.quantity})'

class Bonus(Base):
    __tablename__ = 'bonus'

    id = Column(Integer, primary_key=True)
    type = Column(Enum(BonusType))
    value = Column(Integer)
    intervention_card_id = Column(Integer, ForeignKey('intervention_cards.id'))

    def __repr__(self):
        return f'Bonus({self.id}, {self.type}, {self.value}, {self.intervention_card_id})'


class NextCard(Base):
    __tablename__ = 'next_cards'

    previous_card_id    = Column(ForeignKey('cards.id'), primary_key = True)
    level               = Column(Enum(RelationLevel))
    next_card_id        = Column(ForeignKey('cards.id'), primary_key = True)
    next_card = relationship("Card", foreign_keys=[next_card_id])

    def __repr__(self):
        return f'NextCard({self.previous_card_id}, {self.level}, {self.next_card_id})'

class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    type = Column(Enum(CardType))
    position = Column(Enum(PositionCard))
    next_card = relationship("NextCard", foreign_keys=[NextCard.previous_card_id])

    def __repr__(self):
        return f'Card({self.id}, {self.title}, {self.description}, {self.type}, {self.position})'


class InfoCard(Base):
    __tablename__ = 'info_cards'
    id = Column(Integer, primary_key=True,autoincrement=True, unique=True)
    card_id = Column(Integer,ForeignKey('cards.id'))
    card = relationship("Card", backref="info_cards")
    gain = relationship("Ressource", backref="info_cards")

    def __repr__(self):
        return f'InfoCard({self.id}, {self.card_id}, {self.gain_popularity})'

    

class InterventionCard(Base):
    __tablename__ = 'intervention_cards'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    card_id = Column(Integer, ForeignKey('cards.id'))
    card = relationship("Card", backref="intervention_cards")
    bonus = relationship("Bonus", backref="intervention_cards")
    time = Column(Integer)
    #the difficulty is between 0 and 100
    difficulty = Column(Integer)

    def __repr__(self):
        return f'InterventionCard:card : {self.card}, bonus : {self.bonus}, time : {self.time}, difficulty : {self.difficulty}'
    

if __name__ == "__main__":
    Base.metadata.create_all(Engine)

    with Session(Engine) as session:
        base_card = InterventionCard(
            card = Card(
                title = "Base card",
                description = "Base card description",
                type = CardType.INTERVENTION,
                position = PositionCard.BASE
            ),
            time = 10,
            difficulty = 10,
            bonus = [
                Bonus(
                    type = BonusType.FIRE,
                    value = 10
                ),
                Bonus(
                    type = BonusType.SPEED,
                    value = 10
                )]
        )

        session.add(base_card)
        session.commit()

        good_ending = InfoCard(
            card = Card(
                title = "Good ending",
                description = "Good ending description",
                type = CardType.INFO,
                position = PositionCard.END
            ),
            gain = [
                Ressource(
                    type = RessourceType.POPULARITY,
                    quantity = 10
                ),
                Ressource(
                    type = RessourceType.GROSPIMPON,
                    quantity = 10
                )]
        )

        bad_ending = InfoCard(
            card = Card(
                title = "Bad ending",
                description = "Bad ending description",
                type = CardType.INFO,
                position = PositionCard.END
            ),
            gain = [
                Ressource(
                    type = RessourceType.POPULARITY,
                    quantity = -10
                )]
        )

        session.add(good_ending)
        session.add(bad_ending)
        session.commit()

        base_card.card.next_card = [
            NextCard(
                level = RelationLevel.GOOD,
                next_card = good_ending.card
            ),
            NextCard(
                level = RelationLevel.BAD,
                next_card = bad_ending.card
            )
        ]

        session.commit()

        print(session.query(Card).all())
