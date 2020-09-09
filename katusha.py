import numpy as np
import pandas as pd


def select_tournament():
    global data_file, x
    league_number = int(raw_input('Input the number of required tournament\n'
                                  '1. Italian Serie A league 2018/2019\n'
                                  '2. Spain La Liga Primera Division 2018/2019\n'
                                  '3. English Premier league 2018/2019\n'
                                  'Your input:'))
    if type(league_number) is not int:
        print('Invalid input')
        select_tournament()
    if league_number == 1:
        data_file = 'I1.csv'
    elif league_number == 2:
        data_file = 'SP1.csv'
    elif league_number == 3:
        data_file = 'E0.csv'
    else:
        print('No such league')
        select_tournament()
    x = open(data_file, 'r')
    return data_file, x


def request():
    f_number = int(raw_input('Print the number of function\n'
                             '1.Show all matches of a given team\n'
                             '2.Show all matches on a given date\n'
                             '3.Show ranking\n'
                             'Input:'))
    if type(f_number) is not int:
        print('Invalid input')
        request()
    if f_number == 1:
        req_team = raw_input('Input team:')
        while type(req_team) is not str:
            print('Invalid input')
            req_team = raw_input('Input team:')
        matches_team(req_team)
    elif f_number == 2:
        req_date = raw_input('Input date with slashes:')
        while type(req_date) is not str:
            print('Invalid input')
            req_date = raw_input('Input date with slashes:')
        matches_date(req_date)
    elif f_number == 3:
        all_teams()
        ranking()
    else:
        print('No such function')
        request()


def matches_team(team):
    d = {}
    if type(team) != str:
        print('Input is incorrect')
    x.readline()
    for line in x:
        k = line.split(',')
        if k[2] == team or k[3] == team:
            d['Date'] = k[1]
            d['Teams'] = k[2], k[3]
            d['Score'] = k[4], k[5]
            df = pd.DataFrame(d, index=['1', '2'])
            df = df[['Teams', 'Score', 'Date']]
            print(df)
    if d == {}:
        print('No matches was found')
        select_tournament()
        request()


def matches_date(date):
    d = {}
    if type(date) != str:
        print('Input is incorrect')
    x.readline()
    for line in x:
        k = line.split(',')
        if k[1] == date:
            d['Teams'] = k[2], k[3]
            d['Score'] = k[4], k[5]
            df = pd.DataFrame(d, index=['1', '2'])
            df = df[['Teams', 'Score']]
            print(df)
    if d == {}:
        print('No matches was found')
        select_tournament()
        request()


def all_teams():
    global teams
    teams = []
    x.readline()
    for line in x:
        k = line.split(',')
        team = k[2]
        if team not in teams:
            teams.append(team)
    for line in x:
        k = line.split(',')
        team = k[3]
        if team not in teams:
            teams.append(team)
    return teams


def ranking():
    global r
    r = []
    for i in range(len(teams)):
        total_games = 0
        wins = 0
        draws = 0
        losses = 0
        goal_dif = 0
        rank_score = 0
        goals = 0
        x = open(data_file, 'r')
        for line in x:
            k = line.split(',')
            team = teams[i]
            if k[2] == team:
                total_games += 1
                if int(k[4]) > int(k[5]):
                    wins += 1
                    rank_score += 3
                    goal_dif += (int(k[4]) - int(k[5]))
                    goals += int(k[4])
                if int(k[4]) == int(k[5]):
                    draws += 1
                    rank_score += 1
                    goals += int(k[4])
                else:
                    losses += 1
                    goal_dif += (int(k[4]) - int(k[5]))
                    goals += int(k[4])
            if k[3] == team:
                total_games += 1
                if int(k[5]) > int(k[4]):
                    wins += 1
                    rank_score += 3
                    goal_dif += (int(k[5]) - int(k[4]))
                    goals += int(k[5])
                if int(k[4]) == int(k[5]):
                    draws += 1
                    rank_score += 1
                    goals += int(k[5])
                else:
                    losses += 1
                    goal_dif += (int(k[5]) - int(k[4]))
                    goals += int(k[5])
        team = teams[i]
        r.append([team, total_games, wins, draws, losses,
                  goal_dif, rank_score, goals])
    if data_file == 'I1.csv':
        sort_head_to_head_points(r)
        sort_goal_diff_heads(r)
        sort_goal_diff_overall(r)
        sort_number_goals(r)
    if data_file == 'E0.csv':
        sort_goal_diff_overall(r)
    else:
        sort_head_to_head_points(r)
        sort_goal_diff_heads(r)
        sort_number_goals(r)
    for i in r:
        i.pop(7)
    print_table(r)


def sort_number_goals(list):
    list.sort(key=lambda i: (i[6], i[7]), reverse=True)


def sort_goal_diff_heads(list):
    score_1 = 0
    score_2 = 0
    for i in range(len(list)-1):
        if r[i][6] == r[i+1][6]:
            team1 = r[i][0]
            team2 = r[i+1][0]
            for line in x:
                k = line.split(',')
                if k[2] == team1 and k[3] == team2:
                    score_1 += int(k[4]) - int(k[5])
                    score_2 += int(k[5]) - int(k[4])
            if score_2 > score_1:
                p = r[i]
                r[i] = r[i+1]
                r[i+1] = p


def sort_head_to_head_points(list):
    wins_1 = 0
    wins_2 = 0
    for i in range(len(list)-1):
        if r[i][6] == r[i+1][6]:
            team1 = r[i][0]
            team2 = r[i+1][0]
            for line in x:
                k = line.split(',')
                if k[2] == team1 and k[3] == team2:
                    if int(k[4]) > int(k[5]):
                        wins_1 += 1
                    if int(k[5]) > int(k[4]):
                        wins_2 += 1
            if wins_2 > wins_1:
                p = r[i]
                r[i] = r[i+1]
                r[i+1] = p


def sort_goal_diff_overall(list):
    list.sort(key=lambda i: (i[6], i[5]), reverse=True)


def print_table(list):
    nda1 = np.array(list)
    df4 = pd.DataFrame(nda1, columns=['Team name', 'Games played', 'Wins',
                                      'Draws', 'Losses', 'Goal difference',
                                      'Points'], index=[1, 2, 3, 4, 5, 6, 7,
                                                        8, 9, 10, 11, 12,
                                                        13, 14, 15, 16, 17,
                                                        18, 19, 20])
    pd.options.display.max_columns = 100
    print(df4)


select_tournament()
request()
