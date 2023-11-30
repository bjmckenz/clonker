from flask import Flask, jsonify
import time

# All times in seconds

app = Flask(__name__)

CLONK_MATCHUP_WINDOW = 2.000

# "Settle" ensures that we'll still be in the list for a bit
# after the sleep CLONK_MATCHUP_WINDOW
# impacted by service time for the request
SETTLE = 0.020

clonks_within_window = []

@app.route('/clonk/<username>', methods=['GET'])
def clonk(username):
    global clonks_within_window

    now = time.time()

    clonks_within_window.append({"username": username, "at": now})

    time.sleep(CLONK_MATCHUP_WINDOW)

    clonks_within_window = list(filter(
        lambda x: x["at"] > now - CLONK_MATCHUP_WINDOW + SETTLE,
        clonks_within_window))

    return jsonify({"clonks_within_window": clonks_within_window})
