from datetime import datetime

import requests

from .utils import STANDARD_TIME_FORMAT

PLATFORM_NAME = '百度点石'


def get_data():
    url = 'https://dianshi.bce.baidu.com/gemstone/competitionslist?type=-1'

    response = requests.get(url)
    content = response.json()
    competitions = content['data']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if competition['status'] == '已结束':
            continue
        # 必须字段
        name = competition['competitionName']
        url = 'https://dianshi.bce.baidu.com/competition/' + competition['id']
        if len(competition['competitionInfo'].strip()) < 1:
            description = name
        else:
            description = competition['competitionInfo']

        FORMAT = "%Y-%m-%d"
        deadline = competition['deadLine']
        deadline = datetime.strptime(deadline, FORMAT)
        deadline = deadline.strftime(STANDARD_TIME_FORMAT)

        start_time = None
        new_flag = False

        reward = competition['totalPrize']

        cp = {
            'name': name,
            'url': url,
            'description': description,
            'deadline': deadline,
            'reward': reward,
            'start_time': start_time,
            'new_flag': new_flag
        }

        cps.append(cp)
    data['competitions'] = cps

    return data
