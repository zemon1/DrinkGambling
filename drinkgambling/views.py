from pyramid.view import view_config
from models import DBSession, Blackjack, Users
import random, json
random.seed(6);
shoe = []

@view_config(route_name='home', renderer='index.mak')
def shuffle(request):
    #curUserName = "nick"
    #curUserName = "jeid"
    curUserName = "testAccount"
    
    uAndB = getUserAndBlackjack(curUserName)
    
    curUser = uAndB[0]
    curBlk = uAndB[1]
    
    curBlk = fillShoe(curBlk) 

    print "curUser:", curUser
    print "curBlk:", curBlk
    print "Shoe: ", type(curBlk.shoe) 

    return {'cards': curBlk.shoe}

@view_config(route_name='stand', renderer='json')
def stand(request):
    
    #curUserName = "nick"
    #curUserName = "jeid"
    curUserName = "testAccount"
    
    #Get or make the current user/blackjack game
    uAndB = getUserAndBlackjack(curUserName)
    
    curUser = uAndB[0]
    curBlk = uAndB[1]

    #decode the JSON in the database
    curShoe = json.loads(curBlk.shoe)
    curDealerCards = json.loads(curBlk.dealerCards)

    #print curUser
    #print curBlk

    #get the cards so we can get the scores
    pScore = curBlk.playerScore
    dScore = 0
    
    print "\n"
    
    for card in curDealerCards:
        print "S - B dScore:", dScore
        dScore = addCardToScore(dScore, card, curDealerCards)
        print "S - A dScore:", dScore
    
    print "-------------------------\n"

    #keep grabbing cards until were done
    if dScore == 21:
        done = True
    elif dScore > 16:
        done = True
    else:
        done = False
    

    #play until the dealer hits 17
    while(not done):
        card = curShoe.pop()
        curDealerCards.append(card)

        dScore = addCardToScore(dScore, card, curDealerCards)
        
        print "S - Card:", card
        print "S - running dScore:", dScore

        if dScore > 16:
            done = True        

    
    print "-------------------------\n"

        
    winner = 1 #dealer wins
       
    print "S - pCards:", curBlk.playerCards
    print "S - pScore:", pScore
    print "S - dCards", curDealerCards
    print "S - dScore:", dScore

    #-1 player, 0 tie, 1 dealer
    if pScore > 21:
        winner = 1
    elif dScore > 21:
        winner = -1
    elif pScore == dScore:
        winner = 0
    elif pScore > dScore:
        winner = -1
    else:
        winner = 1

    
    #Update the Blackjack table and json encode the strings
    res = DBSession.query(Blackjack).filter_by(id = curBlk.id).update({"shoe" : json.dumps(curShoe), "dealerCards" : json.dumps(curDealerCards), "playerScore" : 0, "dealerScore" : 0, "canDeal" : 1})
    
    #Result should be 1 meaning 1 row was effected
    #print res
    
    dNames = []
    for card in curDealerCards:
        dNames.append(getCard(card))

    return {"cards": curShoe, "dealerCards" : dNames, "winner": winner}

@view_config(route_name='hit', renderer='json')
def hit(request):
    
    #curUserName = "nick"
    #curUserName = "jeid"
    curUserName = "testAccount"
    
    #Get or make the current user/blackjack game
    uAndB = getUserAndBlackjack(curUserName)
    
    curUser = uAndB[0]
    curBlk = uAndB[1]

    print curBlk

    #decode the JSON in the database
    shoe = json.loads(curBlk.shoe)
    pCards = json.loads(curBlk.playerCards)
    pScore = curBlk.playerScore
    winner = -2

    card = shoe.pop()
    pCards.append(card)
    pScore = addCardToScore(pScore, card, pCards)    
    

    print "H - Card:", card
    print "H - pCards:", pCards
    print "H - pScore:", pScore

    #if you bust, dealer wins
    if pScore > 21:
        winner = 1;
        
        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"shoe" : json.dumps(shoe)
                    , "playerCards" : json.dumps(pCards)
                    , "playerScore" : pScore
                    , "canDeal" : 1
                    , "canStand" : 0
                    , "canHit" : 0
                    , "canSplit" : 0
                    , "canDouble" : 0
                    , "canInsurance" : 0
                    , "canSurrender" : 0
                    })
    else:
        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"shoe" : json.dumps(shoe)
                    , "playerCards" : json.dumps(pCards)
                    , "playerScore" : pScore
                    , "canDeal" : 0
                    , "canStand" : 1
                    , "canHit" : 1
                    , "canSplit" : 0
                    , "canDouble" : 0
                    , "canInsurance" : 0
                    , "canSurrender" : 1
                    })

    
    #Result should be 1 meaning 1 row was effected
    print res
    
    pNames = []
    for card in pCards:
        pNames.append(getCard(card))

    return {"cards": shoe, "playerCards" : pNames, 'winner' : winner}

