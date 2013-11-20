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

    if not curBlk.canDouble:
        #If you are trying to cheat, dealer wins.
        print "Can't hit you cheating motherfucker"
        
        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"canDeal" : 1 
                    , "canStand" : 0
                    , "canHit" : 0
                    , "canSplit" : 0
                    , "canDouble" : 0
                    , "canInsurance" : 0
                    , "canSurrender" : 0
                    , "canIncrease" : 1
                    , "canDecrease" : 1
                    })
        
        return {'winner' : 1, 'error' : "If you are found trying to cheat your privileges will be revoked."}
    
    print curBlk

    #decode the JSON in the database
    shoe = json.loads(curBlk.shoe)
    pCards = json.loads(curBlk.playerCards)
    dCards = json.loads(curBlk.dealerCards)
    pScore = curBlk.playerScore
    
    #What is allowed to be done here
    cDeal = 0
    cStand = 0
    cHit = 0
    cSplit = 0
    cDouble = 0
    cInsurance = 0
    cSurrender = 0
    cIncrease = 0
    cDecrease = 0
           
    winner = -2

    card = shoe.pop()
    pCards.append(card)
    pScore = addCardToScore(pCards)    
    

    print "D - dCards:", dCards
    print "D - Card:", card
    print "D - pCards:", pCards
    print "D - pScore:", pScore
    
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
        cDeal = 1
        cIncrease = 1
        cDecrease = 1

        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"shoe" : json.dumps(shoe)
                    , "playerCards" : json.dumps(pCards)
                    #, "playerScore" : pScore
                    , "playerScore" : 0
                    , "canDeal" : cDeal 
                    , "canStand" : cStand
                    , "canHit" : cHit
                    , "canSplit" : cSplit
                    , "canDouble" : cDouble
                    , "canInsurance" : cInsurance
                    , "canSurrender" : cSurrender
                    , "canIncrease" : cIncrease
                    , "canDecrease" : cDecrease
                    })
    else:
        print "Flip stand"
        #Changes to what can be done
        cStand = 1


        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"shoe" : json.dumps(shoe)
                    , "playerCards" : json.dumps(pCards)
                    , "playerScore" : pScore
                    , "canDeal" : cDeal 
                    , "canStand" : cStand
                    , "canHit" : cHit
                    , "canSplit" : cSplit
                    , "canDouble" : cDouble
                    , "canInsurance" : cInsurance
                    , "canSurrender" : cSurrender
                    , "canIncrease" : cIncrease
                    , "canDecrease" : cDecrease
                    })
    
    #Result should be 1 meaning 1 row was effected
    print res
    
    pNames = []
    for card in pCards:
        pNames.append(getCard(card))
    
    dNames = []
    for card in passDCards:
        dNames.append(getCard(card))
     

    #What is allowed to be done here
    print "cDeal:", cDeal 
    print "cStand:", cStand 
    print "cHit:", cHit 
    print "cSplit:", cSplit 
    print "cDouble:", cDouble 
    print "cInsurance:", cInsurance 
    print "cSurrender:", cSurrender
    print "cIncrease:", cIncrease 
    print "cDecrease:", cDecrease
    
    return {"playerCards" : pNames
            , "dealerCards" : dNames
            , 'winner' : winner
            , "canDeal" : cDeal 
            , "canStand" : cStand
            , "canHit" : cHit
            , "canSplit" : cSplit
            , "canDouble" : cDouble
            , "canInsurance" : cInsurance
            , "canSurrender" : cSurrender
            , "canIncrease" : cIncrease
            , "canDecrease" : cDecrease
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

    if not curBlk.canSurrender:
        #If you are trying to cheat, dealer wins.
        print "Can't hit you cheating motherfucker"
        
        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"canDeal" : 1 
                    , "canStand" : 0
                    , "canHit" : 0
                    , "canSplit" : 0
                    , "canDouble" : 0
                    , "canInsurance" : 0
                    , "canSurrender" : 0
                    , "canIncrease" : 1
                    , "canDecrease" : 1
                    })
        
        return {'winner' : 1, 'error' : "If you are found trying to cheat your privileges will be revoked."}
    
    print curBlk

    #What is allowed to be done here
    cDeal = 0
    cStand = 0
    cHit = 0
    cSplit = 0
    cDouble = 0
    cInsurance = 0
    cSurrender = 0
    cIncrease = 0
    cDecrease = 0

    #FILL IN HERE
    #give back half of their money
    #/FILL IN HERE
           
    print "Flip Deal, Inc, Dec"
    #Changes to what can be done
    cDeal = 1
    cIncrease = 1
    cDecrease = 1

    #Update the Blackjack table and json encode the strings
    res = DBSession.query(Blackjack)\
        .filter_by(id = curBlk.id)\
        .update({"playerCards" : json.dumps([])
                , "playerScore" : 0
                , "canDeal" : cDeal 
                , "canStand" : cStand
                , "canHit" : cHit
                , "canSplit" : cSplit
                , "canDouble" : cDouble
                , "canInsurance" : cInsurance
                , "canSurrender" : cSurrender
                , "canIncrease" : cIncrease
                , "canDecrease" : cDecrease
                })
    
    #Result should be 1 meaning 1 row was effected
    print res
    
    #What is allowed to be done here
    print "cDeal:", cDeal 
    print "cStand:", cStand 
    print "cHit:", cHit 
    print "cSplit:", cSplit 
    print "cDouble:", cDouble 
    print "cInsurance:", cInsurance 
    print "cSurrender:", cSurrender
    print "cIncrease:", cIncrease 
    print "cDecrease:", cDecrease
    
    return {"canDeal" : cDeal 
            , "canStand" : cStand
            , "canHit" : cHit
            , "canSplit" : cSplit
            , "canDouble" : cDouble
            , "canInsurance" : cInsurance
            , "canSurrender" : cSurrender
            , "canIncrease" : cIncrease
            , "canDecrease" : cDecrease
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

    if not curBlk.canSplit:
        #If you are trying to cheat, dealer wins.
        print "Can't hit you cheating motherfucker"
        
        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"canDeal" : 1 
                    , "canStand" : 0
                    , "canHit" : 0
                    , "canSplit" : 0
                    , "canDouble" : 0
                    , "canInsurance" : 0
                    , "canSurrender" : 0
                    , "canIncrease" : 1
                    , "canDecrease" : 1
                    })
        
        return {'winner' : 1, 'error' : "If you are found trying to cheat your privileges will be revoked."}
    
    print curBlk

    #decode the JSON in the database
    shoe = json.loads(curBlk.shoe)
    pCards = json.loads(curBlk.playerCards)
    pScore = curBlk.playerScore
    
    #What is allowed to be done here
    cDeal = 0
    cStand = 0
    cHit = 0
    cSplit = 0
    cDouble = 0
    cInsurance = 0
    cSurrender = 0
    cIncrease = 0
    cDecrease = 0
            

    #What is allowed to be done here
    print "cDeal:", cDeal 
    print "cStand:", cStand 
    print "cHit:", cHit 
    print "cSplit:", cSplit 
    print "cDouble:", cDouble 
    print "cInsurance:", cInsurance 
    print "cSurrender:", cSurrender
    print "cIncrease:", cIncrease 
    print "cDecrease:", cDecrease
    
    return {"playerCards" : pNames, 'winner' : winner
            , "canDeal" : cDeal 
            , "canStand" : cStand
            , "canHit" : cHit
            , "canSplit" : cSplit
            , "canDouble" : cDouble
            , "canInsurance" : cInsurance
            , "canSurrender" : cSurrender
            , "canIncrease" : cIncrease
            , "canDecrease" : cDecrease
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
    
    if not curBlk.canStand:
        #If you are trying to cheat, dealer wins.
        print "Can't hit you cheating motherfucker"
        
        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"canDeal" : 1 
                    , "canStand" : 0
                    , "canHit" : 0
                    , "canSplit" : 0
                    , "canDouble" : 0
                    , "canInsurance" : 0
                    , "canSurrender" : 0
                    , "canIncrease" : 1
                    , "canDecrease" : 1
                    })
        
        return {'winner' : 1, 'error' : "If you are found trying to cheat your privileges will be revoked."}

    #decode the JSON in the database
    curShoe = json.loads(curBlk.shoe)
    curDealerCards = json.loads(curBlk.dealerCards)
    
    #What is allowed to be done here
    cDeal = 0
    cStand = 0
    cHit = 0
    cSplit = 0
    cDouble = 0
    cInsurance = 0
    cSurrender = 0
    cIncrease = 0
    cDecrease = 0

    #print curUser
    #print curBlk

    #get the cards so we can get the scores
    pScore = curBlk.playerScore
    dScore = 0
    
    print "\n"
    
    for card in curDealerCards:
        print "S - B dScore:", dScore
        dScore = addCardToScore(curDealerCards)
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

        dScore = addCardToScore(curDealerCards)
        
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

    
    print "Flip Deal, Inc, Dec"
    #Changes to what can be done
    cDeal = 1
    cIncrease = 1
    cDecrease = 1

    #Update the Blackjack table and json encode the strings
    res = DBSession.query(Blackjack)\
        .filter_by(id = curBlk.id)\
        .update({"shoe" : json.dumps(curShoe)
                , "dealerCards" : json.dumps(curDealerCards)
                , "playerScore" : 0
                , "dealerScore" : 0
                , "canDeal" : cDeal 
                , "canStand" : cStand
                , "canHit" : cHit
                , "canSplit" : cSplit
                , "canDouble" : cDouble
                , "canInsurance" : cInsurance
                , "canSurrender" : cSurrender
                , "canIncrease" : cIncrease
                , "canDecrease" : cDecrease
                })
    
    #Result should be 1 meaning 1 row was effected
    #print res
    
    dNames = []
    for card in curDealerCards:
        dNames.append(getCard(card))
    
    #What is allowed to be done here
    print "cDeal:", cDeal 
    print "cStand:", cStand 
    print "cHit:", cHit 
    print "cSplit:", cSplit 
    print "cDouble:", cDouble 
    print "cInsurance:", cInsurance 
    print "cSurrender:", cSurrender
    print "cIncrease:", cIncrease 
    print "cDecrease:", cDecrease

    return {"dealerCards" : dNames, "winner": winner
            , "canDeal" : cDeal 
            , "canStand" : cStand
            , "canHit" : cHit
            , "canSplit" : cSplit
            , "canDouble" : cDouble
            , "canInsurance" : cInsurance
            , "canSurrender" : cSurrender
            , "canIncrease" : cIncrease
            , "canDecrease" : cDecrease
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

    if not curBlk.canHit:
        #If you are trying to cheat, dealer wins.
        print "Can't hit you cheating motherfucker"
        
        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"canDeal" : 1 
                    , "canStand" : 0
                    , "canHit" : 0
                    , "canSplit" : 0
                    , "canDouble" : 0
                    , "canInsurance" : 0
                    , "canSurrender" : 0
                    , "canIncrease" : 1
                    , "canDecrease" : 1
                    })
        
        return {'winner' : 1, 'error' : "If you are found trying to cheat your privileges will be revoked."}
    
    print curBlk

    #decode the JSON in the database
    shoe = json.loads(curBlk.shoe)
    pCards = json.loads(curBlk.playerCards)
    pScore = curBlk.playerScore
    
    #What is allowed to be done here
    cDeal = 0
    cStand = 0
    cHit = 0
    cSplit = 0
    cDouble = 0
    cInsurance = 0
    cSurrender = 0
    cIncrease = 0
    cDecrease = 0
            
    winner = -2

    card = shoe.pop()
    pCards.append(card)
    pScore = addCardToScore(pCards)    
    

    print "H - Card:", card
    print "H - pCards:", pCards
    print "H - pScore:", pScore

    #if you bust, dealer wins
    if pScore > 21:
        winner = 1;
        
        print "Flip Deal, Inc, Dec"
        #Changes to what can be done
        cDeal = 1
        cIncrease = 1
        cDecrease = 1

        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"shoe" : json.dumps(shoe)
                    , "playerCards" : json.dumps(pCards)
                    #, "playerScore" : pScore
                    , "playerScore" : 0
                    , "canDeal" : cDeal 
                    , "canStand" : cStand
                    , "canHit" : cHit
                    , "canSplit" : cSplit
                    , "canDouble" : cDouble
                    , "canInsurance" : cInsurance
                    , "canSurrender" : cSurrender
                    , "canIncrease" : cIncrease
                    , "canDecrease" : cDecrease
                    })
    else:
        print "Flip stand, hit, Surrender"
        #Changes to what can be done
        cStand = 1
        cHit = 1
        cSurrender = 1


        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"shoe" : json.dumps(shoe)
                    , "playerCards" : json.dumps(pCards)
                    , "playerScore" : pScore
                    , "canDeal" : cDeal 
                    , "canStand" : cStand
                    , "canHit" : cHit
                    , "canSplit" : cSplit
                    , "canDouble" : cDouble
                    , "canInsurance" : cInsurance
                    , "canSurrender" : cSurrender
                    , "canIncrease" : cIncrease
                    , "canDecrease" : cDecrease
                    })
    
    #Result should be 1 meaning 1 row was effected
    print res
    
    pNames = []
    for card in pCards:
        pNames.append(getCard(card))

    #What is allowed to be done here
    print "cDeal:", cDeal 
    print "cStand:", cStand 
    print "cHit:", cHit 
    print "cSplit:", cSplit 
    print "cDouble:", cDouble 
    print "cInsurance:", cInsurance 
    print "cSurrender:", cSurrender
    print "cIncrease:", cIncrease 
    print "cDecrease:", cDecrease
    
    return {"playerCards" : pNames, 'winner' : winner
            , "canDeal" : cDeal 
            , "canStand" : cStand
            , "canHit" : cHit
            , "canSplit" : cSplit
            , "canDouble" : cDouble
            , "canInsurance" : cInsurance
            , "canSurrender" : cSurrender
            , "canIncrease" : cIncrease
            , "canDecrease" : cDecrease
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

    if not curBlk.canDeal:
        #If you are trying to cheat, dealer wins.
        print "Can't hit you cheating motherfucker"
        
        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"canDeal" : 1 
                    , "canStand" : 0
                    , "canHit" : 0
                    , "canSplit" : 0
                    , "canDouble" : 0
                    , "canInsurance" : 0
                    , "canSurrender" : 0
                    , "canIncrease" : 1
                    , "canDecrease" : 1
                    })
        
        return {'winner' : 1, 'error' : "If you are found trying to cheat your privileges will be revoked."}
    
    #decode the JSON in the database
    curShoe = json.loads(curBlk.shoe)
    curPlayerCards = json.loads(curBlk.playerCards)
    curDealerCards = json.loads(curBlk.dealerCards)
    pScore = curBlk.playerScore
    
    #What is allowed to be done here
    cDeal = 0
    cStand = 0
    cHit = 0
    cSplit = 0
    cDouble = 0
    cInsurance = 0
    cSurrender = 0
    cIncrease = 0
    cDecrease = 0

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
        cInsurance = 1

    if getValue(curPlayerCards[0]) == getValue(curPlayerCards[1]):
        print "Cards:", curPlayerCards
        print "SPLIT!"
        cSplit = 1
    else:
        print "Cards:", curPlayerCards
        print "No Split"

    
    pScore = addCardToScore(curPlayerCards)
    
    print "pScore:", pScore
    print curDealerCards
    print curPlayerCards

    #if the player has blackjack, they win
    if pScore == 21:
        winner = -1
        
        print "Flip Deal, Inc, Dec"
        #Changes to what can be done
        cDeal = 1
        cIncrease = 1
        cDecrease = 1
    
        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"shoe" : json.dumps(curShoe)
                    , "playerCards" : json.dumps(curPlayerCards)
                    , "playerScore" : 0
                    , "dealerCards" : json.dumps(curDealerCards)
                    , "canDeal" : cDeal 
                    , "canStand" : cStand
                    , "canHit" : cHit
                    , "canSplit" : cSplit
                    , "canDouble" : cDouble
                    , "canInsurance" : cInsurance
                    , "canSurrender" : cSurrender
                    , "canIncrease" : cIncrease
                    , "canDecrease" : cDecrease
                    })
    
    else:
        print "Flip stand, hit, Double, Surrender"
        #Changes to what can be done
        cStand = 1
        cHit = 1
        cDouble = 1
        cSurrender = 1
                
        #Update the Blackjack table and json encode the strings
        res = DBSession.query(Blackjack)\
            .filter_by(id = curBlk.id)\
            .update({"shoe" : json.dumps(curShoe)
                    , "playerCards" : json.dumps(curPlayerCards)
                    , "playerScore" : pScore
                    , "dealerCards" : json.dumps(curDealerCards)
                    , "canDeal" : cDeal 
                    , "canStand" : cStand
                    , "canHit" : cHit
                    , "canSplit" : cSplit
                    , "canDouble" : cDouble
                    , "canInsurance" : cInsurance
                    , "canSurrender" : cSurrender
                    , "canIncrease" : cIncrease
                    , "canDecrease" : cDecrease
                    })


    #Result should be 1 meaning 1 row was effected
    print res
    

    deal = ["BlueBack", getCard(curDealerCards[1]), getCard(curPlayerCards[0]), getCard(curPlayerCards[1])]
    
    print deal

    #What is allowed to be done here
    print "cDeal:", cDeal 
    print "cStand:", cStand 
    print "cHit:", cHit 
    print "cSplit:", cSplit 
    print "cDouble:", cDouble 
    print "cInsurance:", cInsurance 
    print "cSurrender:", cSurrender
    print "cIncrease:", cIncrease 
    print "cDecrease:", cDecrease
    
    return {"dealt": deal, "winner": winner
            , "canDeal" : cDeal 
            , "canStand" : cStand
            , "canHit" : cHit
            , "canSplit" : cSplit
            , "canDouble" : cDouble
            , "canInsurance" : cInsurance
            , "canSurrender" : cSurrender
            , "canIncrease" : cIncrease
            , "canDecrease" : cDecrease
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
