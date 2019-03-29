from summoner.summoner import *


class RiotProject(object):
    def __init__(self):
        print('Create Riot Project...')

    # main()
if __name__ == "__main__":
    print('running Project...')
    _id = getSummonerID("hide on bush")
    _data = getSummonerStatus(_id)
    print(_data)
