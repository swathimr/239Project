from math import sqrt
from itertools import imap

#caluclates euclidean distance and the correlation

def similarityDistance(data,person1,person2):
	disimiliarFlag = True
	for place in data[person1]:
		if place in data[person2]:
			disimiliarFlag = False
	if(disimiliarFlag):
		return 0

	distance = 0
	for place in data[person1]:
		if place in data[person2]:
			distance += (data[person1][place]-data[person2][place])*(data[person1][place]-data[person2][place])
	if distance != 0:
		return float(1) / float(distance)
	else:
		return 0

# Finds similarity between users/places
# calls similarity to calculate euclidean
def mostSimilar(data,person1):
	persons = data.keys()

	scores = {}
	for person in persons:
		if(person!=person1):
			thisDistance = similarityDistance(data,person1,person)
			if thisDistance > 0:
				scores[person] = thisDistance

	scores=sorted(scores.items(), key=lambda scores:scores[1])
	return scores[:4]


def pearsonDistance(data, person1, person2):
	disimiliarFlag = True

	for movie1 in data[person1]:
		if movie1 in data[person2]:
			disimiliarFlag = False

	si={}
	for item in data[person1]:
		if item in data[person2]:
			si[item] = 1
	n=len(si)

	if(disimiliarFlag):
		return 0

	#sum1 = sum([data[person1][movie] for movie in si])
	#sum2 = sum([data[person2][movie] for movie in si])

	x=[data[person1][movie] for movie in si]
	y=[data[person2][movie] for movie in si]

	sum1 = float(sum(x))
	sum2 = float(sum(y))

	sumSquares1 = sum(map(lambda x: pow(x, 2), x))
	sumSquares2 = sum(map(lambda x: pow(x, 2), y))

	pSum = sum(imap(lambda x, y: x * y, x, y))
	#pSum = sum([data[person2][movie]*data[person1][movie] for movie in si])

	num = pSum -(sum1*sum2/n)
	den=sqrt((sumSquares1-pow(sum1,2)/n)*(sumSquares2-pow(sum2,2)/n))
	#den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)
	if(den==0): return 0
	return num/den


def getListOfPlaces(data):
	listOfUsers = data.keys()
	listOfPlaces = []
	for user in listOfUsers:
		for place in data[user].keys():
			listOfPlaces.append(place)

	listOfPlaces = list(set(listOfPlaces))
	return listOfPlaces


def flipPersonToPlaces(data):
	places = getListOfPlaces(data)
	result = {}
	for plc in places:
		thisResult = {}
		for person in data.keys():
			if plc in data[person].keys():
				thisResult[person] = data[person][plc]
		result[plc] = thisResult
	return result

def computeItemSimilarities(data):

	itemSimiliarty = {}
	for place in data.keys():
			itemSimiliarty[place] = mostSimilar(data,place)
	return itemSimiliarty


def getRecommendations(data,person):
	places = getListOfPlaces(data)
	unWatchedPlaces = []
	for place in places:
		if place not in data[person].keys():
			unWatchedPlaces.append(place)


	placeRecommendations = {}
	for place in unWatchedPlaces:
		cnt = 0
		thisPlaceRating = 0
		for person1 in data.keys():
			similarityIndex = pearsonDistance(data,person,person1)
			if(similarityIndex<0):
				continue

			if(person1!=person and place in data[person1].keys() ):
				#print str(similarityIndex)+str(person1)
				thisPlaceRating += similarityIndex*data[person1][place]
				cnt += similarityIndex
		if cnt > 0:
			thisPlaceRating = thisPlaceRating /cnt
			placeRecommendations[place] = thisPlaceRating
	placeRec=sorted(placeRecommendations.items(), key=lambda placeRecommendations:placeRecommendations[1])
	return placeRec[:20]


def itemBasedFiltering(data,person,itemSimiliarty):

	places = getListOfPlaces(data)
	persons = data.keys()
	unWatchedPlaces = []
	watchedPlaces = []
	for plc in places:
		if plc not in data[person].keys():
			unWatchedPlaces.append(plc)
		else:
			watchedPlaces.append(plc)

	recommendations = {}
	for uplc in unWatchedPlaces:
		placeRating = 0
		normalizingFactor = 0
		if len(recommendations)<15:
			for plc in watchedPlaces:
				if plc in dict(itemSimiliarty[uplc]):
					placeRating += 	data[person][plc]*dict(itemSimiliarty[uplc])[plc]
					normalizingFactor +=dict(itemSimiliarty[uplc])[plc]
			if normalizingFactor!=0:
				placeRating /= normalizingFactor
			recommendations[uplc] = placeRating
			print str(uplc)+"::"+str(recommendations[uplc])
	return recommendations