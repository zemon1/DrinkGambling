from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Unicode, String, ForeignKey, Column, LargeBinary
from sqlalchemy.orm import scoped_session, sessionmaker, relationship

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    userGuid = Column(String(128))
    userName = Column(String(128))
    profit = Column(Integer)
    blackjack = relationship("Blackjack")

    def __init__(self, userName, userGuid="", profit=0):
        self.userGuid = userGuid
        self.userName = userName
        self.profit = profit

    def __str__(self):
        string = "Users: {" + str(self.id) + ": " + str(self.userGuid) + ", " + str(self.userName) + " - " + str(self.profit) + "}"
        return string

class Blackjack(Base):
    __tablename__ = 'blackjack'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('users.id'))
    shoe = Column(LargeBinary)
    playerCards = Column(LargeBinary)
    dealerCards = Column(LargeBinary)
    hiddenCard = Column(Integer)
    dealerScore = Column(Integer)
    playerScore = Column(Integer)
    canDeal = Column(Integer)
    canStand = Column(Integer)
    canHit = Column(Integer)
    canSplit = Column(Integer)
    canDouble = Column(Integer)
    canInsurance = Column(Integer)
    canSurrender = Column(Integer)

    def __init__(self, userId, shoe=[], playerCards=[], dealerCards=[]):
        self.userId = userId
        self.shoe = shoe
        self.playerCards = playerCards
        self.dealerCards = dealerCards
        self.hiddenCard = 1 
        self.dealerScore = 0 
        self.playerScore = 0
        self.canDeal = 1
        self.canStand = 0
        self.canHit = 0
        self.canSplit = 0
        self.canDouble = 0
        self.canInsurance = 0
        self.canSurrender = 0

    def __str__(self):
        string = "Blackjack: {" + str(self.id) + ": " 
        string += str(self.userId) + ",\n " 
        string += str(self.shoe) + "\nCanDeal: " 
        string += str(self.canDeal) + "\nCanStand: "
        string += str(self.canStand) + "\nCanHit: "
        string += str(self.canHit) + "\nCanSplit: "
        string += str(self.canSplit) + "\nCanDouble: "
        string += str(self.canDouble) + "\nCanInsurance: "
        string += str(self.canInsurance) + "\nCanSurrender: "
        string += str(self.canSurrender) + "\nPC: "
        string += str(self.playerCards) + "\nDC: " 
        string += str(self.dealerCards) + "\nDS: "
        string += str(self.dealerScore) + "\nPS: "
        string += str(self.playerScore) + "\nHC: "
        string += str(self.hiddenCard) + "}"
        return string


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.drop_all()
    Base.metadata.create_all(engine, checkfirst=False)
    DBSession.commit()
