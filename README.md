# マイクロ秒が任意の桁数の乱数代わりになるんじゃないかと考えた実験

とあるプロジェクトの中で、乱数を発生させたくないが、
乱数的な挙動をする関数を探しているとき、
マイクロ秒が使えるんじゃないかと思いつき、
それで実装し、動かしています。

小ネタのところなので意図しない動きでも影響はないのですが、
実際のところはどうだったんだろ？
との疑問が湧いてきたので、試してみることにしました。

## Pythonで動くようにしてみる
方向性としては、何桁で計算したいかというところから、
必要な繰り返し回数などを計算しました


### time-stat.py
```
import datetime
import pandas

# 何桁必要か
NeedDigit = 3

nums = []
RoopTimes = 10**NeedDigit	# 繰り返しの回数 10^桁数 で算出

# RoopTimes回繰り返し現在時刻のマイクロ秒の後ろNeedDigit桁を取得し配列化
for i in range(RoopTimes):
	NowDateTime = str(datetime.datetime.now())	# 現在の時刻をマイクロ秒まで取得し型を文字列に
	num = int(NowDateTime[-NeedDigit:]) # 後ろから初期値の桁数を取得
	nums.append(num) # 配列に挿入

df = pandas.Series(nums) # データフレーム化

#個々の統計量の出力
print('合計',df.sum())
print('平均',df.mean())
print('最大',df.max())
print('中央値',df.median())
print('最小',df.min())
print('分散',df.var(ddof=1))
print('標準偏差',df.std(ddof=1))
print('歪度',df.skew())
print('尖度',df.kurt())
print('四分位',df.quantile(q=[0,0.25,0.5,0.75,1]))
print('最頻値',df.mode())
```

### コードの補足
```
import datetime
import pandas
```
まずは必要なライブラリの呼び出し


```
# 何桁ほしいか
NeedDigit = 3

nums = []
RoopTimes = 10**NeedDigit	# 繰り返しの回数 10^桁数 で算出
```
値の設定。
NeedDigitで必要な桁数を入力したら、後は勝手に動く

```
# RoopTimes回繰り返し現在時刻のマイクロ秒の後ろNeedDigit桁を取得し配列化
for i in range(RoopTimes):
	NowDateTime = str(datetime.datetime.now())	# 現在の時刻をマイクロ秒まで取得し型を文字列に
	num = int(NowDateTime[-NeedDigit:]) # 後ろから初期値の桁数を取得
	nums.append(num) # 配列に挿入
```
必要な桁数から算出した繰り返し回数だけ、
マイクロ秒を取得し、配列に放り込む


```
df = pandas.Series(nums) # データフレーム化

#個々の統計量の出力
print('合計',df.sum())
print('平均',df.mean())
print('最大',df.max())
print('中央値',df.median())
print('最小',df.min())
print('分散',df.var(ddof=1))
print('標準偏差',df.std(ddof=1))
print('歪度',df.skew())
print('尖度',df.kurt())
print('四分位',df.quantile(q=[0,0.25,0.5,0.75,1]))
print('最頻値',df.mode())
```
配列をもとに、pandasのデータフレームにし、
データフレームから各種統計値を取得

結果、動かしてみるといくらかのブレはあるものの、
ある程度は想定した形で動いてくれていたので、
まあ、良かったのかと。

### 実行結果（例）
```
$ python3 time-stat.py
合計 503526
平均 503.526
最大 999
中央値 499.0
最小 0
分散 92987.78110510511
標準偏差 304.9389793140672
歪度 -0.0059686175466188126
尖度 -1.3920210735116008
四分位 0.00      0.00
0.25    225.75
0.50    499.00
0.75    782.25
1.00    999.00
dtype: float64
最頻値 0        4
1       11
2       14
3       19
4       24
      ...
243    981
244    984
245    986
246    989
247    991
Length: 248, dtype: int64
```
ざっと、平均や中央値とか見る感じだと、
まあ、想定通りの分布になってるんじゃないかと。


## これから
とりあえず作ってみたという次元なので、
分布や統計値がなんとなく見えればよかったのだけれども、
手元では繰り返し実行して値のブレを見たりもしています。

それも踏まえてコード上で上記のフローの繰り返しの実行と
集計にあわせ、グラフ化して出力できるようにして、
ビジュアル的に分布が見えると直感的にわかりやすいかと思いました。
（たぶんやんないけど）

あと、あらためてデータフレーム便利。
