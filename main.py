# CSVを読み込んで診断するために、pandasライブラリを使います。
import pandas as pd

# ファイルやフォルダの場所を扱いやすくするために、Pathを使います。
from pathlib import Path


# main.py が置いてあるフォルダの場所を取得します。
BASE_DIR = Path(__file__).resolve().parent


# 読み込むCSVファイル名を指定します。
INPUT_FILE_NAME = "sample_clean.csv"

# inputフォルダの場所を指定します。
INPUT_DIR = BASE_DIR / "input"

# outputフォルダの場所を指定します。
OUTPUT_DIR = BASE_DIR / "output"

# 読み込むCSVファイルの場所を指定します。
INPUT_FILE = INPUT_DIR / INPUT_FILE_NAME

# 診断結果を保存するファイル名を指定します。
OUTPUT_FILE = OUTPUT_DIR / f"diagnosis_report_{Path(INPUT_FILE_NAME).stem}.md"



# 日付として使えそうな列を探す関数です。
def find_date_like_columns(df):
    # 日付列候補を入れるための空リストを作ります。
    date_like_columns = []

    # CSVの列を1列ずつ確認します。
    for column_name in df.columns:
        # 列名に「日付」や「date」が含まれない列は、日付判定をしません。
        if "日付" not in column_name and "date" not in column_name.lower():
            continue
        # 数値列は日付候補から外します。
        if pd.api.types.is_numeric_dtype(df[column_name]):
            continue

        # 空欄ではないデータだけを取り出します。
        non_empty_values = df[column_name].dropna()

        # 空欄ではないデータが1つもなければ、次の列へ進みます。
        if len(non_empty_values) == 0:
            continue

        # その列の値を日付に変換できるか試します。
        converted_dates = pd.to_datetime(non_empty_values, errors="coerce")

        # 日付に変換できたデータの数を数えます。
        success_count = converted_dates.notna().sum()

        # 空欄ではないデータのうち、8割以上が日付に変換できれば日付列候補にします。
        if success_count / len(non_empty_values) >= 0.8:
            date_like_columns.append(column_name)

    # 見つけた日付列候補を返します。
    return date_like_columns


