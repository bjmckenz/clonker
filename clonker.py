from flask import Flask, jsonify, request
from geopy.distance import great_circle
import time
import sys

# All times in seconds

CURRENT_VERSION = "1.0.0"
DEFAULT_CLOSE_ENOUGH_METERS = 1.0
DEFAULT_TIME_MATCHUP_WINDOW = 0.5
DEFAULT_IDENTITY_KEY = 'id'

# "Settle" ensures that we'll still be in the list for a bit
# after the sleep DEFAULT_TIME_MATCHUP_WINDOW
# insurance compensating for service time of the request
SETTLE = 0.005

clonks_within_time_window = []

# app must be defined and initialized before routes.
# non-Flask arguments must be parsed before app is initialized.
if __name__ == '__main__':

    global app

    config = {}
    config['distance'] = DEFAULT_CLOSE_ENOUGH_METERS
    config['time'] = DEFAULT_TIME_MATCHUP_WINDOW
    config['debug'] = False

    if len(sys.argv) > 1 and sys.argv[1] == '-d':
        config['debug'] = True
        sys.argv = [sys.argv[0]] + sys.argv[2:]

    if len(sys.argv) > 1 and sys.argv[1] == '-m':
        config['distance'] = int(sys.argv[2])
        sys.argv = [sys.argv[0]] + sys.argv[3:]

    if len(sys.argv) > 1 and sys.argv[1] == '-t':
        config['time'] = int(sys.argv[2])
        sys.argv = [sys.argv[0]] + sys.argv[3:]

    app = Flask(__name__)

    for key in config:
        app.config[key] = config[key]


@app.route('/clonk', methods=['POST'])
def clonk():
    client = request.json
    now = time.time()

    if 'version' not in client or client['version'] != CURRENT_VERSION:
        return jsonify({
            "error": "incorrect or missing version",
            "required": CURRENT_VERSION
            }), 400

    if DEFAULT_IDENTITY_KEY not in client:
        return jsonify({
            "error": "no identity key",
            "required": DEFAULT_IDENTITY_KEY
            }), 400

    my_event = client | {"at": now}
    if app.config['debug']:
        print(my_event, file=sys.stderr)

    global clonks_within_time_window

    clonks_within_time_window = \
        list(filter(lambda x: not same_client(my_event, x),
                    clonks_within_time_window)) + \
        [my_event]

    # wait for our peer clonkers
    time.sleep(app.config['time'])

    clonks_within_time_window = list(filter(
        lambda x: x["at"] > now - app.config['time'] + SETTLE,
        clonks_within_time_window))

    if app.config['debug']:
        print(list(clonks_within_time_window), file=sys.stderr)

    clonking_me = filter(lambda x: are_clonking(my_event, x),
                         clonks_within_time_window)

    return jsonify({"clonks": list(clonking_me)})


def hypotenuse(s1, s2):
    return (s1**2 + s2**2)**0.5


def same_client(clonk1, clonk2):
    return clonk1[DEFAULT_IDENTITY_KEY] == clonk2[DEFAULT_IDENTITY_KEY]

# "is within time window" is assumed
def are_clonking(clonk1, clonk2):
    return not same_client(clonk1, clonk2) and are_close_enough(clonk1, clonk2)

def distance_can_be_calculated(clonk1, clonk2):
    return 'latitude' in clonk1 and 'latitude' in clonk2 and \
        'longitude' in clonk1 and 'longitude' in clonk2 and \
        ('altitude' in clonk1) == ('altitude' in clonk2)


def are_close_enough(clonk1, clonk2):
    return distance_can_be_calculated(clonk1, clonk2) and \
        distance_between(clonk1, clonk2) < app.config['distance']


def distance_between(clonk1, clonk2):
    sea_level_distance = great_circle(
        (clonk1['latitude'], clonk1['longitude']),
        (clonk2['latitude'], clonk2['longitude']),
    ).meters

    dist = sea_level_distance

    # incorporate altitude (farily valid for << 1km) if it's available
    if 'altitude' in clonk1:
        dist = hypotenuse(sea_level_distance,
                        clonk1['altitude'] - clonk2['altitude'])

    return dist


if __name__ == '__main__':
    app.run()
