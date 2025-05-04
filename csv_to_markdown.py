import csv
from pathlib import Path
from datetime import datetime

# 定义作者信息
author = "Farhill Studio"

# 定义 CSV 文件路径
csv_path = Path("ai_tools.csv")

# 检查 CSV 文件是否存在
if not csv_path.exists():
    print(f"错误：未找到 {csv_path} 文件。")
else:
    # 读取 CSV 数据，使用 utf-8-sig 编码自动去除 BOM
    data = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames  # 获取表头
        for row in reader:
            # 统一替换网站介绍列的换行符
            if fieldnames[3] in row:
                row[fieldnames[3]] = row[fieldnames[3]].replace("\n", "<br>")
            data.append(row)

    # 生成 Markdown 文件路径
    md_path = Path("ai_tools.md")

    # 按网站类别（标签）分组
    tag_groups = {}
    for item in data:
        for tag in item[fieldnames[2]].split(","):
            tag = tag.strip()
            if tag not in tag_groups:
                tag_groups[tag] = []
            tag_groups[tag].append(item)

    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 生成 Markdown 文件
    with open(md_path, "w", encoding="utf-8") as f:
        # 写入文件标题
        f.write("# 中国优秀AI工具列表\n")
        # 写入作者信息
        f.write(f"- 作者: {author}\n")
        # 写入当前时间
        f.write(f"- 时间: {current_time}\n")
        # 写入当前时间
        f.write(f"- 说明: 本文档由脚本自动生成，请勿编辑\n\n\n\n")

        for tag, items in tag_groups.items():
            f.write(f"\n\n# {tag} 工具列表\n\n")
            # 调整表头，合并名称和网址
            new_fieldnames = [field for field in fieldnames if field != "网址"]
            header_line = "| " + " | ".join(new_fieldnames) + " |\n"
            separator_line = "| " + " | ".join(["---"] * len(new_fieldnames)) + " |\n"
            f.write(header_line)
            f.write(separator_line)
            for item in items:
                row_data = []
                # 合并名称和网址为带链接的一列
                name_with_link = f"[{item['名称']}]({item['网址']})"
                row_data.append(name_with_link)
                for field in fieldnames[2:]:
                    row_data.append(item[field])
                line = "| " + " | ".join(row_data) + " |\n"
                f.write(line)
    