# Horse_Optimization

競馬必勝法をプログラム化してみた

## Description

スクレイピングでパラメータ（**info**）を設定すれば、そのデータをとることが出来る。
最適化(pulp)によって競馬必勝法のプログラムを作成しモジュール化しました。これにより、時間をかけずに負けない賭け方を出力する。
(参考記事:<a href="https://www.umameshi.com/info/0011.html">うまめし.com 競馬必勝法)</a> 

## Usage

*```Scraiping(tansyo_url, umatan_url).get()```:スクレイピングでリアルタイムの単勝と馬単のデータを取ってくる  
取得データ元:<a href="https://www.netkeiba.com/">netkeiba.com</a>, <a href="https://nar.netkeiba.com/odds/index.html?type=b1&race_id=202036062202&rf=shutuba_submenu">単勝（例）</a>, <a href="https://nar.netkeiba.com/odds/index.html?type=b6&race_id=202036062202&housiki=c0&rf=shutuba_submenu">馬単（例）</a> 
    
*```Relative(sc_df).sum_odds()```:スクレイピングしてきたデータ（sc_df）を入れると馬単合成オッズが出力される  
*```Choise(re_df).combine()```:比較(上の作業)で得られたデータを入れると必勝法に使う馬単の番号がlistで出力される  
*```Winning(sc_df[単勝], sc_df['i'], sc_df['j'](=None)).model_0()```:model_0(ベット枚数を最小、どの馬が勝っても払い戻し金が0以上)を得る  
*```Winning(sc_df[単勝], sc_df['i'], sc_df['j'](=None)).model_1(100)```:model_1(払い戻し金の総額が最大、どの馬が勝っても払い戻し金が0以上、ベット枚数の上限（100枚）)を得る  
*```Winning(sc_df[単勝], sc_df['i'], sc_df['j'](=None)).result(model_0(or model_1)))```:結果と、最適化問題が解けたか解けていないかが出力される 

## Comment

- Example.ipynbがあるのでそれを参考にして下さい。
- win_main.pyは**info**をいじれば```python win_main.py```をするだけで結果が得られる。
- methods.pyの中のモジュールExpectは機械学習させて着順の確率を計算できれば使用できる。基本的にはExpectのメソッドは期待値を最大にする最適化を行う。

## Requirement

- python(=3.7.7)
  
- numpy(=1.18.1)  
- pandas(=1.0.3)  
- requests(=2.23.0)  
- bs4(=4.8.2)  
- json(=2.0.9)  
- pulp(=2.1)  