@view_config(route_name='deal', renderer='json')
def dealCards(request):
    #contact_id = request.POST.get('contact_id', None)
    
    #curUserName = "nick"
    #curUserName = "jeid"
    curUserName = "testAccount"
    winner = -2

    #Get or make the current user/blackjack game
    uAndB = getUserAndBlackjack(curUserName)
    
    curUser = uAndB[0]
    curBlk = uAndB[1]

    #decode the JSON in the database
    curShoe = json.loads(curBlk.shoe)
    curPlayerCards = json.loads(curBlk.playerCards)
    curDealerCards = json.loads(curBlk.dealerCards)
    pScore = curBlk.playerScore
    ins = 0
    split = 0

    print curUser
    print curBlk

    cards = []
    for i in range(0, 4):
        if(len(curShoe) > 0):
            cards.append(curShoe.pop())
            #print curShoe
        else:
            fillShoe(curBlk) 
            cards.append(curShoe.pop())

            #print curShoe
    
    curDealerCards = cards[:2]
    curPlayerCards = cards[2:]
    

    if curDealerCards[1]%100 == 14:
        ins = 1

    if getValue(curPlayerCards[0]) == getValue(curPlayerCards[1]):
        print "Cards:", curPlayerCards
        print "SPLIT!"
        split = 1
    else:
        print "Cards:", curPlayerCards
        print "No Split"

    
    for card in curPlayerCards:
        pScore = addCardToScore(pScore, card, curPlayerCards)
    
    print "pScore:", pScore
    print curDealerCards
    print curPlayerCards

    #if the player has blackjack, they win
    if pScore == 21:
        winner = -1
    
        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"shoe" : json.dumps(curShoe)
                    , "playerCards" : json.dumps(curPlayerCards)
                    , "playerScore" : pScore
                    , "dealerCards" : json.dumps(curDealerCards)
                    , "canDeal" : 1
                    , "canStand" : 0
                    , "canHit" : 0
                    , "canSplit" : 0
                    , "canDouble" : 0
                    , "canInsurance" : 0
                    , "canSurrender" : 0
                    })
    
    else:
        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"shoe" : json.dumps(curShoe)
                    , "playerCards" : json.dumps(curPlayerCards)
                    , "playerScore" : pScore
                    , "dealerCards" : json.dumps(curDealerCards)
                    , "canDeal" : 0
                    , "canStand" : 1
                    , "canHit" : 1
                    , "canSplit" : split
                    , "canDouble" : 1
                    , "canInsurance" : ins
                    , "canSurrender" : 1
                    })


    #Result should be 1 meaning 1 row was effected
    print res
    

    deal = ["BlueBack", getCard(curDealerCards[1]), getCard(curPlayerCards[0]), getCard(curPlayerCards[1])]
    
    print deal

    return {"cards": curShoe, 'dealt': deal, 'winner': winner }

def makeDeck():
    suit = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    deck = []
    for i in range(1,5):
        for card in suit:
            deck.append((i * 100) + card)

    return deck

def fillShoe(black):
    deck = makeDeck()
    print len(deck)#, deck
    if black.shoe == "[]":
        print "Filled"
        shoe = []
        decksInShoe = 6
        for i in range(0, decksInShoe):
            shoe.extend(deck)

        random.shuffle(shoe)
        black.shoe = shoe

        DBSession.commit()
    else:
        print "Looked up"
        shoe = black.shoe

    return DBSession.query(Blackjack).filter_by(id = black.id).first()

def getSuit(card):
    suit = card//100
    
    if suit == 1:
        return ["C", "Clubs"]
    if suit == 2:
        return ["D", "Diamonds"]
    if suit == 3:
        return ["H", "Hearts"]
    if suit == 4:
        return ["S", "Spades"]

def addCardToScore(score, card, allCards):
    hasAce = False
    
    for aCard in allCards:
        if aCard%100 == 14:
            hasAce = True

    value = getValue(card)
    
    if (score + value) > 21 and hasAce:
        if value == 11:
            return score + 1
        else:
            return (score - 10) + value
    else:
        return score + value

def getValue(card):
        value = card%100
        
        print "Card:", card
        print "Value:", value
        print "\n"

        #if the card is higher than a 9 and less than an Ace
        if value > 9 and value < 14:
            return 10
        elif value == 14:
            return 11
        else:
            return value

def getCard(card):
    value = card%100

    #value does not account for Aces and sets it to point value
    if not value == 14:
        cardName = str(getValue(card)) + getSuit(card)[0]
    else:
        cardName = str(14) + getSuit(card)[0]

    return cardName

def getUserAndBlackjack(uName, uGuid=""):
    curUser = None
    curBlk = None
    
    #if Guid is empty use the username
    if uGuid == "":
        userExist = DBSession.query(Users).filter_by(userName = uName).all()
    else:
        userExist = DBSession.query(Users).filter_by(userGuid = uGuid).all()
    
    #If the user doesnt exist make one
    if len(userExist) == 0:
        curUser = Users(uName, userGuid=uGuid)
        DBSession.add(curUser)
        DBSession.commit()
        userExist = DBSession.query(Users).filter_by(userName = uName).all()

        print "Made"
    #If they do, retrieve it
    if len(userExist) == 1: # or curUser != None:
        print "Found"
        curUser = userExist[0]
        userBlk = DBSession.query(Blackjack).filter_by(userId = curUser.id).all()
        #If a game doesnt exist make one 
        if len(userBlk) == 0:

            #Make a game
            curBlk = Blackjack(curUser.id)
            
            #add the game
            DBSession.add(curBlk)
            
            #commit it
            DBSession.commit()
            curBlk = DBSession.query(Blackjack).filter_by(userId = curUser.id).first()
            print "Made"
        elif len(userBlk) == 1:
            print "Found"
            curBlk = userBlk[0]

    if curUser == None or curBlk == None:
        print "Had to recurse, Should never need this"
        return getUserAndBlackjack(uName, uGuid)

    return [curUser, curBlk]
