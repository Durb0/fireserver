from sqlalchemy import Column, Integer, Enum, String, ForeignKey, Table, and_
from sqlalchemy.orm import relationship, Session


if __name__ != "__main__":
    from . import main
    from . import enums
    from . import category
else:
    import main
    import category
    import enums



class Card(main.Base):
    """
        Cette classe permet de definir une carte

        Attributes:
            id (int): l'id de la carte
            title (str): le titre de la carte
            description (str): la description de la carte
            position (PositionCard): la position de la carte
            time_before_trigger (int): le temps avant declenchement de la carte
    """
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
    """
        Cette classe permet de definir une carte d'information

        Attributes:
            id (int): l'id de la carte
            actions (List[Action]): la liste des actions de la carte
    """
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

# Table d'association entre une carte d'intervention et une categorie 
association_intervention_category = Table(
    'association_intervention_category', main.Base.metadata,
    Column('category_name', String, ForeignKey(category.Category.name)),
    Column('card_id', Integer, ForeignKey(Card.id))
)

class InterventionCard(Card):
    """
        Cette classe permet de definir une carte d'intervention

        Attributes:
            id (int): l'id de la carte
            ratio_success (int): le ratio de succes de la carte
            ratio_critical_success (int): le ratio de succes critique de la carte
            ratio_critical_failure (int): le ratio d'echec critique de la carte
            ratio_critical_refusal (int): le ratio de refus critique de la carte
            categories (List[Category]): la liste des categories de la carte
    """
    __tablename__ = 'intervention_cards'

    id = Column(Integer, ForeignKey(Card.id), primary_key=True)
    ratio_success = Column(Integer)
    ratio_critical_success = Column(Integer)
    ratio_critical_failure = Column(Integer)
    ratio_critical_refusal = Column(Integer)
    categories = relationship("Category", secondary=association_intervention_category)

    def __repr__(self):
        return f'InterventionCard({self.id})'

    def addCategories(self,cats):
        for cat in cats:
            self.categories.append(cat)
    
    def addCategory(self,cat):
        self.categories.append(cat)

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
            'ratio_critical_refusal': self.ratio_critical_refusal,
            'categories': [category.toJson() for category in self.categories]
        }


class DilemmeCard(Card):
    """
        Cette classe permet de definir une carte de dilemme

        Cette classe n'est pas encore implementee

        Attributes:
            id (int): l'id de la carte
    """
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
    """
        Cette classe permet de definir une association entre une carte et une autre carte
    """
    __tablename__ = 'association_next_card'

    card_id = Column(Integer, ForeignKey(Card.id), primary_key=True)
    level = Column(Enum(enums.RelationLevel))
    next_card_id = Column(Integer, ForeignKey(Card.id), primary_key=True)
