<div align="center">
  <h1>
    <br/>
    Limitime-QFluentKit
  </h1>

  <p>
    一个经过生产验证的 PyQt6 + <a href="https://github.com/zhiyiYo/PyQt-Fluent-Widgets">QFluentWidgets</a> 桌面应用模板。
    <br />
    <i>关键布局修复、JSON 国际化、AI Agent 友好 —— 克隆即用。</i>
  </p>
</div>

<!-- Badges -->
<div align="center">

![平台](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
[![许可证](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

[English Readme](README.md) | 简体中文说明

---

## 这是什么？

这**不是**一个框架或库。它是一个预配置、已修复 bug、克隆即用的桌面应用骨架，基于 PyQt6 和 QFluentWidgets 构建。

当你直接用裸 QFluentWidgets 开始写应用时，每次都会踩到同样的隐藏陷阱：
- 窗口缩放到 1008px 以下时，左侧边栏自动折叠消失
- 品牌 Logo 和标题被布局挤压到不可见
- 没有 i18n 系统、没有关于页面、没有配置持久化

本模板在你写**任何一行业务代码之前**就已经修复了所有这些问题。它经过了生产级应用的实战检验（[KeanSeatsCatcher](https://github.com/Daozhu1007/KeanSeatsCatcher)、[RhythmAlign](https://github.com/Daozhu1007/RhythmAlign)），然后被提取为可复用的形式。

---

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/yourusername/yourproject.git
cd yourproject

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行
python main.py
```

**环境要求：** Python 3.10+、PyQt6 >= 6.5、QFluentWidgets >= 1.5.0

---

## 项目结构

```
yourproject/
├── main.py              # QApplication 入口，高 DPI 配置
├── ui_main.py           # 主窗口（FluentWindow）+ 品牌组件 + 布局修复
├── ui_home.py           # 占位首页
├── ui_settings.py       # 设置页面（语言切换）
├── ui_about.py          # 关于页面（作者、版权、警告）
├── i18n.py              # JSON 国际化引擎 + 配置持久化
├── locales/
│   ├── zh_CN.json       # 中文翻译
│   └── en_US.json       # 英文翻译
├── assets/
│   ├── logo.png         # 侧边栏品牌 logo
│   └── logo.ico         # 窗口图标
└── CLAUDE.md            # 全面的 AI Agent 指令文档
```

---

## 核心功能（预应用的修复）

### 侧边栏防挤压保护

QFluentWidgets 的 `NavigationPanel` 有**两个独立的折叠阈值**。`eventFilter(Resize)` 处理器在窗口宽度低于 1008px 时会自动折叠侧边栏 —— 即使 `expand()` 的逻辑判断是展开。本模板将 `minimumExpandWidth` 设为 800，确保它始终低于窗口最小尺寸 900px，侧边栏**永远不会**自动折叠。

### 带锁定尺寸策略的品牌组件

Logo 图标使用 `QSizePolicy.Fixed` 策略，永不缩放。标题标签使用 `QSizePolicy.Minimum` 策略，最小宽度等于其文本自然宽度 —— 布局无法将其压窄。`setWordWrap(False)` 防止多行换行。

### JSON 国际化 + 配置持久化

与 KSC 和 RhythmAlign 完全兼容的 i18n 方案。语言选择写入 `config.json`，重启后自动恢复。添加一个新翻译 key 只需在两个 JSON 文件中各加一行。

### 面向 AI Agent 的 CLAUDE.md

一份 580+ 行的文档，教任何 AI 编程智能体（Claude Code、Codex、Cursor）如何使用本模板：项目结构、架构图、2 步创建新页面流程、全部 5 个关键布局约束及其源码级别的原理解释、常见踩坑、以及完整的可导入组件目录。

---

## 添加新页面

```python
# 1. 创建 ui_myfeature.py，包含一个 QWidget 子类
class MyFeatureInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("MyFeatureInterface")  # 必须设置
        ...

# 2. 在 ui_main.py 中注册
from ui_myfeature import MyFeatureInterface
self.myfeature_interface = MyFeatureInterface(self)
self.addSubInterface(
    self.myfeature_interface,
    FIF.DEVELOPER_TOOLS, "我的功能",
    position=NavigationItemPosition.SCROLL
)
```

完整说明见 [CLAUDE.md](CLAUDE.md)。

---

## 基于此模板开发的应用

- [KeanSeatsCatcher](https://github.com/Daozhu1007/KeanSeatsCatcher) — 肯恩大学课程空位监控与自动抢课工具
- [RhythmAlign](https://github.com/Daozhu1007/RhythmAlign) — 音游手元音频自动对齐工具

---

## 致谢

- **作者：** [Limitime](https://github.com/Daozhu1007)
- **UI 框架：** [zhiyiYo/PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)
- **设计灵感：** [ok-oldking/ok-wuthering-waves](https://github.com/ok-oldking/ok-wuthering-waves)

---

## 许可证

MIT — 自由使用，署名感谢。
