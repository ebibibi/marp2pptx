# marp2pptx

[English](README.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

将 [Marp](https://marp.app/) Markdown 幻灯片转换为 PowerPoint (.pptx)，支持**字体自动调整大小**。

## 为什么要做这个？

Marp 是用 Markdown 写幻灯片的优秀工具——但它内置的 PPTX 导出功能生成的文件内部结构混乱，几乎无法用于后续编辑。形状的放置方式与 PowerPoint 原生组织内容的方式不匹配，文本框行为异常，整体结构给人一种事后补丁的感觉，而不是一个正式的输出格式。

**marp2pptx** 采用了完全不同的方法：它不是将 Marp 的 HTML 渲染转换为 PPTX，而是直接解析 Markdown，使用 python-pptx 从零构建 PowerPoint。结果是一个干净、可编辑的 PPTX，具有正确结构化的形状、自动调整大小以最大化可读性的字体，以及完整的 CJK 支持。

## 特性

- **字体自动调整**：自动找到不会溢出的最大字号
- **CJK 支持**：全角/半角感知的文本宽度测量
- **ASCII 艺术**：将标记为 `arch-box` 的代码块渲染为像素级精确的等宽字体图像
- **表格支持**：HTML 和 Markdown 表格，带有自动换行感知的高度估算
- **设计配置**：通过 YAML 文件外部化颜色、字体和字号范围
- **重叠检测**：自动检查生成的形状是否重叠

## 安装

```bash
pip install git+https://github.com/ebibibi/marp2pptx.git
```

### ASCII 艺术字体

渲染包含 CJK 字符的 ASCII 艺术需要等宽 CJK 字体：

```bash
# Ubuntu/Debian
sudo apt install fonts-ipafont-gothic

# Fedora
sudo dnf install ipa-gothic-fonts
```

工具会自动检测可用字体（IPAGothic、Noto Sans Mono CJK、MS Gothic、Osaka、DejaVu）。

## 使用方法

```bash
# 基本用法
marp2pptx slides.md

# 指定输出路径
marp2pptx slides.md -o presentation.pptx

# 跳过重叠检查
marp2pptx slides.md --no-check
```

也可以作为 Python 模块运行：

```bash
python -m marp2pptx slides.md
```

### Python API

```python
from marp2pptx import convert

output_path, slide_count = convert("slides.md")
```

## 设计配置

创建 YAML 文件来自定义设计。工具按以下顺序查找配置：

1. `<输入文件>.yaml`（例如：`slides.md` 对应 `slides.yaml`）
2. 同目录下的 `marp2pptx.yaml`
3. 内置默认值

`slides.yaml` 示例：

```yaml
colors:
  accent: "#FF6600"
  text: "#333333"

fonts:
  main: "Arial"
  mono: "Courier New"

font_ranges:
  default: [40, 14, 36]  # [标题最大, 正文最小, 正文最大]
  small: [36, 12, 28]
```

所有选项请参见 [`default.yaml`](src/marp2pptx/default.yaml)。

## 支持的 Markdown 语法

- Marp frontmatter（`---` / `marp: true`）
- 幻灯片分隔符（`---`）
- 类指令（`<!-- _class: lead -->`）
- 背景图片（`![bg right:30% 80%](image.png)`）
- 标题（h1–h3）
- 项目列表（支持嵌套）
- Markdown 和 HTML 表格
- 代码块
- ASCII 艺术块（`<div class="arch-box">`）
- 行内格式：**粗体**、*斜体*、`代码`、链接、`<span class="tag-xxx">`

## 许可证

MIT
