import random

def random_games(recommendations, games, n):
    count = 0
    while count < n and games: 
        game = random.choice(games)
        if game not in recommendations:
            recommendations.append(game)
            games.remove(game)  
            count += 1
    return recommendations