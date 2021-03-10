import csv
import random

with open('C:\pokemon.csv', 'r') as f: #ファイルを開く
    reader = csv.reader(f)  #ファイルからデータを読み込む
    line = [row for row in reader]

    while True:
        print("この説明のポケモンを描いてください！")

        number = random.randrange(387)
        print(number)
        print(line[number][1])

        while True:
            print("答えのポケモンを表示しますか？")
            str = input()

            if(str == 'Y'):
                print("答えのポケモン",line[number][0])
                break
            else:
                print("待ちます")   

        break         
            