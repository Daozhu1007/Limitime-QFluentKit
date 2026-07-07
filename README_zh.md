# Limitime-QFluentKit

一个经过生产项目验证后提纯出来的 PyQt6 + QFluentWidgets 桌面应用模板。

它不是框架，也不是库，而是一个干净的应用外壳。模板保留每个新项目里都容易反复踩坑的通用部分：

- 稳定展开的左侧导航
- 不会被挤压消失的侧栏品牌区
- JSON 国际化与设置持久化
- 跟随主题的滚动页面背景
- 可复用的首页 / 设置 / 关于页面结构
- 高 DPI 图标与图片缩放工具

[English Readme](README.md) | 简体中文说明

## 快速开始

```bash
pip install -r requirements.txt
python main.py
```

环境要求：Python 3.10+、PyQt6 >= 6.5、PyQt6-Fluent-Widgets >= 1.5.0。

## 项目结构

```text
yourproject/
|-- main.py              # QApplication 入口
|-- app_config.py        # 应用常量与 QFluentWidgets 配置项
|-- ui_utils.py          # 资源、图标、主题和 ScrollArea 工具
|-- ui_main.py           # FluentWindow 外壳与导航
|-- ui_home.py           # 起始首页
|-- ui_settings.py       # 主题与语言设置
|-- ui_about.py          # 通用关于页
|-- i18n.py              # JSON 国际化加载器
|-- locales/
|   |-- zh_CN.json
|   `-- en_US.json
`-- assets/
    |-- github.png
    `-- bilibili.png
```

## 提纯了什么

这个模板参考了 RhythmAlign 等成熟项目中的可复用外壳经验，但不会带入任何具体业务逻辑。保留下来的精华包括导航行为、主题刷新、ScrollArea 背景处理、设置卡片、国际化和资源缩放。

## 自定义清单

1. 在 `app_config.py` 中修改应用名称、版本、作者和链接。
2. 替换 `assets/` 中的图标资源。
3. 把 `ui_home.py` 的占位首页替换成你的第一个真实页面。
4. 在两个 locale JSON 文件中同步新增翻译 key。
5. 在 `ui_main.py` 中注册新增页面。

## 许可

MIT。
