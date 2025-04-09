#Versus mode pointers
VSCOUNTERS = {
    "match_counter_1": 0x80459F68, # the game checks this one in order to call a character unlock fight
    "match_counter_2": 0x80459F88, # the game checks this one in order to unlock a stage
    "match_counter_3": 0x80459F90, # the game checks this one in order to unlock trophies
    "match_counter_4": 0x8045A114, # this one is shown in vs records in the Records section of main menu
    "match_counter_5": 0x8045A128 # this one includes forfeits (the others do not)
}

# Setting counters 1-4 to a high number (like 25000) can and does allow the 
#   player to do their character unlocks fights after a single vs mode battle
# An option can be provided for this to lessen grinding (or not)