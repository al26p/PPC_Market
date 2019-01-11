# all of this need to be global variable
var energyNeeded
var energySell
var energyToShare
var energyUndeterminate
Lock energyMutex #to protect the variable upside this line

var energyBought
var external #value in $ of the influence of the external factor on the energy price

var PrixPrec
var PrixActuel

boolean external1
boolean external2
Lock externalMutex #to protect the variable upside this line

def calculatingPrice () :
	while True :
		sleep(Time) # we re-calculate the price each "x" milisecond where x is Time and it's an hard-coded constant
		with  externalMutex:
			if external1 :
				external += cte
				external1 = False
			if external2 :
				external += cte
				external2 = False

		with energyMutex :
			if energyToShare >= energieNeeded
				energyNeeded = 0 #les maisons communistes du voisinage permettent l'autossufisance ! (c'est beau l'URSS...)
				# le surplus est détruit lors de la remise a 0
			else :
				energyNeeded += -energyToShare
				if energyUndeterminate >= energyNeeded :
					energyUndeterminate += -energyNeeded
					energyNeeded = 0 #les maisons socialiste/capitaliste du voisinage permettent l'autossufisance !
					energySell += energyUndeterminate #maintenant qu'on a partager, on vend le surplus
				else :
					energyNeeded += -energyUndeterminate #la demande est importante, toute l'energie indéterminée est donnée


			energyBought = energyNeeded

			PrixPrec = PrixActuel
			PrixActuel = y*PrixPrec + s*energySell + b*energyBought + external #where y s and b are hard-coded constant factor

			energyNeeded = energySell = energyToShare = energyUndeterminate = 0

		energyBought = external = 0

def gettingExternal () :
	if sig == signal.SIGUSR1:
		with externalMutex :
			external1 = True

	if sig == signal.SIGUSR2:
		with externalMutex :
			external2 = True
