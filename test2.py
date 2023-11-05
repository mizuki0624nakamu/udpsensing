
import pandas as pd
import os
print("test")
# test.csvを読み込む
df = pd.read_csv('data4.csv')

# 1列目を消す
df = df.drop(df.columns[0], axis=1)
first = 2150
last = 9600
file_index = 1
df_subset = df.iloc[first:first+339]

    # CSVファイル名を設定（leftフォルダに保存）
# filename = os.path.join('train1', f'{file_index}.csv')

#     # CSVファイルに書き込み
# df_subset.to_csv(filename, index=False)
while first <= last:
    df_subset = df.iloc[first:first+339]

    # CSVファイル名を設定（leftフォルダに保存）
    filename = os.path.join('wavedata', f'{file_index}.csv')

    # CSVファイルに書き込み
    df_subset.to_csv(filename, index=False)

    # 行番号とファイルインデックスを更新
    first += 10
    file_index += 1









