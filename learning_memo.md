今回追加した処理：

inputフォルダ内のCSVファイルを探して、
それぞれのCSVから作られる予定のレポート名を表示した。

sample.csv なら diagnosis_report_sample.md
sample_clean.csv なら diagnosis_report_sample_clean.md

今回出た NameError は、
OUTPUT_DIR を定義する前に使ったことが原因だった。
Pythonは上から順番に実行するので、
使う変数は先に作っておく必要がある。

## 4日目メモ

### CSV一覧表示

今回追加した処理：

inputフォルダ内のCSVファイルを探して、それぞれのCSVから作られる予定のレポート名を表示した。

- sample.csv → diagnosis_report_sample.md
- sample_clean.csv → diagnosis_report_sample_clean.md

### NameErrorについて

今回出た `NameError` は、`OUTPUT_DIR` を定義する前に使ったことが原因だった。

Pythonは上から順番に実行するので、使う変数は先に作っておく必要がある。

### csv_filesについて

`csv_files` には、inputフォルダ内で見つかったCSVファイルの一覧が入っている。

`for`文で1つずつ `csv_file` として取り出し、`csv_file.name` で `sample.csv` のようなファイル名だけを表示している。

### 今日の理解ポイント

`csv_file` は、CSVファイルの場所情報を持っている。

- `csv_file.name` → ファイル名だけ
- `csv_file.stem` → 拡張子なしの名前
- `csv_file.suffix` → 拡張子

## 5日目メモ：main と __main__ の整理

- main.py はファイル名。
- def main(): は、main という関数を定義する書き方。
- main() は、def main(): で作った関数を実行する書き方。
- "__main__" はファイル名ではなく、「このPythonファイルが直接実行された」という印。
- 基本形は、def main(): で処理をまとめて、最後に if __name__ == "__main__": main() と書く。

## 5日目メモ：main.py の全体地図

main.py は、大きく分けると次の流れで動いている。

1. 準備
   - pandas や pathlib を使えるようにする
   - input フォルダ、output フォルダ、入力CSV、出力レポートの場所を決める

2. 日付列候補を探す関数
   - find_date_like_columns(df)
   - CSVの中から、日付として使えそうな列を探す

3. 診断レポート本文を作る関数
   - create_diagnosis_report(df)
   - 行数、列数、列名、データ型、欠損値、重複、数値列、日付列、総合判定を文章にする
   - 最後に return "\n".join(lines) で、1つのMarkdown本文として返す

4. メイン処理
   - main()
   - outputフォルダを作る
   - CSVを読み込む
   - 診断レポート本文を作る
   - Markdownファイルとして保存する
   - ターミナルにも表示する

5. 実行の入口
   - if __name__ == "__main__":
   - main.py を直接実行したときだけ main() を動かす

   ## 5日目メモ：DIR と FILE の違い

- DIR は directory の略で、フォルダの場所を表す。
- FILE は file のことで、ファイルの場所を表す。
- INPUT_DIR は input フォルダの場所。
- OUTPUT_DIR は output フォルダの場所。
- INPUT_FILE は 読み込むCSVファイルのパス。
- OUTPUT_FILE は 保存するMarkdownファイルのパス。
- INPUT_FILE_NAME は ファイル名だけ。