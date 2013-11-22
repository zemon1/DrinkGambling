from pyramid.view import view_config
from models import DBSession, Blackjack, Users
import random, json
random.seed(6);

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

    return {}
@view_config(route_name='double', renderer='json')
def double(request):
    
    #curUserName = "nick"
    #curUserName = "jeid"
    curUserName = "testAccount"
    
    #Get or make the current user/blackjack game
    uAndB = getUserAndBlackjack(curUserName)
    
    curUser = uAndB[0]
    curBlk = uAndB[1]
    
    ver = verify(curBlk, curBlk.canDouble, "double")
    if not ver == -1:
        return ver
    
    print curBlk

    #decode the JSON in the database
    shoe = json.loads(curBlk.shoe)
    pCards = json.loads(curBlk.playerCards)
    dCards = json.loads(curBlk.dealerCards)
    pScore = curBlk.playerScore
    
    curBlk = setFlags(curBlk) 
    winner = -2

    card = shoe.pop()
    pCards.append(card)
    pScore = addCardToScore(pCards)    
    

    print "D - dCards:", dCards
    print "D - Card:", card
    print "D - pCards:", pCards
    print "D - pScore:", pScore
    
    curBlk.shoe = shoe
    curBlk.playerCards = pCards
    curBlk.playerScore = pScore

    #If the player busts we want to reveal the dealer's hidden card
    #   but if they didn't we want to send an empty array back to the client
    #   so they can't cheat.
    passDCards = []
    
    #if you bust, dealer wins
    if pScore > 21:
        winner = 1;
        
        passDCards = dCards

        print "Flip Deal, Inc, Dec"
        #Changes to what can be done
        curBlk.canDeal = 1
        curBlk.canIncrease = 1
        curBlk.canDecrease = 1

        #Update the Blackjack table and json encode the strings
        res = updateBlk(curBlk)

    else:
        print "Flip stand"
        #Changes to what can be done
        curBlk.canStand = 1


        #Update the Blackjack table and json encode the strings
        res = updateBlk(curBlk)
    
    #Result should be 1 meaning 1 row was effected
    print res
    
    pNames = []
    for card in pCards:
        pNames.append(getCard(card))
    
    dNames = []
    for card in passDCards:
        dNames.append(getCard(card))
     

    printFlags(curBlk)

    return {"playerCards" : pNames
            , "dealerCards" : dNames
            , 'winner' : winner
            , "canDeal" : curBlk.canDeal 
            , "canStand" : curBlk.canStand
            , "canHit" : curBlk.canHit
            , "canSplit" : curBlk.canSplit
            , "canDouble" : curBlk.canDouble
            , "canInsurance" : curBlk.canInsurance
            , "canSurrender" : curBlk.canSurrender
            , "canIncrease" : curBlk.canIncrease
            , "canDecrease" : curBlk.canDecrease
            }

@view_config(route_name='surrender', renderer='json')
def surrender(request):
    
    #curUserName = "nick"
    #curUserName = "jeid"
    curUserName = "testAccount"
    
    #Get or make the current user/blackjack game
    uAndB = getUserAndBlackjack(curUserName)
    
    curUser = uAndB[0]
    curBlk = uAndB[1]

    ver = verify(curBlk, curBlk.canSurrender, "surrender")
    if not ver == -1:
        return ver
    
    print curBlk

    curBlk = setFlags(curBlk)

    #FILL IN HERE
    #give back half of their money
    #/FILL IN HERE
    
    curBlk.playerCards = []
    curBlk.dealerCards = []
    curBlk.pScore = 0
    curBlk.dScore = 0
    print "Flip Deal, Inc, Dec"
    #Changes to what can be done
    curBlk.canDeal = 1
    curBlk.canIncrease = 1
    curBlk.canDecrease = 1

    #Update the Blackjack table and json encode the strings
    res = updateBlk(curBlk)
    
    #Result should be 1 meaning 1 row was effected
    print res
    
    printFlags(curBlk)

    return {"canDeal" : curBlk.canDeal 
            , "canStand" : curBlk.canStand
            , "canHit" : curBlk.canHit
            , "canSplit" : curBlk.canSplit
            , "canDouble" : curBlk.canDouble
            , "canInsurance" : curBlk.canInsurance
            , "canSurrender" : curBlk.canSurrender
            , "canIncrease" : curBlk.canIncrease
            , "canDecrease" : curBlk.canDecrease
            }

