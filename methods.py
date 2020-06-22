from pulp import  LpVariable, LpProblem, LpMaximize, LpMinimize, lpSum, value, LpStatus
import pandas as pd
import numpy as np
from helpers import Connect



class Winning(Connect):

    def __init__(self, tansyo, umatan_, umatan__ = None):

        super().__init__(tansyo, umatan_, umatan__)
        self.df = self.connect()
        self.odds = self.df['オッズ']
        self.l = len(self.df)
        self.V = [LpVariable('v'+n, lowBound = 0) for n in self.df.index]

    def model_0(self):

        model = LpProblem(name = 'horse', sense = LpMinimize)

        model += lpSum(v for v in self.V)

        for l in range(self.l):
            model += self.odds[l] * self.V[l] - lpSum(v for v in self.V) >= 0
            model += self.V[l] >= 1

        return model

    def model_1(self, betsum):

        model = LpProblem(name = 'horse', sense = LpMaximize)

        odds_V = np.sum(self.odds * self.V)
        sum_V = lpSum(v for v in self.V)

        model += odds_V - self.l * sum_V
        model += sum_V <= betsum
        for l in range(self.l):
            model += self.odds[l] * self.V[l] - lpSum(v for v in self.V) >= 0
            model += self.V[l] >= 1

        return model

    def result(self, model):

        res = model.solve()

        bet = np.array([v.value() for v in self.V])

        bet = np.ceil(bet)
        result_betsum = np.sum(bet)
        if_win = self.odds * bet * 100
        diff = (self.odds * bet - result_betsum) * 100

        self.df['ベット(枚)'] = bet
        self.df['払い戻し金(円)'] = if_win
        self.df['差額(円)'] = diff

        status = 'Solved' if LpStatus[res] == 'Optimal' else 'Not solved'

        return self.df, status


class Expect(Connect):

    def __init__(self, tansyo, umatan_ = None, umatan__ = None, propability = None):

        super().__init__(tansyo, umatan_ = None, umatan__ = None)
        self.df = self.connect()
        self.l = len(self.df)
        self.odds = self.df['オッズ']
        self.pro = propability
        if self.pro == None:
            self.pro = self.df['確率']
        self.V = [LpVariable('v'+n, lowBound = 0) for n in self.df.index]

    def model_0(self, betsum, k):

        model = LpProblem(name = 'horse', sense = LpMaximize)

        model += lpSum(o * v * p for o, p, v in zip(self.odds, self.pro, self.V))
        model += lpSum(v for v in self.V) <= betsum

        for i in range(self.l):
            model += self.V[i] >= k

        return model

    def model_1(self, betsum):

        model = LpProblem(name = 'horse', sense = LpMaximize)

        model += lpSum(o * v * p for o, p, v in zip(self.odds, self.pro, self.V))
        model += lpSum(v for v in self.V) <= betsum

        pre_df = self.df.copy()
        pre_df['V'] = self.V
        pre_df = pre_df.sort_values('オッズ')
        V = pre_df['V']

        for i in range(self.l):
            if i < self.l - 1:
                model += V[i] - V[i+1] >= 1
            elif i == self.l:
                model += V[i] >= 1

        return model


    def result(self, model):

        result = model.solve()

        bet = np.array([value(v) for v in self.V])
        bet = np.ceil(bet)
        result_betsum = np.sum(bet)
        if_win = self.odds * bet * 100
        diff = self.odds * bet * 100 - result_betsum * 100
        expected_value = np.sum(self.odds * self.pro * bet * 100)

        self.df['ベット(枚)'] = bet
        self.df['払い戻し金(円)'] = if_win
        self.df['差額(円)'] = diff

        print('Solved' if LpStatus[result] == 'Optimal' else 'Not solved')
        print('ベット総額(枚)　: {}'.format(int(result_betsum)))
        print('期待値(円) : {}'.format(int(expected_value)))

        return self.df
