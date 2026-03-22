# RimWorld Mod Translator (Enhanced)

RimWorld Modの翻訳作業を支援する強化版Pythonツール。ModフォルダからXMLファイルを解析し、日本語翻訳テンプレートを自動生成します。

## ✨ 新機能（v2.0）

- 🔑 **Keyed翻訳対応**: UI・メッセージなどのKeyed文字列を抽出
- 📦 **Patches翻訳対応**: 他Mod互換性パッチの翻訳も可能
- 📂 **LoadFolders.xml生成**: バージョン別・DLC別の翻訳管理
- 📊 **翻訳進捗レポート**: 翻訳状況を可視化
- 🔄 **既存翻訳マージ**: 既存翻訳を保持しながら新規文字列を追加
- 🎯 **拡張フィールド対応**: 16種類の翻訳可能フィールドに対応

## 特徴

- ✨ **シンプル**: Python標準ライブラリのみ使用（外部依存なし）
- 🚀 **高速**: XMLパースで翻訳可能な文字列を一括抽出
- 📝 **完全対応**: DefInjected / Keyed / Patches すべてサポート
- 🎯 **RimWorld準拠**: v1.6対応、DefInjectedフォーマットに完全準拠

## インストール

### 前提条件
- Python 3.7以降

### セットアップ

```bash
git clone https://github.com/etejasdgjjjj532/RimWorldModTranslator.git
cd RimWorldModTranslator
```

外部ライブラリは不要です（Python標準ライブラリのみ使用）。

## 使い方

### 基本的な使用方法

```bash
python translator.py <RimWorld Modフォルダのパス>
```

例：
```bash
python translator.py "C:/Program Files (x86)/Steam/steamapps/workshop/content/294100/1234567890"
```

### オプション

```bash
python translator.py <Modパス> [オプション]
```

| オプション | 説明 |
|-----------|------|
| `-o, --output <パス>` | 翻訳ファイルの出力先（デフォルト: `./output`） |
| `-m, --merge` | 既存翻訳とマージ（既存の翻訳を保持） |
| `-r, --report` | 翻訳進捗レポートを生成 |
| `--no-keyed` | Keyed翻訳の抽出をスキップ |
| `--no-patches` | Patches翻訳の抽出をスキップ |

### 使用例

**完全抽出（推奨）:**
```bash
python translator.py "path/to/mod" -o "./translation" -r
```

**既存翻訳とマージ:**
```bash
python translator.py "path/to/mod" -m -r
```

**DefInjectedのみ:**
```bash
python translator.py "path/to/mod" --no-keyed --no-patches
```

### 出力構造

ツールは以下のような構造で翻訳テンプレートを生成します：

```
output/
├── Japanese/
│   ├── DefInjected/
│   │   ├── ThingDef.xml
│   │   ├── ResearchProjectDef.xml
│   │   └── ...
│   ├── Keyed/
│   │   └── Keys.xml
│   └── Patches/
│       └── PatchOperations.xml
├── LoadFolders.xml
└── TranslationReport.txt  (--report使用時)
```

各XMLファイルには翻訳待ちのエントリが含まれます：

```xml
<?xml version='1.0' encoding='UTF-8'?>
<LanguageData>
  <ThingDef.MyItem.label>TODO: Original English Text</ThingDef.MyItem.label>
  <ThingDef.MyItem.description>TODO: Original description here</ThingDef.MyItem.description>
</LanguageData>
```

## 翻訳ワークフロー

1. **抽出**: ツールを実行してテンプレートを生成
2. **翻訳**: 各XMLファイルの `TODO:` 部分を日本語に置換
3. **配置**: 翻訳済みファイルをModの `Languages/Japanese/` フォルダにコピー
4. **テスト**: RimWorldで動作確認
5. **更新**: Mod更新時は `-m` オプションで既存翻訳を保持

## 対応翻訳フィールド

以下16種類のフィールドを自動抽出します：

- `label`, `labelShort`, `labelMale`, `labelFemale`
- `description`, `descriptionShort`, `descriptionHyperlinks`
- `jobString`, `gerund`, `verb`
- `pawnSingular`, `pawnsPlural`
- `customLabel`, `skillLabel`
- `chargeNoun`, `destroyedLabel`

## 翻訳進捗レポート

`-r` オプションで生成される `TranslationReport.txt` の例：

```
RimWorld Mod Translation Report
Generated: 2026-03-22 12:00:00
============================================================

Total strings: 1,234
Translated: 856 (69.4%)
Untranslated: 378

============================================================
Untranslated strings:

ThingDef.Gun_Pistol.label: Pistol
ThingDef.Gun_Pistol.description: A simple pistol...
...
```

## RimTransとの比較

| 機能 | RimWorldModTranslator | RimTrans |
|------|----------------------|----------|
| 言語 | Python | TypeScript/C# |
| GUI | CLI | Electron GUI |
| 依存関係 | なし | Node.js/Electron |
| DefInjected | ✅ | ✅ |
| Keyed | ✅ | ✅ |
| Patches | ✅ | ❌ |
| LoadFolders.xml | ✅ 自動生成 | ❌ |
| 翻訳進捗レポート | ✅ | ❌ |
| 既存翻訳マージ | ✅ | ❌ |
| メンテナンス | 2026年（最新） | 2018年（停止） |
| 日本語特化 | ✅ | 中国語メイン |

## トラブルシューティング

### XMLパースエラー
```
Warning: Could not parse /path/to/file.xml: not well-formed
```
→ Modの元XMLファイルが壊れている可能性があります。Mod作者に報告してください。

### 翻訳が見つからない
```
No translatable content found.
```
→ Modフォルダのパスが正しいか確認してください。`Defs`フォルダが存在する必要があります。

### Keyedファイルがない
```
Extracting Keyed translations... (0 found)
```
→ 一部のModはKeyedファイルを持ちません。`--no-keyed`で警告を抑制できます。

## ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照

## 貢献

Pull Request歓迎！バグ報告や機能要望はIssuesへ。

## 参考資料

- [RimWorld公式](https://rimworldgame.com/)
- [RimWorld Modding Wiki](https://rimworldwiki.com/wiki/Modding_Tutorials)
- [RimWorld Localization Guide](https://rimworldwiki.com/wiki/Modding_Tutorials/Localization)
- [RimTrans (Original)](https://github.com/RimWorld-zh/RimTrans)

## 更新履歴

### v2.0 (2026-03-22)
- ✨ Keyed翻訳対応追加
- ✨ Patches翻訳対応追加
- ✨ LoadFolders.xml自動生成
- ✨ 翻訳進捗レポート機能
- ✨ 既存翻訳マージ機能
- 🎯 翻訳可能フィールドを16種類に拡張
- 🐛 XMLパースエラーハンドリング改善

### v1.0 (2026-03-22)
- 🎉 初回リリース
- ✨ DefInjected翻訳対応
