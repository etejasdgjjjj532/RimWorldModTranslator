RimWorld Mod Translator

RimWorld Modの翻訳作業を支援するPythonツールです。

Mod内のXMLファイルを解析し、DefInjectedやKeyedなどの翻訳対象文字列を抽出できます。抽出したデータはExcel（XLSX）形式で出力でき、既存の日本語翻訳を利用した作業にも対応しています。

現在も開発中のため、一部の機能は未実装または簡易実装です。

主な機能

実装済み

* DefInjected抽出
    * Modの Defs フォルダを解析
    * 翻訳対象となるフィールドを抽出
    * Def名、元テキスト、ファイル名などを取得
* Keyed抽出
    * Languages/English/Keyed 内のXMLを解析
    * Keyed形式の翻訳対象を抽出
* Excel（XLSX）出力
    * DefInjectedとKeyedをシート別に出力
    * 翻訳作業用データとして利用可能
* 既存DefInjected翻訳の読み込み
    * Languages/Japanese/DefInjected 内の既存翻訳を読み込み
    * 抽出データへ既存翻訳を反映
* GUI
    * Tkinterを使用した簡易GUI
    * Modフォルダを選択して翻訳対象を抽出可能

開発中・未実装

以下の機能はコード上に構想または一部処理がありますが、現在は完全には実装されていません。

* XML翻訳テンプレートの自動生成
* Patchesの翻訳抽出
* Keyedの既存翻訳マージ
* LoadFolders.xmlの自動生成
* 翻訳進捗レポート
* 複雑なXML階層・リスト構造への完全対応
* ParentDefなどの継承関係を利用した高度な解析

必要環境

* Python 3.7以降
* pandas
* openpyxl

インストール

リポジトリをクローンします。

git clone https://github.com/etejasdgjjjj532/RimWorldModTranslator.git
cd RimWorldModTranslator

必要なPythonパッケージをインストールします。

pip install -r requirements.txt

使い方

GUI

python gui.py

GUIからRimWorld Modのフォルダを選択し、翻訳対象を抽出できます。

CLI

Excel形式で抽出する場合：

python translator.py "path/to/mod" --xlsx

出力先を指定する場合：

python translator.py "path/to/mod" --xlsx -o "./translation"

既存の日本語DefInjected翻訳を読み込む場合：

python translator.py "path/to/mod" --xlsx --merge

CLIオプション

オプション	説明
-o, --output <path>	出力フォルダを指定
-x, --xlsx	Excel（XLSX）形式で出力
-m, --merge	既存の日本語DefInjected翻訳を読み込む

Excel出力

現在の主要な出力形式はXLSXです。

翻訳対象が存在する場合、以下のシートが生成されます。

* DefInjected
* Keyed

DefInjectedでは主に以下の情報を出力します。

* Def Type
* 翻訳パス
* 原文
* 翻訳
* 元ファイル
* ParentDef

Keyedでは主に以下を出力します。

* Key
* 原文
* 翻訳
* 元ファイル

対応している翻訳対象

Def XML内では、label、description、jobString、text、inspectString など複数の翻訳対象フィールドを検出します。

現在の抽出処理は比較的単純なXML構造を対象としており、ネストされた要素やリスト内に同名フィールドが複数存在する場合など、複雑なDefでは正確なDefInjectedパスを生成できない可能性があります。

既存翻訳の利用

--merge を指定すると、

Languages/Japanese/DefInjected/

内のXMLファイルから既存翻訳を読み込み、抽出結果へ反映します。

現時点ではKeyedの既存翻訳読み込みには完全対応していません。

プロジェクトの方向性

今後は以下の機能を順次改善する予定です。

* DefInjectedパス生成の改善
* XML翻訳テンプレート生成
* Keyed翻訳マージ
* Patches対応
* 翻訳進捗レポート
* LoadFolders.xml生成
* XML継承・参照処理
* GUIの改善

注意事項

このツールは開発中です。

ModによってXML構造が大きく異なるため、すべてのRimWorld Modで正確な翻訳データを生成できることを保証するものではありません。

生成・抽出したデータは、実際にModへ導入する前に内容を確認してください。

ライセンス

MIT License

詳細は LICENSE を参照してください。

参考

* RimWorld
* RimWorld Modding Wiki
* RimWorld Localization Guide
* RimTrans

RimTransおよび既存のRimWorld翻訳ツールの設計・考え方を参考にしています。
