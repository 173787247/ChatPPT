import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from utils import remove_all_slides
from logger import LOG  # 引入日志模块

# 生成 PowerPoint 演示文稿
def generate_presentation(powerpoint_data, template_path: str, output_path: str):
    # 检查模板文件是否存在
    if not os.path.exists(template_path):
        LOG.error(f"模板文件 '{template_path}' 不存在。")  # 记录错误日志
        raise FileNotFoundError(f"模板文件 '{template_path}' 不存在。")

    prs = Presentation(template_path)  # 加载 PowerPoint 模板
    remove_all_slides(prs)  # 清除模板中的所有幻灯片
    prs.core_properties.title = powerpoint_data.title  # 设置 PowerPoint 的核心标题

    # 遍历所有幻灯片数据，生成对应的 PowerPoint 幻灯片
    for slide in powerpoint_data.slides:
        # 确保布局索引不超出范围，超出则使用默认布局
        if slide.layout_id >= len(prs.slide_layouts):
            slide_layout = prs.slide_layouts[0]
        else:
            slide_layout = prs.slide_layouts[slide.layout_id]

        new_slide = prs.slides.add_slide(slide_layout)  # 添加新的幻灯片

        # 设置幻灯片标题
        if new_slide.shapes.title:
            new_slide.shapes.title.text = slide.content.title
            LOG.debug(f"设置幻灯片标题: {slide.content.title}")

        # 添加文本内容
        for shape in new_slide.shapes:
            # 只处理非标题的文本框
            if shape.has_text_frame and not shape == new_slide.shapes.title:
                text_frame = shape.text_frame
                text_frame.clear()  # 清除原有内容
                # 将要点内容作为项目符号列表添加到文本框中
                for point in slide.content.bullet_points:
                    p = text_frame.add_paragraph()
                    p.text = point
                    p.level = 0  # 项目符号的级别
                    LOG.debug(f"添加列表项: {point}")
                break

        # 插入图片
        if slide.content.image_path:
            image_full_path = os.path.join(os.getcwd(), slide.content.image_path)  # 构建图片的绝对路径
            if os.path.exists(image_full_path):
                # 插入图片到占位符中
                for shape in new_slide.placeholders:
                    if shape.placeholder_format.type == 18:  # 18 表示图片占位符
                        shape.insert_picture(image_full_path)
                        LOG.debug(f"插入图片: {image_full_path}")
                        break
            else:
                LOG.warning(f"图片路径 '{image_full_path}' 不存在，跳过此图片。")
        
        # 插入表格（如果内容包含表格数据）
        if hasattr(slide.content, 'table_data') and slide.content.table_data:
            _insert_table(new_slide, slide.content.table_data)
        
        # 插入图表（如果内容包含图表数据）
        if hasattr(slide.content, 'chart_data') and slide.content.chart_data:
            _insert_chart(new_slide, slide.content.chart_data)

    # 保存生成的 PowerPoint 文件
    prs.save(output_path)
    LOG.info(f"演示文稿已保存到 '{output_path}'")


def _insert_table(slide, table_data: dict):
    """
    在幻灯片中插入表格
    
    Args:
        slide: 幻灯片对象
        table_data: 表格数据字典，包含 'rows', 'cols', 'data'
    """
    try:
        rows = table_data.get('rows', 2)
        cols = table_data.get('cols', 2)
        data = table_data.get('data', [])
        
        # 查找表格占位符
        table_placeholder = None
        for shape in slide.placeholders:
            if shape.placeholder_format.type == 12:  # 12 表示表格占位符
                table_placeholder = shape
                break
        
        if table_placeholder:
            # 使用占位符创建表格
            graphic_frame = table_placeholder.insert_table(rows, cols)
            table = graphic_frame.table
        else:
            # 如果没有占位符，在幻灯片上添加表格
            left = Inches(1)
            top = Inches(2)
            width = Inches(8)
            height = Inches(4)
            graphic_frame = slide.shapes.add_table(rows, cols, left, top, width, height)
            table = graphic_frame.table
        
        # 填充表格数据
        for i, row_data in enumerate(data[:rows]):
            for j, cell_data in enumerate(row_data[:cols]):
                if i < len(table.rows) and j < len(table.columns):
                    cell = table.cell(i, j)
                    cell.text = str(cell_data) if cell_data else ""
                    # 设置第一行为表头样式
                    if i == 0:
                        for paragraph in cell.text_frame.paragraphs:
                            for run in paragraph.runs:
                                run.font.bold = True
        
        LOG.debug(f"插入表格：{rows}行 x {cols}列")
    except Exception as e:
        LOG.warning(f"插入表格失败: {str(e)}")


def _insert_chart(slide, chart_data: dict):
    """
    在幻灯片中插入图表
    
    Args:
        slide: 幻灯片对象
        chart_data: 图表数据字典，包含 'chart_type', 'categories', 'series'
    """
    try:
        chart_type = chart_data.get('chart_type', 'column')  # 默认柱状图
        categories = chart_data.get('categories', [])
        series_data = chart_data.get('series', {})
        
        # 查找图表占位符
        chart_placeholder = None
        for shape in slide.placeholders:
            if shape.placeholder_format.type == 20:  # 20 表示图表占位符
                chart_placeholder = shape
                break
        
        if not chart_placeholder:
            # 如果没有占位符，在幻灯片上添加图表
            left = Inches(1)
            top = Inches(2)
            width = Inches(8)
            height = Inches(4.5)
            chart_placeholder = slide.shapes.add_chart(
                XL_CHART_TYPE.COLUMN_CLUSTERED,
                left, top, width, height
            )
        
        # 准备图表数据
        chart_data_obj = CategoryChartData()
        chart_data_obj.categories = categories
        
        # 添加系列数据
        for series_name, values in series_data.items():
            chart_data_obj.add_series(series_name, values)
        
        # 更新图表
        chart = chart_placeholder.chart
        chart.replace_data(chart_data_obj)
        
        # 根据类型设置图表类型
        chart_type_map = {
            'column': XL_CHART_TYPE.COLUMN_CLUSTERED,
            'bar': XL_CHART_TYPE.BAR_CLUSTERED,
            'line': XL_CHART_TYPE.LINE,
            'pie': XL_CHART_TYPE.PIE,
        }
        if chart_type.lower() in chart_type_map:
            chart.chart_type = chart_type_map[chart_type.lower()]
        
        LOG.debug(f"插入图表：{chart_type}，{len(categories)}个类别")
    except Exception as e:
        LOG.warning(f"插入图表失败: {str(e)}")
