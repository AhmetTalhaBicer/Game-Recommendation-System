from flask import render_template, request
from controller.gameController import load_data, recommend


def init_routes(app):
    user_game_matrix_hours, similarity_scores, top_games, top_50_games = load_data()

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    @app.route("/", methods=["GET", "POST"])
    def index():
        data = None  # To hold recommended games, if any

        if request.method == "POST":
            # Get the game title entered by the user
            user_input = request.form.get("user_input")

            # Get recommendations
            data = recommend(
                user_input, user_game_matrix_hours, similarity_scores, top_games
            )

        return render_template(
            "index.html",
            game_title=list(top_50_games["title"].values),
            game_date_release=list(top_50_games["date_release"].values),
            game_score=list(top_50_games["positive_ratio"].values),
            game_price=list(top_50_games["price_final"].values),
            game_image=list(top_50_games["image_url"].values),
            data=data,
        )
