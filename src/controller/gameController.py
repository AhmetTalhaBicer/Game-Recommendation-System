import numpy as np
import pickle
from fuzzywuzzy import process


def load_data():
    user_game_matrix_hours = pickle.load(
        open("./data/processed/user_game_matrix_hours.pkl", "rb")
    )
    similarity_scores = pickle.load(
        open("./data/processed/similarity_scores.pkl", "rb")
    )
    top_games = pickle.load(open("./data/processed/top_games.pkl", "rb"))
    top_50_games = pickle.load(open("./data/processed/top_50_games.pkl", "rb"))
    return user_game_matrix_hours, similarity_scores, top_games, top_50_games


def recommend(
    game_title, user_game_matrix_hours, similarity_scores, top_games, top_n=10
):
    game_title = game_title.lower()
    normalized_titles = user_game_matrix_hours.index.str.lower()

    # Fuzzy matching to find the closest match
    closest_match = process.extractOne(game_title, normalized_titles, score_cutoff=80)

    if closest_match is None:
        return "Game not found in the dataset."

    index = np.where(normalized_titles == closest_match[0])[0][0]
    similar_items = sorted(
        list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True
    )[1 : top_n + 1]

    data = []
    for i in similar_items:
        item = []
        temp_df = top_games[top_games["title"].str.lower() == normalized_titles[i[0]]]
        item.extend(list(temp_df.drop_duplicates("title")["title"].values))
        item.extend(list(temp_df.drop_duplicates("title")["date_release"].values))
        item.extend(
            list(temp_df.drop_duplicates("title")["positive_ratio"].values.astype(int))
        )
        item.extend(
            list(temp_df.drop_duplicates("title")["price_final"].values.astype(float))
        )
        item.extend(list(temp_df.drop_duplicates("title")["image_url"].values))
        data.append([x.item() if isinstance(x, np.generic) else x for x in item])

    return data
