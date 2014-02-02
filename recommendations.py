#A dictionary of movie critics and their ratings of a small set of movies.

from math import sqrt



def sim_distance(prefs, person1, person2):
	"""
	Returns a Euclidian distance-based similarity score for person1 and person2
	"""
	#Get the list of shared items
	si = {}
	for item in prefs[person1]:
		if item in prefs [person2]:
			si[item] = 1

	# if they have no ratings in common, return 0
	if len(si) == 0:
		return 0

	# Euclidian distance: Find the SUM of the SQUARES of the DIFFERENCES
	sum_of_squares = sum([pow(prefs[person1][item] - 
						  prefs[person2][item], 2) for item in si])
	return 1 / (1+sqrt(sum_of_squares))



def sim_pearson(prefs, p1, p2):
	"""
	Returns the Pearson correlation coefficient for two people -- p1 and p2
	"""
	#Get the list of mutually rated items
	si = {}
	for item in prefs[p1]:
		if item in prefs[p2]:
			si[item] = 1
	
	# Find the number of elements
	n = len(si)

	# If the have no ratings in common, return 0
	if n == 0:
		return 0

	# Add up all the preferences
	sum1 = sum([prefs[p1][it] for it in si])
	sum2 = sum([prefs[p2][it] for it in si])

    # Sum up the squares
	sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
	sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # Sum up the products
	pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    #Calculate Pearson score
	num = pSum - (sum1 * sum2 / n)
	den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
	if den == 0:
		return 0
	r = num/den

	return r


def topMatches(prefs, person, n=5, similarity=sim_pearson):
	"""
	Returns the best-matched persons for a given person from the prefs dictionary.
	Number of results and similarity function are optional params.
	"""
	scores = [(similarity(prefs, person, other), other) for other in 
			   prefs if other != person]

	# Sort the list so the highest scores appear at the top
	scores.sort()
	scores.reverse()
	return scores[0:n]


def getRecommendations(prefs, person, similarity=sim_pearson):
	"""
	Get recommendations for a person by using a weighted average
	of every other user's similarity rankings.
	For any given item I haven't rated yet, other person's similarities are multiplied 
	by their rating for that item, those scores are then summed and averaged. 
	
	rankings then returns a list of the highest-average-scored items. 
	"""
	totals = {}
	simSums = {}
	for other in prefs:
		#don't compare me to myself
		if other == person: continue
		sim = similarity(prefs, person, other)

		#ignore scores of zero or lower
		if sim <= 0: continue
		for item in prefs[other]:

			#only score the items I haven't rated yet
			if item not in prefs[person] or prefs[person][item] == 0:
				#Similarity * score
				totals.setdefault(item, 0)
				totals[item] += prefs[other][item] * sim
				#Sum of the similarities
				simSums.setdefault(item, 0)
				simSums[item] += sim
	#Create the normalized list
	rankings = [((total / simSums[item]), item) for item, total in totals.items()]

	#Return the sorted list
	rankings.sort()
	rankings.reverse()
	return rankings


######## Now we match the products themselves ########

def transformPrefs(prefs):
	"""
	Returns a dictionary of {prodcuts: {person: rating}} that can be
	used with the same set of functions for product similarity discovery
	"""
	result = {}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item, {})

			#Flip item and person
			result[item][person]=prefs[person][item]
	return result








