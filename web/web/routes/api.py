from flask import Blueprint, jsonify, request

from web.__main__ import red

app = Blueprint("api", __name__)


@app.route("/add_score", methods=["POST"])
def add_highscore():
    wpm = int(request.json["wpm"])
    accuracy = int(request.json["accuracy"])
    username = request.json["username"]

    score = wpm * accuracy

    existing = red.hget(f"stats:{username}", "score")

    if existing:
        if int(existing) >= score:
            return jsonify({"message": "not_changed"}), 200

    red.hset(f"stats:{username}", "wpm", wpm)
    red.hset(f"stats:{username}", "accuracy", accuracy)
    red.hset(f"stats:{username}", "score", score)

    return jsonify({"message": "ok"}), 200


@app.route("/scores")
def get_scores():
    score_keys = red.keys("stats:*")

    scores = {}
    for key in score_keys:
        data = red.hgetall(key)
        scores[key[6:]] = {k: int(v) for k, v in data.items()}

    return jsonify(scores), 200
