# marp2pptx

[English](README.md) | [中文](README.zh.md) | [한국어](README.ko.md)

[Marp](https://marp.app/) Markdownスライドを、**フォント自動サイズ調整付き**でPowerPoint (.pptx) に変換します。

## なぜ作ったのか？

MarpはMarkdownでスライドを書くのに最高のツールです。でも、Marp標準のPPTXエクスポート機能で出力されるファイルは、内部構造が気持ち悪くて実用性がありません。シェイプの配置がPowerPointのネイティブな構造と一致しない、テキストボックスの挙動が予想外、全体の構造がとってつけたような感じ——正直、あとから編集する気になれない品質です。

**marp2pptx** はまったく違うアプローチを取ります。MarpのHTMLレンダリングをPPTXに変換するのではなく、Markdownを直接パースして、python-pptxでゼロからPowerPointを構築します。結果として、きれいで編集しやすいPPTX、適切に構造化されたシェイプ、可読性を最大化する自動サイズフォント、そして完全なCJKサポートが得られます。

## 特徴

- **フォント自動サイズ調整**: オーバーフローしない最大のフォントサイズを自動検出
- **CJKサポート**: 全角・半角を考慮したテキスト幅計測
- **アスキーアート**: `arch-box` マーク付きコードブロックを等幅フォントでピクセルパーフェクトな画像としてレンダリング
- **テーブル対応**: HTMLテーブル・Markdownテーブルの両方に対応、折り返しを考慮した高さ推定
- **デザイン設定**: 色・フォント・フォントサイズ範囲をYAMLファイルで外部化
- **重なり検出**: 生成後にシェイプの重なりを自動チェック

## インストール

```bash
pip install git+https://github.com/ebibibi/marp2pptx.git
```

### アスキーアート用フォント

CJK文字を含むアスキーアートのレンダリングには、等幅CJKフォントが必要です：

```bash
# Ubuntu/Debian
sudo apt install fonts-ipafont-gothic

# Fedora
sudo dnf install ipa-gothic-fonts
```

利用可能なフォントを自動検出します（IPAGothic、Noto Sans Mono CJK、MS Gothic、Osaka、DejaVu）。

## 使い方

```bash
# 基本
marp2pptx slides.md

# 出力パスを指定
marp2pptx slides.md -o presentation.pptx

# 重なりチェックをスキップ
marp2pptx slides.md --no-check
```

Pythonモジュールとしても実行可能：

```bash
python -m marp2pptx slides.md
```

### Python API

```python
from marp2pptx import convert

output_path, slide_count = convert("slides.md")
```

## デザイン設定

YAMLファイルでデザインをカスタマイズできます。設定ファイルの解決順序：

1. `<入力ファイル>.yaml`（例：`slides.md` → `slides.yaml`）
2. 同じディレクトリの `marp2pptx.yaml`
3. ビルトインデフォルト

`slides.yaml` の例：

```yaml
colors:
  accent: "#FF6600"
  text: "#333333"

fonts:
  main: "Arial"
  mono: "Courier New"

font_ranges:
  default: [40, 14, 36]  # [タイトル最大, 本文最小, 本文最大]
  small: [36, 12, 28]
```

全オプションは [`default.yaml`](src/marp2pptx/default.yaml) を参照してください。

## 対応するMarkdown記法

- Marpフロントマター（`---` / `marp: true`）
- スライド区切り（`---`）
- クラスディレクティブ（`<!-- _class: lead -->`）
- 背景画像（`![bg right:30% 80%](image.png)`）
- 見出し（h1〜h3）
- 箇条書き（ネスト対応）
- Markdownテーブル・HTMLテーブル
- コードブロック
- アスキーアートブロック（`<div class="arch-box">`）
- インライン書式：**太字**、*斜体*、`コード`、リンク、`<span class="tag-xxx">`

## ライセンス

MIT
