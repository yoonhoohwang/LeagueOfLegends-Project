import requests


def getSummonerID(summonerName):  # get 소환사 ID
    # 빈 칸을 '%20' 으로 대체
    summonerName.replace(" ", "%20")
    # URL 등록
    URL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"\
        "{}?api_key=RGAPI-d5b1bdf4-de38-4e9a-8777-8f80ea8273dd"\
        .format(summonerName)

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
        "{}?api_key=RGAPI-d5b1bdf4-de38-4e9a-8777-8f80ea8273dd".format(
            summonerID)

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

    ''' dic 정보
    leagueId :: b82a4a63-6fe0-34c1-96c5-bd9a7b8b8201
    leagueName :: Syndra's Masterminds
    queueType :: RANKED_SOLO_5x5
    position :: NONE
    tier :: GRANDMASTER
    rank :: I
    leaguePoints :: 157
    wins :: 123
    losses :: 125
    veteran :: false
    inactive :: false
    freshBlood :: true
    hotStreak :: false
    summonerId :: 4s1cdpSQb-GAnZWgUohVc4Z3wZg11JY-Lwu3c56bCcNNgA
    summonerName :: Hide on bush
    '''

    # Return dic
    return dic
