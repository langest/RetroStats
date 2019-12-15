from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from stats.log import parse_log
from stats.stats import get_stats_from_sessions, Stats
from stats.top import TopList

app = Flask(__name__)

GAME_STATS_LOG = "/home/langest/repos/RetroStats/game_stats.log"


@app.route("/", methods=["GET"])
def root():
    return render_template('index.html')


@app.route("/stats", methods=["GET"])
def get_stats():
    sessions = parse_log(GAME_STATS_LOG)
    stats = get_stats_from_sessions(sessions)
    top = TopList(stats)
    criteria = request.args.get("criteria")
    top = top.get_list_entries_raw(criteria)
    return jsonify(top)


def main():
    app.run()


if __name__ == "__main__":
    main()