@view_config(route_name='split', renderer='json')
def split(request):
    
    #curUserName = "nick"
    #curUserName = "jeid"
    curUserName = "testAccount"
    
    #Get or make the current user/blackjack game
    uAndB = getUserAndBlackjack(curUserName)
    
    curUser = uAndB[0]
    curBlk = uAndB[1]

    ver = verify(curBlk, curBlk.canSplit, "split")
    if not ver == -1:
        return ver
    
    print curBlk

    #decode the JSON in the database
    shoe = json.loads(curBlk.shoe)
    pCards = json.loads(curBlk.playerCards)
    pScore = curBlk.playerScore
    
    curBlk = setFlags(curBlk) 

    printFlags(curBlk)

    return {"playerCards" : pNames, 'winner' : winner
            , "canDeal" : curBlk.canDeal 
            , "canStand" : curBlk.canStand
            , "canHit" : curBlk.canHit
            , "canSplit" : curBlk.canSplit
            , "canDouble" : curBlk.canDouble
            , "canInsurance" : curBlk.canInsurance
            , "canSurrender" : curBlk.canSurrender
            , "canIncrease" : curBlk.canIncrease
            , "canDecrease" : curBlk.canDecrease
            }

@view_config(route_name='stand', renderer='json')
def stand(request):
    
    #curUserName = "nick"
    #curUserName = "jeid"
    curUserName = "testAccount"
    
    #Get or make the current user/blackjack game
    uAndB = getUserAndBlackjack(curUserName)
    
    curUser = uAndB[0]
    curBlk = uAndB[1]
    
    ver = verify(curBlk, curBlk.canStand, "stand")
    if not ver == -1:
        return ver

    #decode the JSON in the database
    curShoe = json.loads(curBlk.shoe)
    curDealerCards = json.loads(curBlk.dealerCards)
    #get the cards so we can get the scores
    pScore = curBlk.playerScore
    dScore = 0
    
    curBlk = setFlags(curBlk)
    #print curUser
    #print curBlk
    
    print "\n"
   
    dScore = addCardToScore(curDealerCards)
    print "S - dScore:", dScore
   
    '''
    for card in curDealerCards:
        print "S - B dScore:", dScore
        dScore = addCardToScore(curDealerCards)
        print "S - A dScore:", dScore
    '''

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

        dScore = addCardToScore(curDealerCards)
        
        print "S - Card:", card
        print "S - running dScore:", dScore

        if dScore > 16:
            done = True        

    
    print "-------------------------\n"

        
    winner = 1 #dealer wins
       

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

    print "S - pCards:", curBlk.playerCards
    print "S - pScore:", pScore
    print "S - dCards", curDealerCards
    print "S - dScore:", dScore
    
    curBlk.shoe = curShoe
    curBlk.dealerCards = []
    curBlk.playerCards = []
    curBlk.dealerScore = 0
    curBlk.playerScore = 0
    
    print "Flip Deal, Inc, Dec"
    #Changes to what can be done
    curBlk.canDeal = 1
    curBlk.canIncrease = 1
    curBlk.canDecrease = 1

    #Update the Blackjack table and json encode the strings
    res = updateBlk(curBlk)
    
    #Result should be 1 meaning 1 row was effected
    #print res
    
    dNames = []
    for card in curDealerCards:
        dNames.append(getCard(card))
    
    printFlags(curBlk)

    return {"dealerCards" : dNames, "winner": winner
            , "canDeal" : curBlk.canDeal 
            , "canStand" : curBlk.canStand
            , "canHit" : curBlk.canHit
            , "canSplit" : curBlk.canSplit
            , "canDouble" : curBlk.canDouble
            , "canInsurance" : curBlk.canInsurance
            , "canSurrender" : curBlk.canSurrender
            , "canIncrease" : curBlk.canIncrease
            , "canDecrease" : curBlk.canDecrease
            }

