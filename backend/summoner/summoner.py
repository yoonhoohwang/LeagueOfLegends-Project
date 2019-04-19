import requests
from api import *
import abc
import telegram


class TelegramAPI(object):
    def __init__(self):
        self.API_KEY = '661670678:AAFluBW-ZTSmxsUSv85WkzrcvH57AQF5nsA'
        self.bot = telegram.Bot(token = self.API_KEY)
    
    def sendMsg(self, text_barn):
        self.bot.sendMessage(chat_id = "704445567", text = text_barn)


class Summoner(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def getSummonerID(self, summonerName):
        pass
    
    @abc.abstractmethod
    def getSummonerStatus(self, summonerID):
        pass

class Observer(object):
    @abc.abstractmethod
    def update(self, summonerName):
        pass

class SummonerObserver(Observer):
    def __init__(self):
        self.tel = TelegramAPI()

    def update(self, summonerName):
        msg = "소환사 이름 {} 으로 변경되었습니다. ".format(summonerName)
        self.telMsg(summonerName)
    
    def telMsg(self, summonerName):
        self.tel.sendMsg(summonerName)

        

class SubSummoner(Summoner):
    
    def __init__(self):
        self.summonerID = None
        self.summonerName = None
        self.observer = SummonerObserver()
        
    def getSummonerID(self, summonerName):  # get 소환사 ID
    # 빈 칸을 '%20' 으로 대체
        self.summonerName = summonerName
        self.summonerName.replace(" ", "%20")
        print(self.summonerName)
        # URL 등록
        URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"\
            "{}?api_key={}"\
            .format(self.summonerName, getApiKey())

        # URL 에 소환사 이름 호출
        response = requests.get(URL)
        # 응답온 데이터를 딕셔너리 형태로 변환
        if response.status_code != 200:
            print('잘못된 소환사 이름 입니다.')
            return

        resData = eval(response.text)

        # summnerID 를 return 해준다.
        return resData['id']


    def getSummonerStatus(self, summonerID):  # 소환사 전적확인
        # print(summonerID)
        
        URL = "https://kr.api.riotgames.com/lol/league/v4/positions/by-summoner/"\
            "{}?api_key={}".format(summonerID, getApiKey())

        # print(URL)
        
        response = requests.get(URL)

        # response 상태 코드가 200 이 아니면 출력 후 함수 종료
        if response.status_code != 200:
            print('잘못된 정보입니다.')
            return

        # response 데이터 정제
        resData = response.text
        resData = resData.replace('[', "").replace(']', "")\
            .replace('{', "").replace('}', "")

        li = resData.split(",")

        # 정제된 데이터 dic 변수에 저장
        dic = {}

        for i in li:
            i = i.replace('"', '')
            i = i.split(":")
            dic[i[0]] = i[1]

        self.observer.update(summonerID)
        
        # Return dic
        return dic
        
'''
def getSummonerID(summonerName):  # get 소환사 ID
    # 빈 칸을 '%20' 으로 대체
    summonerName.replace(" ", "%20")
    print(summonerName)
    # URL 등록
    URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"\
        "{}?api_key={}"\
        .format(summonerName, getApiKey())

    # URL 에 소환사 이름 호출
    response = requests.get(URL)
    # 응답온 데이터를 딕셔너리 형태로 변환
    if response.status_code != 200:
        print('잘못된 소환사 이름 입니다.')
        return

    resData = eval(response.text)

    # summnerID 를 return 해준다.
    return resData['id']


def getSummonerStatus(summonerID):  # 소환사 전적확인
    # print(summonerID)
    URL = "https://kr.api.riotgames.com/lol/league/v4/positions/by-summoner/"\
        "{}?api_key={}".format(summonerID, getApiKey())

    # print(URL)
    response = requests.get(URL)

    # response 상태 코드가 200 이 아니면 출력 후 함수 종료
    if response.status_code != 200:
        print('잘못된 정보입니다.')
        return

    # response 데이터 정제
    resData = response.text
    resData = resData.replace('[', "").replace(']', "")\
        .replace('{', "").replace('}', "")

    li = resData.split(",")

    # 정제된 데이터 dic 변수에 저장
    dic = {}

    for i in li:
        i = i.replace('"', '')
        i = i.split(":")
        dic[i[0]] = i[1]


    # Return dic
    return dic
'''