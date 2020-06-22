from scraiping import make_url, Scraiping
from helpers import Choise, Relative
from methods import Winning

info = ['2020', '55', '0621', '04']#[年, 会場,　月日,　レース番号]
#会場 : 門別=30, 水沢=36, 船橋=43, 笠松=47, 園田=50, 高知=54, 佐賀=55, 帯広=65, 金沢 = 46

def run_Winning(c):

    #combiの要素が一個の場合
    if type(c) == str:

        Wi = Winning(sc_df['単勝'], sc_df[c])
        model = Wi.model_0()

        return Wi.result(model)

    #combiの要素が二個の場合
    else:

        c0 = c[0]
        c1 = c[1]
        Wi = Winning(sc_df['単勝'], sc_df[c0], sc_df[c1])
        model = Wi.model_0()

        return Wi.result(model)


if __name__ == '__main__':

    print('start : ', info)
    print('----------------------')
    #単勝用, 馬単用のurl作成
    tansyo_url, umatan_url = make_url(info)
    #スクレイピング開始
    sc_df = Scraiping(tansyo_url, umatan_url).get()
    #馬単合成オッズ計算
    re_df = Relative(sc_df).sum_odds()
    #class Winningに入れる馬単の引数の組み合わせを作成
    combi = Choise(re_df).combine()
    #combiが空の場合
    if combi == []:
        print('[]:Not solved')
    #combiがある場合
    else:
        #combiを使ってWinningを走らせる
        for c in combi:
            result = run_Winning(c)
            print(str(c) + ':' + result[1])
            if result[1] == 'Solved':
                print(result[0])
