# ChatPPT v0.1 - Fair Frames 布局更新

## 更新说明

本次更新将 ChatPPT v0.1 的模板从 `MasterTemplate.pptx` 替换为微软官方的 `Fair frames presentation.pptx`，并使用其布局名称。

## Fair frames presentation.pptx 布局列表

Fair frames presentation.pptx 包含以下 13 个布局：

1. **Title** (布局 0) - 标题页
2. **Agenda** (布局 1) - 议程页
3. **Section Header 1** (布局 2) - 章节标题页（带图片）
4. **Section Header 2** (布局 3) - 章节标题页（带文本）
5. **Introduction** (布局 4) - 介绍页
6. **Section Header 3** (布局 5) - 章节标题页（带图片和文本）
7. **Comparison** (布局 6) - 对比页
8. **Two Content 2** (布局 7) - 两列内容页
9. **Summary** (布局 8) - 总结页（带图片）
10. **Title Content and Table** (布局 9) - 标题、内容和表格页
11. **Two Content** (布局 10) - 两列内容页
12. **Table** (布局 11) - 表格页
13. **Thank you** (布局 12) - 感谢页

## 布局映射对比

### 原始模板 (MasterTemplate.pptx)
- `Title Only` → 标题页
- `Title and Content` → 标题和内容页
- `Title and Picture 1` → 标题和图片页
- `Title and 2 Column` → 标题和两列页

### 新模板 (Fair frames presentation.pptx)
- `Title` → 标题页
- `Introduction` → 介绍页（类似 Title and Content）
- `Summary` → 总结页（类似 Title and Picture）
- `Two Content` → 两列内容页
- `Agenda` → 议程页
- `Thank you` → 感谢页

## 使用方法

在输入文本中使用布局名称时，使用 Fair frames 的布局名称：

```markdown
# 演示文稿标题

## 幻灯片标题 [Title]
## 议程 [Agenda]
## 介绍内容 [Introduction]
## 总结 [Summary]
## 两列内容 [Two Content]
## 感谢 [Thank you]
```

## 代码修改

主要修改了以下文件：

1. **src/main.py**
   - 将模板文件路径从 `templates/MasterTemplate.pptx` 改为 `Fair frames presentation.pptx`
   - 更新示例输入文本，使用新的布局名称

2. **analyze_fair_frames.py** (新增)
   - 用于分析 Fair frames presentation.pptx 的布局结构

## 测试

运行以下命令生成 PPT：

```bash
cd src
python main.py
```

生成的 PPT 文件将保存在 `outputs/` 目录下。

## 验证

生成的 PPT 文件应：
1. 使用 Fair frames presentation.pptx 的母版样式
2. 内容正确匹配到对应的布局
3. 图片正确插入到图片占位符
4. 文本正确填充到文本占位符

