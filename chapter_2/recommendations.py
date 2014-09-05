# A dictionary of movie critics and their ratings of a small
# set of movies
critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'The Night Listener': 3.0,
        'You, Me and Dupree': 3.5
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5, 
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5, 
        'Just My Luck': 3.0,
        'The Night Listener': 4.5,
        'Superman Returns': 4.0, 
        'You, Me and Dupree': 2.5
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0, 
        'Snakes on a Plane': 4.0, 
        'Just My Luck': 2.0, 
        'Superman Returns': 3.0, 
        'The Night Listener': 3.0, 
        'You, Me and Dupree': 2.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0, 
        'Snakes on a Plane': 4.0, 
        'The Night Listener': 3.0, 
        'Superman Returns': 5.0, 
        'You, Me and Dupree': 3.5
    },
    'Toby': {
        'Snakes on a Plane': 4.5,
        'You, Me and Dupree': 1.0,
        'Superman Returns': 4.0
    }
}


from math import sqrt


def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    if len(si) == 0: 
        return 0
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])
    return 1 / (1 + sqrt(sum_of_squares))


def sim_pearson(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1


    n = len(si)

    if n == 0:
        return 0
    sum_of_person1 = sum([prefs[person1][item] for item in si])
    sum_of_person2 = sum([prefs[person2][item] for item in si])

    sum_of_squares_person1 = sum([pow(prefs[person1][item], 2) for item in si])
    sum_of_squares_person2 = sum([pow(prefs[person2][item], 2) for item in si])

    product_of_two_persons = sum([prefs[person1][item] * prefs[person2][item] for item in si])

    num = product_of_two_persons - sum_of_person1 * sum_of_person2 / n

    den = sqrt((sum_of_squares_person1-pow(sum_of_person1, 2)/n) * (sum_of_squares_person2-pow(sum_of_person2, 2)/n))

    if den == 0:
        return 0
    return num / den


def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]

    scores.sort()
    scores.reverse()
    return scores[0:n]

def getRecommendations(prefs, person, similarity=sim_pearson):
    total_value = {}
    sim_total_value = {}

    for other in prefs:
        if other == person:
            continue
        sim_value = similarity(prefs, person, other)
        if sim_value <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                total_value.setdefault(item, 0)
                total_value[item] += sim_value * prefs[other][item]
                sim_total_value.setdefault(item, 0)
                sim_total_value[item] += sim_value
    rank = [(total_value[item]/sim_total_value[item], item) for item, total in total_value.items()]
        
    rank.sort()
    rank.reverse()
    return rank

def transformPrefs(prefs):
    items = {}
    for person in prefs:
        for item in prefs[person]:
            items.setdefault(item, {})
            items[item][person] = prefs[person][item]
    return items

if __name__ == "__main__":
    print sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')
    print topMatches(critics, 'Toby', n=3)
    print getRecommendations(critics, 'Toby', similarity=sim_pearson)
    print getRecommendations(critics, 'Lisa Rose', similarity=sim_pearson)
    print getRecommendations(transformPrefs(critics), 'Just My Luck')
