import re 
import csv
from pathlib import Path
from lxml import html

# 不要なタグを検索する xpath 表現のタプル
REMOVE_TAGS = ('.//style', './/script', './/noscript')

# 見出しタグを検索する xpath 表現
XPATH_H_TAGS = './/h1|.//h2|.//h3|.//h4|.//h5|.//h6'

# 見出しタグを検出するための正規表現
RE_H_MATCH = re.compile('^h[1-6]$').match

def main():

    src_file = Path("C:\pokemon.html")

    # htmlデータを取得
    with src_file.open('rb') as f:
        html_data = f.read()

    # htmlを解析
    root = html.fromstring(html_data)

    #htmlから不要なタグを削除
    for remove_tag in REMOVE_TAGS:
        for tag in root.findall(remove_tag):
            tag.drop_tree()

    texts=[]
    texts.append(['タグ名', 'タグテキスト', 'タグに属するテキスト'])

    # タイトルタグを取得
    t = root.find('.//title')
    if t is not None:
        text = t.text_content()

        #空でなければリストに追加
        if text:
            texts.append([t.tag, text, ''])

        print(f'(デバッグ) {t.tag}: {text}\n')

    for h_tag in root.xpath(XPATH_H_TAGS):
        # 見出しタグのテキストを取得
        h_text = h_tag.text_content()

        print(f'(デバッグ) {h_tag.tag}: {h_text}')

# 見出しタグと同じ階層にあったテキストを入れるリスト
        contents = []

        # 見出しの次のタグを取得
        next_tag = h_tag.getnext()

        # 次のタグがなくなるまでループ
        while next_tag is not None:
            # タグが見出しだったらブレーク
            if RE_H_MATCH(next_tag.tag):
                print(f'(デバッグ) 次の見出しタグ {next_tag.tag} が見つかった。')
                print(f'(デバッグ) while ブレーク\n')
                break

            # タグのテキストを取得
            text = next_tag.text_content()

            # 空でなければリストに追加
            if text:
                contents.append(text)

            print(f'(デバッグ) {next_tag.tag}: {text}')

            # さらに次のタグを取得してループする
            next_tag = next_tag.getnext()
        else:
            # 同じ階層のタグをたどり尽くして、次のタグが無かった場合。
            print(f'(デバッグ) 次のタグが無かった。 {next_tag}')

        # リストを連結してひとつの文字列にします
        contents = '|'.join(contents)

        # リストに追加
        texts.append([h_tag.tag, h_text, contents])

    # (8/8) テキストを CSV に保存します
    csv_file = Path("C:\pokemon.csv")
    with csv_file.open('w', encoding='UTF-8', newline='') as f:
        w = csv.writer(f)
        w.writerows(texts)

    # 以上です
    return


if __name__ == "__main__":
    main()