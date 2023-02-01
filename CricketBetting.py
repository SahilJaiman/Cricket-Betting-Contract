import smartpy as sp


class CricketBetting(sp.Contract):
    def __init__(self, admin):
        self.init(
            events = sp.big_map(
                tkey = sp.TString, 
                tvalue = sp.TRecord(
                    teamA = sp.TString,
                    teamB = sp.TString,
                    fixedBetAmount = sp.TMutez,
                    totalBetAmount = sp.TMutez,
                    resolved = sp.TBool,
                    bettorsCount = sp.TNat,
                    result = sp.TString,
                    #bets = sp.big_map(tkey = sp.TAddress,tvalue = sp.TString),
                )
            ),
            bets = sp.map(tkey= sp.TRecord(eventId = sp.TString, user = sp.TAddress),tvalue = sp.TString),
            admin = admin
        )
    
    @sp.entry_point
    def addEvent(self, params):
        sp.verify(sp.sender == self.data.admin)
        self.data.events[params.eventId] = sp.record(
            teamA = params.teamA,
            teamB = params.teamB,
            fixedBetAmount = params.fixedBetAmount,
            totalBetAmount = params.totalBetAmount,
            resolved = params.resolved,
            bettorsCount = params.bettorsCount,
            result = params.result,
           
        )
        
    
    
    @sp.entry_point
    def placeBet(self, params):
        sp.verify(sp.sender != self.data.admin)
        sp.verify(self.data.events.contains(params.eventId))
        sp.verify(sp.amount >= self.data.events[params.eventId].fixedBetAmount, "Invalid Amount")
        sp.verify(self.data.bets.contains(sp.record(eventId = params.eventId,user = sp.sender))==False, "Already Betted")
        
        self.data.events[params.eventId].totalBetAmount += self.data.events[params.eventId].fixedBetAmount
        self.data.events[params.eventId].bettorsCount += sp.nat(1)
        #self.data.events[params.eventId].bets[sp.sender] = params.bet
        self.data.bets[sp.record(eventId = params.eventId,user = sp.sender)] = params.bet

        extra_balance = sp.amount - self.data.events[params.eventId].fixedBetAmount
        sp.if extra_balance > sp.mutez(0):
            sp.send(sp.sender, extra_balance)
    
    @sp.entry_point
    def resolveBet(self, params):
        sp.verify(sp.sender == self.data.admin)
        sp.verify(self.data.events.contains(params.eventId))
        
        winningTeam = params.winningTeam
        losingTeam = params.losingTeam
        self.data.events[params.eventId].result = winningTeam+" "+"Won"
        bettorsCount = self.data.events[params.eventId].bettorsCount
        fixedBetAmount = self.data.events[params.eventId].fixedBetAmount
        winnersList = sp.local('winnersList',[])
        losersList = sp.local('losersList',[])
        extra_amount = sp.local('extra_amount',sp.nat(0))
    
    
        sp.for x in self.data.bets.items():
            sp.if x.key.eventId == params.eventId:
                sp.if x.value == params.winningTeam:
                    winnersList.value.push(x.key.user)
                sp.else:
                    losersList.value.push(x.key.user)

        winnersCount = sp.len(winnersList.value)
        losersCount = sp.as_nat(bettorsCount - winnersCount)
        
        sp.if winnersCount > 0 :
            extra_amount = (losersCount * sp.utils.mutez_to_nat(fixedBetAmount))/winnersCount

        totalWinAmount = sp.utils.nat_to_mutez(extra_amount) + fixedBetAmount

        sp.if winnersCount > 0 :
            sp.for user in winnersList.value:
                sp.send(user,totalWinAmount)
        sp.else:
            sp.for user in losersList.value:
                sp.send(user,fixedBetAmount)

        self.data.events[params.eventId].resolved = True
        
        
        
    @sp.add_test(name = "Cricket Betting")
    def test():
        scenario = sp.test_scenario()
        
        admin  = sp.test_account("admin")
        
        alice  = sp.test_account("alice")
        bob  = sp.test_account("bob")
        mike = sp.test_account("mike")
        charles = sp.test_account("charles")
        john = sp.test_account("john")
        
        ob = CricketBetting(admin.address)
        
        scenario += ob

        scenario += ob.addEvent(
             eventId = "Match01",
             teamA = "India",
             teamB = "Pakistan",
             fixedBetAmount = sp.tez(2),
             totalBetAmount = sp.tez(0),
             resolved = False,
             bettorsCount = sp.nat(0),
             result = "undeclared",
            
        ).run(sender = admin)

        scenario += ob.placeBet(
             eventId = "Match01",
             bet = "India"
        ).run(amount = sp.tez(3),sender = alice)

        scenario += ob.placeBet(
             eventId = "Match01",
             bet = "India"
        ).run(amount = sp.tez(5),sender = bob)

        scenario += ob.placeBet(
             eventId = "Match01",
             bet = "India"
        ).run(amount = sp.tez(4),sender = mike)

        scenario += ob.placeBet(
             eventId = "Match01",
             bet = "India"
        ).run(amount = sp.tez(6),sender = charles)

        scenario += ob.placeBet(
             eventId = "Match01",
             bet = "Pakistan"
        ).run(amount = sp.tez(2),sender = john)

        scenario += ob.resolveBet(
             eventId = "Match01",
             winningTeam = "India",
             losingTeam = "Pakistan",
        ).run(sender = admin)

