from flask import Flask, render_template, request
import numpy as np
import pickle

# Load the necessary DataFrames
user_game_matrix_hours = pickle.load(
    open("./data/processed/user_game_matrix_hours.pkl", "rb")
)
similarity_scores = pickle.load(open("./data/processed/similarity_scores.pkl", "rb"))
top_games = pickle.load(open("./data/processed/top_games.pkl", "rb"))
top_50_games = pickle.load(open("./data/processed/top_50_games.pkl", "rb"))

# Flask app setup
app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Home page route
@app.route("/", methods=["GET", "POST"])
def index():
    data = None  # To hold recommended games, if any

    if request.method == "POST":
        # Get the game title entered by the user
        user_input = request.form.get("user_input")

        # Check if the game title exists in the index
        if user_input in user_game_matrix_hours.index:
            # Get the index of the entered game title
            index = np.where(user_game_matrix_hours.index == user_input)[0][0]

            # Find similar games and select the top 10
            similar_items = sorted(
                list(enumerate(similarity_scores[index])),
                key=lambda x: x[1],
                reverse=True,
            )[1:11]

            data = []
            for i in similar_items:
                item = []
                # Get details of the similar games
                temp_df = top_games[
                    top_games["title"] == user_game_matrix_hours.index[i[0]]
                ]
                item.extend(list(temp_df.drop_duplicates("title")["title"].values))
                item.extend(
                    list(temp_df.drop_duplicates("title")["date_release"].values)
                )
                item.extend(
                    list(temp_df.drop_duplicates("title")["positive_ratio"].values)
                )
                item.extend(
                    list(temp_df.drop_duplicates("title")["price_final"].values)
                )

                data.append(item)
        else:
            data = ["Game not found in the dataset."]

    return render_template(
        "index.html",
        game_title=list(top_50_games["title"].values),
        game_date_release=list(top_50_games["date_release"].values),
        game_score=list(top_50_games["positive_ratio"].values),
        game_price=list(top_50_games["price_final"].values),
        data=data,
    )


if __name__ == "__main__":
    # Run the app
    app.run(host="0.0.0.0", port=5000, debug=True)