@view_config(route_name='hit', renderer='json')
def hit(request):
    
    #curUserName = "nick"
    #curUserName = "jeid"
    curUserName = "testAccount"
    
    #Get or make the current user/blackjack game
    uAndB = getUserAndBlackjack(curUserName)
    
    curUser = uAndB[0]
    curBlk = uAndB[1]

    ver = verify(curBlk, curBlk.canHit, "hit")
    if not ver == -1:
        return ver
    
    print curBlk

    #decode the JSON in the database
    shoe = json.loads(curBlk.shoe)
    pCards = json.loads(curBlk.playerCards)
    pScore = curBlk.playerScore
    
    print "PCards:", pCards

    curBlk = setFlags(curBlk)        
    winner = -2

    card = shoe.pop()
    pCards.append(card)
    pScore = addCardToScore(pCards)    
    
    print "H - Card:", card
    print "H - pCards:", pCards
    print "H - pScore:", pScore
    
    curBlk.shoe = shoe
    curBlk.playerCards = pCards
    curBlk.playerScore = pScore


    #if you bust, dealer wins
    if pScore > 21:
        winner = 1;
        
        dCards = json.loads(curBlk.dealerCards)
        
        print "Flip Deal, Inc, Dec"
        #Changes to what can be done
        curBlk.canDeal = 1
        curBlk.canIncrease = 1
        curBlk.canDecrease = 1

        #Update the Blackjack table and json encode the strings
        res = updateBlk(curBlk)
    
    else:
        print "Flip stand, hit, Surrender"
        #Changes to what can be done
        curBlk.canStand = 1
        curBlk.canHit = 1
        curBlk.canSurrender = 1

        dCards = []
        dNames = []

        #Update the Blackjack table and json encode the strings
        res = updateBlk(curBlk)
    
    #Result should be 1 meaning 1 row was effected
    print res
    
    pNames = []
    for card in pCards:
        pNames.append(getCard(card))
    
    if len(dCards) > 0:
        dNames = []
        print "DCards:", dCards
        for card in dCards:
            print "Card:", card
            dNames.append(getCard(card))

    printFlags(curBlk)

    return {"playerCards" : pNames, 'winner' : winner
            , "dealerCards" : dNames
            , "canDeal" : curBlk.canDeal 
            , "canStand" : curBlk.canStand
            , "canHit" : curBlk.canHit
            , "canSplit" : curBlk.canSplit
            , "canDouble" : curBlk.canDouble
            , "canInsurance" : curBlk.canInsurance
            , "canSurrender" : curBlk.canSurrender
            , "canIncrease" : curBlk.canIncrease
            , "canDecrease" : curBlk.canDecrease
            }

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

    ver = verify(curBlk, curBlk.canDeal, "deal")
    if not ver == -1:
        return ver
    
    #decode the JSON in the database
    curShoe = json.loads(curBlk.shoe)
    curPlayerCards = getPCards(curBlk)
    curDealerCards = json.loads(curBlk.dealerCards)
    pScore = curBlk.playerScore
    
    #Set all the cans to 0
    curBlk = setFlags(curBlk)

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
        curBlk.canInsurance = 1

    if getValue(curPlayerCards[0]) == getValue(curPlayerCards[1]):
        print "Cards:", curPlayerCards
        print "SPLIT!"
        curBlk.canSplit = 1
    else:
        print "Cards:", curPlayerCards
        print "No Split"

    
    pScore = addCardToScore(curPlayerCards)
    
    print "D - pScore:", pScore
    print "D - pCards:", curPlayerCards
    print curDealerCards, len(curDealerCards)
    print curPlayerCards, len(curPlayerCards)
    
    #Give curBlk it's new values
    curBlk.shoe = curShoe 
    curBlk.dealerCards = curDealerCards 
    curBlk.playerScore = pScore
    putPCards(curBlk, curPlayerCards)
    
    #if the player has blackjack, they win
    if pScore == 21:
        winner = -1
        
        print "Flip Deal, Inc, Dec"
        #Changes to what can be done
        curBlk.canDeal = 1
        curBlk.canIncrease = 1
        curBlk.canDecrease = 1
    
        #Update the Blackjack table and json encode the strings
        res = updateBlk(curBlk)

    else:
        print "Flip stand, hit, Double, Surrender"
        #Changes to what can be done
        curBlk.canStand = 1
        curBlk.canHit = 1
        curBlk.canDouble = 1
        curBlk.canSurrender = 1
                
        #Update the Blackjack table and json encode the strings
        res = updateBlk(curBlk)


    #Result should be 1 meaning 1 row was effected
    print res
    

    deal = ["BlueBack", getCard(curDealerCards[1]), getCard(curPlayerCards[0]), getCard(curPlayerCards[1])]
    
    print deal

    printFlags(curBlk)

    return {"dealt": deal, "winner": winner
            , "canDeal" : curBlk.canDeal 
            , "canStand" : curBlk.canStand
            , "canHit" : curBlk.canHit
            , "canSplit" : curBlk.canSplit
            , "canDouble" : curBlk.canDouble
            , "canInsurance" : curBlk.canInsurance
            , "canSurrender" : curBlk.canSurrender
            , "canIncrease" : curBlk.canIncrease
            , "canDecrease" : curBlk.canDecrease
            }

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
        #black.shoe = json.dumps(shoe)
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

