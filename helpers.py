import pandas as pd
import numpy as np
import itertools

class Relative:

    def __init__(self, sc_df):

        self.sc_df = sc_df

    def sum_odds(self):

        length = len(self.sc_df)

        umatan_sum = np.array([np.nan for i in range(length)])

        for l in range(length):

            if self.sc_df[str(l+1)].isnull().values.sum() != length:
                umatan = self.sc_df[str(l+1)]
                a = np.sum(1 / umatan)
                umatan_sum[l] = 1 / a


        diff = umatan_sum - self.sc_df['単勝']

        horse_number = [str(i) for i in range(1, length+1)]
        re_df = pd.DataFrame({'馬番' : horse_number, '単勝' : self.sc_df['単勝'], '馬単合成' : umatan_sum})
        re_df = re_df.set_index('馬番')
        re_df['差'] = diff

        return re_df


class Choise:

    def __init__(self, re_df):

        self.re_df = re_df

    #class Winningに入れる馬単の引数の組み合わせを作成
    def combine(self):

        cho_df = self.condition()
        combi = list(cho_df.index)
        com2 = list(itertools.combinations(combi, 2))
        combi.extend(com2)

        return combi

    #単勝のオッズが20以下,差（単勝と馬単合成オッズの）が正であるものを取り出す
    def condition(self):

        cho_df = self.re_df.loc[self.re_df['単勝'] <= 20.]
        cho_df = cho_df.loc[cho_df['差'] > 0]

        return cho_df



class Connect:

    def __init__(self, tansyo, umatan_ = None, umatan__ = None):

        self.tansyo = tansyo
        self.umatan_ = umatan_
        self.umatan__ = umatan__
        self.l = len(self.tansyo)

    def connect(self):

        co_df = []

        propability = 0.8/self.tansyo
        df = self.get_df(self.tansyo, propability)
        co_df.append(df)

        if type(self.umatan_) == pd.Series:

            index_ = self.get_index(self.umatan_)
            propability_ = self.get_propability(propability, index_)
            df_ = self.get_df(self.umatan_, propability_, index_)

            co_df.append(df_)

        if type(self.umatan__) == pd.Series:

            index__ = self.get_index(self.umatan__)
            propability__ = self.get_propability(propability, index__)
            df__ = self.get_df(self.umatan__, propability__, index__)
            co_df.append(df__)

        co_df = pd.concat(co_df)
        co_df = co_df.set_index('馬番')
        co_df = co_df.dropna()

        if type(self.umatan_) == pd.Series:
            co_df = co_df.drop(str(index_+1))
        if type(self.umatan__) == pd.Series:
            co_df = co_df.drop(str(index__+1))

        return co_df


    def get_index(self, umatan):

        umatan_null = umatan.loc[self.tansyo.isnull() == False]
        umatan_null = umatan_null.loc[umatan_null.isnull() == True]
        index = int(umatan_null.index[0]) - 1

        return index

    def get_propability(self, propability, index):

        propability_copy = propability.copy()
        propability_copy[index] = np.nan

        return propability[index] * propability_copy / (1 - propability[index])

    def get_df(self, tan, propability, index = None):

        if index == None:
            horse_number = [str(i) for i in range(1, self.l+1)]

        else:
            horse_number = [str(index+1)+'-'+str(i+1) for i in range(self.l)]

        df = pd.DataFrame({'馬番' : horse_number,
                            'オッズ' : tan,
                            '確率' : propability})

        return df
