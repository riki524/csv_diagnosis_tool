# CSV診断ツール

## 概要
CSVファイルのデータ品質を自動で診断するツールです。
データ分析・集計作業の前処理として、問題のある箇所を素早く把握できます。

## こんな課題を解決します
- 「CSVを開いたが、どこに問題があるかわからない」
- 「欠損値や重複行を手作業で確認するのが面倒」
- 「データ型が正しいか確認したい」

## 主な機能
- 行数・列数・列名・データ型の確認
- 欠損値の検出（列ごとの件数表示）
- 重複行の検出
- 数値列・日付列の自動判定
- 診断結果のMarkdownレポート自動出力

## 使用技術
- Python 3
- pandas
- pathlib

## フォルダ構成
```text
csv_diagnosis_tool/
├─ main.py
├─ input/
│  ├─ sample.csv
│  └─ sample_clean.csv
├─ output/
│  └─ diagnosis_report.md
└─ README.md
```

## 実行方法
```powershell
py main.py
```
実行後、診断結果が `output/diagnosis_report.md` に出力されます。