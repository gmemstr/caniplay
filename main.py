from requests import get
from os import path, mkdir
from sys import argv
import json


game_title = argv[1]


def main():
    if path.exists("cache") is not True:
        mkdir("cache")

    if path.exists("cache/games.json") is not True:
        print("Fetching latest games list from API.")
        req = get("https://protondb.max-p.me/games")
        with open("cache/games.json", "wb") as f:
            f.write(req.content)

    games = {}
    with open("cache/games.json") as f:
        games = json.load(f)

    cases = {
        "Native": "Yes",
        "Platinum": "Yes",
        "Gold": "Most likely",
        "Silver": "Maybe",
        "Bronze": "Unlikely",
        "Borked": "No"
    }

    for game in games:
        if game_title in game["title"]:
            g = get(f"https://protondb.max-p.me/games/{game['appId']}/reports")
            g_latest = g.json()

            ratings = {}
            for review in g_latest:
                if review["rating"] in ratings:
                    ratings[review["rating"]] += 1
                else:
                    ratings[review["rating"]] = 1

            ratings_sorted = sorted(ratings.items(), key=lambda item: item[1], 
                    reverse=True)

            can_run = cases.get(ratings_sorted[0][0])
            print(f"{game['title']}: {can_run} ({ratings_sorted[0][0]})")


if __name__ == '__main__':
    main()
