import argparse
import os
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from stats.gamestats import get_stats_from_sessions
from stats.top import TopList
from stats.schedule import Schedule
from stats.history import History

from server.cache import LogCache


def parse_args():
    desc = "Calculate some play statistics for your retro gaming"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8080,
        help="portnumber for the server, defaults to 8080",
    )
    parser.add_argument(
        "-r",
        "--refresh-interval",
        type=int,
        default=30,
        help="the number of minutes you want to cache the log",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="/home/pi/RetroPie/game_stats.log",
        help="path to the stats file, defaults to /home/pi/RetroPie/game_stats.log",
    )

    return parser.parse_args()


args = parse_args()
cache = LogCache(args.file, args.refresh_interval)
app = Flask(
    "RetroStats-Server",
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
)


@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")


@app.route("/stats", methods=["GET"])
def get_stats():
    criteria = request.args.get("criteria", "total")
    systems = request.args.get("systems", None)
    exclude_systems = request.args.get("exclude_systems", None)
    skip_shorter_than = request.args.get("skip_shorter_than", 0)
    lookback = request.args.get("lookback", 0)
    num_entries = request.args.get("num_entries", 0)
    sessions = cache.get_log().get_sessions(
        systems, exclude_systems, int(skip_shorter_than), int(lookback)
    )
    stats = get_stats_from_sessions(sessions)
    top = TopList(stats)
    top = top.get_list_entries_raw(criteria, int(num_entries))
    return jsonify(top)


@app.route("/schedule", methods=["GET"])
def get_schedule():
    systems = request.args.get("systems", None)
    exclude_systems = request.args.get("exclude_systems", None)
    skip_shorter_than = request.args.get("skip_shorter_than", 0)
    lookback = request.args.get("lookback", 0)
    sessions = cache.get_log().get_sessions(
        systems, exclude_systems, int(skip_shorter_than), int(lookback)
    )
    schedule = Schedule(sessions)
    return jsonify(schedule.get_schedule_data())


@app.route("/history", methods=["GET"])
def get_history():
    systems = request.args.get("systems", None)
    exclude_systems = request.args.get("exclude_systems", None)
    skip_shorter_than = request.args.get("skip_shorter_than", 0)
    lookback = request.args.get("lookback", 0)
    sessions = cache.get_log().get_sessions(
        systems, exclude_systems, int(skip_shorter_than), int(lookback)
    )
    history = History(sessions)
    return jsonify(history.get_history_data())


def main():
    app.run(host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
