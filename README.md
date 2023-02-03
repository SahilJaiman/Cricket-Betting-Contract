# Cricket-Betting-Contract
This is a Tezos based cricket betting smart contract built using SmartPy. It allows users to place bets on winning teams in a cricket match. The match events are added by an admin, and users can place bets on their preferred team. The admin then resolves the bets, and the users who bet correctly receive a proportion of the funds from the losing bets. The contract is transparent and secure, ensuring fairness in the betting process.

## Entry Points

- **addEvent()** \
The addEvent() entry point allows the admin to add a new cricket match event to the contract.
- **placeBet()** \
The placeBet() entry point allows users to place a bet on their preferred team for a specific match event. The entry point takes in two parameters, the event ID and the team name the user wants to bet on. 

- **resolveBet()** \
The resolveBet() entry point allows the admin to resolve a specific match event and distribute the funds to the winning bettors. The entry point takes in two parameters, the event ID and the name of the winning team. The contract checks the bets placed for the event, calculates the winnings for the correct bets, and transfers the funds to the winning users' accounts. This entry point ensures that the betting process is resolved in a fair and transparent manner, and the winnings are distributed accurately to the winning bettors.

## Contract 
Address : KT1BGfekcZLniRiA1CYXcPoVMTP2xnPNC7yV\
TzKT : https://ghostnet.tzkt.io/KT1BGfekcZLniRiA1CYXcPoVMTP2xnPNC7yV/operations/
