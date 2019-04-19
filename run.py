from backend.summoner.summoner import *

from flask import Flask, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return ''


@app.route('/status', defaults={'path': ''}, methods={'GET'})
@app.route('/status/<path:path>')
def status(path):
    ss = SubSummoner()
    summonerName = path
    id = ss.getSummonerID(summonerName)
    data = ss.getSummonerStatus(id)

    return jsonify(data)


# main()
if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
