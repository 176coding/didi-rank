# encoding:utf-8

import requests, json

rank_url = 'http://research.xiaojukeji.com/competition/rankingData.action'
post_data = {'competitionId': 'DiTech2016', 'pageSize': '10', 'rowStart': '0',}
# get total size
resp = requests.post(rank_url, data=post_data)
post_data['pageSize'] = resp.json()['totalSize']
# start to get all data
resp = requests.post(rank_url, data=post_data)

with open('./ranks.json', 'r') as file:
    ranks = json.load(file)


def get_ranks(team_names):
    for tm in team_names:
        my_team = [t for t in ranks['data'] if t['teamName'] == tm]
        is_new_team = True
        if len(my_team) == 0:
            # json文件中没有该记录，新添加
            my_team = {}
        else:
            is_new_team = False
            my_team = my_team[0]
        team = [t for t in resp.json()['data'] if t['teamName'] == tm]
        if len(team) == 0:
            print('返回结果中没有找到%s的排名信息' % tm)
            continue
        team = team[0]
        my_team["teamName"] = team["teamName"]
        my_team["lastRank"] = team["rank"]
        my_team["bestScore"] = team["bestScore"]
        my_team["bestCommitTime"] = team["bestCommitTime"]
        my_team["lastScore"] = team["lastScore"]
        my_team["lastCommitTime"] = team["lastCommitTime"]
        h = {}
        h['commitTime'] = team['lastCommitTime']
        h['score'] = team['lastScore']
        h['rank'] = team['rank']
        if is_new_team:
            my_team['history'] = []
        if h not in my_team['history']:
            my_team['history'].append(h)
        if is_new_team:
            ranks['data'].append(my_team)
        # pprint(ranks)
        print('======================== teamName: ' + my_team['teamName'] + ' ==========================')
        print('最新排名: %s 最新分数: %s 最新提交日期: %s' % (my_team['lastRank'], my_team['lastScore'], my_team['lastCommitTime']))
        print('最佳分数: %s 最佳提交日期: %s' % (my_team['bestScore'], my_team['bestCommitTime']))
        print('历史数据：')
        for h in my_team['history']:
            print('历史排名: %s 历史分数: %s 历史日期: %s' % (h['rank'], h['score'], h['commitTime']))
        print()
        pass
    with open('./ranks.json', 'w') as file:
        json.dump(ranks, file)


if __name__ == '__main__':
    team_names = ['XMZH', 'yiersan']
    get_ranks(team_names)
    pass