# CSVの診断レポート本文を作る関数です。
def create_diagnosis_report(df):
    # 行数と列数を取得します。
    row_count, column_count = df.shape

    # 重複している行の数を数えます。
    duplicate_count = df.duplicated().sum()

    # 数値として扱われている列を取得します。
    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    # 日付として使えそうな列を取得します。
    date_like_columns = find_date_like_columns(df)

    # レポート本文を1行ずつ入れるための空リストを作ります。
    lines = []

    # レポートのタイトルを追加します。
    lines.append("# CSV診断レポート")
    lines.append("")

    # 読み込んだファイル名を追加します。
    lines.append("## 1. 読み込んだファイル")
    lines.append(f"- {INPUT_FILE}")
    lines.append("")

    # 行数と列数を追加します。
    lines.append("## 2. 行数・列数")
    lines.append(f"- 行数: {row_count}")
    lines.append(f"- 列数: {column_count}")
    lines.append("")

    # 列名一覧を追加します。
    lines.append("## 3. 列名一覧")
    for column_name in df.columns:
        lines.append(f"- {column_name}")
    lines.append("")

    # 各列のデータ型を追加します。
    lines.append("## 4. データ型")
    for column_name, dtype in df.dtypes.items():
        lines.append(f"- {column_name}: {dtype}")
    lines.append("")

    # 欠損値の数を追加します。
    lines.append("## 5. 欠損値の数")
    missing_counts = df.isna().sum()
    for column_name, missing_count in missing_counts.items():
        lines.append(f"- {column_name}: {missing_count}")
    lines.append("")

    # 重複行の数を追加します。
    lines.append("## 6. 重複行数")
    lines.append(f"- 重複行数: {duplicate_count}")
    lines.append("")

    # 数値列候補を追加します。
    lines.append("## 7. 数値列候補")
    if numeric_columns:
        for column_name in numeric_columns:
            lines.append(f"- {column_name}")
    else:
        lines.append("- 数値列候補は見つかりませんでした。")
    lines.append("")

    # 日付列候補を追加します。
    lines.append("## 8. 日付列候補")
    if date_like_columns:
        for column_name in date_like_columns:
            lines.append(f"- {column_name}")
    else:
        lines.append("- 日付列候補は見つかりませんでした。")
    lines.append("")

        # 診断コメントを追加します。
    lines.append("## 9. 診断コメント")

    # 欠損値または重複行がある場合は、総合判定を「要確認」にします。
    if missing_counts.sum() > 0 or duplicate_count > 0:
        lines.append("- 総合判定: 要確認")
    else:
        lines.append("- 総合判定: 大きな問題は見つかりませんでした")

        # 欠損値が1つでもあるか確認します。
    if missing_counts.sum() > 0:
        # 欠損値がある列名だけを取り出します。
        missing_column_names = missing_counts[missing_counts > 0].index.tolist()

        # 列名を「, 」でつないで、1つの文字列にします。
        missing_column_text = ", ".join(missing_column_names)

        # 欠損値がある列名を診断コメントに追加します。
        lines.append(f"- 欠損値が含まれる列があります: {missing_column_text}")
    else:
        lines.append("- 欠損値はありません。")

       # 重複行が1行でもあるか確認します。
    if duplicate_count > 0:
        lines.append(f"- 重複行が{duplicate_count}行あります。")
    else:
        lines.append("- 重複行はありません。")

    # 日付列候補があるか確認します。
    if date_like_columns:
        date_column_text = ", ".join(date_like_columns)
        lines.append(f"- 日付列候補があります: {date_column_text}")
    else:
        lines.append("- 日付列候補は見つかりませんでした。")

    # 数値列候補があるか確認します。
    if numeric_columns:
        numeric_column_text = ", ".join(numeric_columns)
        lines.append(f"- 数値列候補があります: {numeric_column_text}")
    else:
        lines.append("- 数値列候補は見つかりませんでした。")                

    # 見やすくするために空行を追加します。
    lines.append("")

    # リストに入れた文章を、改行でつなげて1つの文章にします。
    return "\n".join(lines)


# メイン処理を書く関数です。
# メイン処理を書く関数です。
def main():
    # outputフォルダがなければ作ります。
    OUTPUT_DIR.mkdir(exist_ok=True)

    # inputフォルダ内にあるCSVファイル一覧を取得します。
    csv_files = list(INPUT_DIR.glob("*.csv"))

    # CSVファイルが見つからない場合は、メッセージを表示して処理を終了します。
    if not csv_files:
        print("inputフォルダ内にCSVファイルが見つかりませんでした。")
        return

    # 見つかったCSVファイルと、出力予定のレポート名を画面に表示します。
    print("=== inputフォルダ内のCSVファイル一覧 ===")

    # CSVファイルを1つずつ処理します。
    for csv_file in csv_files:
        # 出力するMarkdownファイルの保存先を作ります。
        output_file = OUTPUT_DIR / f"diagnosis_report_{csv_file.stem}.md"

        # どのCSVからどのレポートを作るかを表示します。
        print(f"{csv_file.name} -> {output_file.name}")

        # CSVファイルを読み込みます。
        df = pd.read_csv(csv_file, encoding="utf-8-sig")

        # 診断レポート本文を作ります。
        report_text = create_diagnosis_report(df)

        # 診断レポートをMarkdownファイルとして保存します。
        output_file.write_text(report_text, encoding="utf-8")

    # 全CSVの処理が終わったことを表示します。
    print("\nすべてのCSV診断レポートを保存しました。")
    
# このファイルを直接実行したときだけ、main関数を動かします。
if __name__ == "__main__":
    main()