def addCardToScore(cards):
    aceCount = 0
    score = 0 
    
    for card in cards:
        value = getValue(card)
        if card%100 == 14:
            aceCount += 1

        if (score + value) > 21 and aceCount > 0:
                score = (score - 10) + value
                aceCount -= 1
        else:
            score += value

    return score

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

def verify(blk, field, type):
    
    if not field:
        #If you are trying to cheat, dealer wins.
        print "Can't " + type  + " you cheating motherfucker"
        
        #Update the Blackjack table and json encode the strings
        blk.canDeal = 1
        blk.canIncrease = 1
        blk.canDecrease = 1

        updateBlk(blk)

        return {'winner' : 1, 'error' : "If you are found trying to cheat your privileges will be revoked."}
    else:
        return -1

def getPCards(blk):
    cards = json.loads(blk.playerCards)
    return cards[blk.splitFocus]
    
def putPCards(blk, cards):
    allCards = json.loads(blk.playerCards)
    allCards[blk.splitFocus] = cards
    return allCards

def updateBlk(blk):
    """ 
    if type(blk.shoe) == type(""):
        shoe = json.dumps(blk.shoe)
    else:
        shoe = blk.shoe

    if type(blk.playerCards) == type(""):
        playerCards = json.dumps(blk.playerCards)
    else:
        playerCards = blk.playerCards

    if type(blk.dealerCards) == type(""):
        dealerCards = json.dumps(blk.dealerCards)
    else:
        dealerCards = blk.dealerCards
    """

    #Update the Blackjack table and json encode the strings
    res = DBSession.query(Blackjack)\
        .filter_by(id = blk.id)\
        .update({"shoe" : blk.shoe
                , "playerCards" : blk.playerCards
                , "dealerCards" : blk.dealerCards
                , "hiddenCard" : blk.hiddenCard
                , "dealerScore" : blk.dealerScore
                , "playerScore" : blk.playerScore
                , "canDeal" : blk.canDeal
                , "canStand" : blk.canStand
                , "canHit" : blk.canHit
                , "canSplit" : blk.canSplit
                , "canDouble" : blk.canDouble
                , "canInsurance" : blk.canInsurance
                , "canSurrender" : blk.canSurrender
                , "canIncrease" : blk.canIncrease
                , "canDecrease" : blk.canDecrease
                , "splitCount" : blk.splitCount
                , "splitFocus" : blk.splitFocus
                })
    return res 

def setFlags(blk):
    
    #What is allowed to be done here
    blk.canDeal = 0
    blk.canStand = 0
    blk.canHit = 0
    blk.canSplit = 0
    blk.canDouble = 0
    blk.canInsurance = 0
    blk.canSurrender = 0
    blk.canIncrease = 0
    blk.canDecrease = 0
    blk.splitCount = 0
    blk.splitFocus = 0
    
    return blk

def printFlags(blk):

    #What is allowed to be done here
    print "cDeal:", blk.canDeal 
    print "cStand:", blk.canStand 
    print "cHit:", blk.canHit 
    print "cSplit:", blk.canSplit 
    print "cDouble:", blk.canDouble 
    print "cInsurance:", blk.canInsurance 
    print "cSurrender:", blk.canSurrender
    print "cIncrease:", blk.canIncrease 
    print "cDecrease:", blk.canDecrease
    print "cSplitCount:", blk.splitCount
    print "cSplitFocus:", blk.splitFocus

