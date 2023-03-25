import datetime
import pandas

# 何桁必要か
NeedDigit = 3

nums = []
LoopTimes = 10**NeedDigit	# 繰り返しの回数 10^桁数 で算出

# LoopTimes回現在時刻のマイクロ秒の後ろNeedDigit桁を取得し配列化
for i in range(LoopTimes):
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
