#!/usr/bin/python
from prettytable import PrettyTable

# x = PrettyTable()
# x.title = 'Table 2 City Info'
# x.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
# x.add_rows(
#     [
#         ["Adelaide", 1295, 1158259, 600.5],
#         ["Brisbane", 5905, 1857594, 1146.4],
#         ["Darwin", 112, 120900, 1714.7],
#         ["Hobart", 1357, 205556, 619.5],
#         ["Sydney", 2058, 4336374, 1214.8],
#         ["Melbourne", 1566, 3806092, 646.9],
#         ["Perth", 5386, 1554769, 869.4],
#     ]
# )
#
# print(x)

# from prettytable import PrettyTable
#
# x = PrettyTable()
# x.title = 'Table 3 City Info'
# x.add_column("City name",
# ["Adelaide","Brisbane","Darwin","Hobart","Sydney","Melbourne","Perth"])
# x.add_column("Area", [1295, 5905, 112, 1357, 2058, 1566, 5386])
#
#
# x.add_columns()
# print(x)


from prettytable import from_csv
#
# with open("data.csv") as fp:
#     mytable = from_csv(fp)
#     mytable.title = '表 4 天气详情'
#     print(mytable)


# import sqlite3
# from prettytable import from_db_cursor
#
# connection = sqlite3.connect("sqlite.db")
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM COMPANY")
# mytable = from_db_cursor(cursor)
# mytable.title = 'table 5 database info'
# print('原始表格输出：')
# print(mytable)

# print('\n删除某行后的输出：')
# mytable.del_row(1)
# print(mytable)

# print('\n删除某列后的输出：')
# mytable.del_column('ADDRESS')
# print(mytable)

# print('\n清理所有行，但保留字段名后的输出：')
# mytable.clear_rows()
# print(mytable)


# print('\n清理所有行，以及字段名后的输出：')
# mytable.clear()
# print(mytable)
# print(mytable.get_string())


# from prettytable import PrettyTable
#
# x = PrettyTable()
# x.title = '表6 多语言测试'
# x.field_names = ["序号", "中文名", "平假名", "英文"]
# x.add_rows(
#     [
#         [1, "东京", "とぅきよぅ", "Tokyo"],
#         [2, "北海道", "ほっかいどう", "Hokkaido"],
#         [3, "横滨", "よこはま", "Yokohama"],
#         [4, "名古屋", "なごやし", "Nagoya"],
#     ]
# )
#
# print(x)
#
#
# class MyPrettyTable(PrettyTable):
#     def add_row(self, row, *, divider=True) -> None:
#         super().add_row(row, divider=divider)
#
#
# x = MyPrettyTable()
# x.title = '表6 多语言测试'
# x.field_names = ["序号", "中文名", "平假名", "英文"]
# x.add_rows(
#     [
#         [1, "东京", "とぅきよぅ", "Tokyo"],
#         [2, "北海道", "ほっかいどう", "Hokkaido"],
#         [3, "横滨", "よこはま", "Yokohama"],
#         [4, "名古屋", "なごやし", "Nagoya"],
#     ]
# )
#
# print(x)

# from prettytable import PrettyTable
#
# x = PrettyTable()
# x.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
# x.add_row(["Adelaide", 1295, 1158259, 600.5], divider=True)
# x.add_row(["Brisbane", 5905, 1857594, 1146.4], divider=True)
# x.add_row(["Darwin", 112, 120900, 1714.7], divider=True)
# x.add_row(["Hobart", 1357, 205556, 619.5], divider=True)
# x.add_row(["Melbourne", 1566, 3806092, 646.9], divider=True)
# x.add_row(["Perth", 5386, 1554769, 869.4], divider=True)
# x.add_row(["Sydney", 2058, 4336374, 1214.8], divider=True)
# print(x)


# class MyPrettyTable(PrettyTable):
#     # *表示位置参数的结束。之后的每个参数只能由关键字指定。这在PEP 3102中定义
#     def add_row(self, row, *, default=True) -> None:
#         # 调用父类的add_row方法
#         super().add_row(row, divider=default)
#
#
# # 注意，此处调用不是默认的PrettyTable()，而不自定义有MyPrettyTable()
# x = MyPrettyTable()
# x.title = "表7 设置默认分隔钱"
# x.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
# x.add_row(["Adelaide", 1295, 1158259, 600.5])
# x.add_row(["Brisbane", 5905, 1857594, 1146.4])
# x.add_row(["Darwin", 112, 120900, 1714.7])
# x.add_row(["Hobart", 1357, 205556, 619.5])
# x.add_row(["Melbourne", 1566, 3806092, 646.9])
# x.add_row(["Perth", 5386, 1554769, 869.4])
# x.add_row(["Sydney", 2058, 4336374, 1214.8])
# print(x)


# from prettytable import from_csv
#
#
# with open("data.csv") as fp:
#     x = from_csv(fp)
#     x.title = '表 8 天气详情 默认样式'
#     print(x)


# from prettytable import from_csv, SINGLE_BORDER, DOUBLE_BORDER
#
#
# with open("data.csv") as fp:
#     x = from_csv(fp)
#     x.title = '表 8 天气详情 SINGLE_BORDER连续单框线样式'
#     x.set_style(SINGLE_BORDER)
#     print(x)
#
#     x.title = '表 8 天气详情 DOUBLE_BORDER连续双框线样式'
#     x.set_style(DOUBLE_BORDER)
#     print(x)


# from prettytable import from_csv, RANDOM
#
#
# with open("data.csv") as fp:
#     x = from_csv(fp)
#     x.title = '表 8 天气详情 RANDOM随机样式'
#     x.set_style(RANDOM)
#     print(x)

# from prettytable import from_csv
#
# with open("data.csv") as fp:
#     x = from_csv(fp)
#     x.title = '表 9 天气详情 所有列右对齐'
#     x.align = 'r'
#     print(x)
#
#     x.title = '表 9 天气详情 所有列左对齐'
#     x.align = 'l'
#     print(x)
#
#     x.title = '表 9 天气详情 所有列居中对齐'
#     x.align = 'c'
#     print(x)


# from prettytable import from_csv
#
# with open("data.csv") as fp:
#     x = from_csv(fp)
#     x.title = '表 9 天气详情 所有列右对齐'
#     x.align = 'r'
#     print(x)
#
#     x.title = '表 9 天气详情 所有列左对齐'
#     x.align = 'l'
#     print(x)
#
#     x.title = '表 9 天气详情 所有列居中对齐'
#     x.align = 'c'
#     print(x)

# from prettytable import from_csv
#
# with open("data.csv") as fp:
#     x = from_csv(fp)
#     x.title = '表 9 天气详情 每列单独控制对齐方式'
#     x.align["序号"] = 'r'
#     x.align["城市"] = 'l'
#     x.align["日期"] = 'c'
#     x.align["最低气温"] = 'r'
#     x.align["最高气温"] = 'r'
#     print(x)

# from prettytable import from_csv
#
# with open("sort.csv") as fp:
#     x = from_csv(fp)
#     x.title = '表 10 天气详情 按序号升序排序'
#     x.sortby = "序号"
#     print(x)
#
# with open("sort.csv") as fp:
#     x = from_csv(fp)
#     x.title = '表 10 天气详情 按序号降序排序'
#     x.sortby = "序号"
#     x.reversesort = True
#
#     print(x)
#     print(x)

from prettytable import PrettyTable

x = PrettyTable()
x.title = '表 10 天气详情 默认排序'
x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
x.add_rows(
    [
        [1, '北京', '2023/4/30', 11, 25],
        [2, '上海', '2023/4/30', 15, 24],
        [3, '深圳', '2023/4/30', 20, 26],
        [4, '哈尔滨', '2023/4/30', 1, 9],
        [5, '呼和浩特', '2023/4/30', 7, 21],
        [6, '北京', '2023/5/1', 16, 27],
        [7, '上海', '2023/5/1', 17, 29],
        [8, '深圳', '2023/5/1', 29, 29],
        [9, '哈尔滨', '2023/5/1', 9, 19],
        [10, '呼和浩特', '2023/5/1', 9, 25]
    ]
)
# x.sortby = '序号'
# print(x)


# x.title = '表 10 天气详情 按最低气温 升序排序'
# x.sortby = '最低气温'
# print(x)

# x.title = '表 10 天气详情 按最低气温 降序排序'
# x.sortby = '最低气温'
# x.reversesort = True
# print(x)

from prettytable import PrettyTable

# rows = [
#     [1, '北京', '2023/4/30', 11, 25],
#     [2, '上海', '2023/4/30', 15, 24],
#     [3, '深圳', '2023/4/30', 20, 26],
#     [4, '哈尔滨', '2023/4/30', 1, 9],
#     [5, '呼和浩特', '2023/4/30', 7, 21],
#     [6, '北京', '2023/5/1', 16, 27],
#     [7, '上海', '2023/5/1', 17, 29],
#     [8, '深圳', '2023/5/1', 20, 29],
#     [9, '哈尔滨', '2023/5/1', 9, 19],
#     [10, '呼和浩特', '2023/5/1', 9, 25]
# ]
# 对rows进行排序,先按照第4列排序，再按照第5列升序排序
# rows.sort(key=lambda r: (r[3], r[4]))

# 对rows进行排序,先按照第4列排序，再按照第5列降序排序
# rows.sort(key=lambda r: (r[3], -r[4]))
#
#
# x = PrettyTable()
# print('先按最低气温升序，再按最高气温降序排序')
# x.title = '表 10 天气详情 多列排序'
# x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
# x.add_rows(rows)
# print(x)


# from prettytable import PrettyTable
#
# rows = [
#     [1, '北京', '2023/4/30', 11, 25],
#     [2, '上海', '2023/4/30', 15, 24],
#     [3, '深圳', '2023/4/30', 20, 26],
#     [4, '哈尔滨', '2023/4/30', 1, 9],
#     [5, '呼和浩特', '2023/4/30', 7, 21],
# ]
#
# x = PrettyTable()
# x.title = '表 11 天气详情 输出格式化字符串'
# x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
# x.add_rows(rows)
# print(x)
# print(type(x))
# out_str = x.get_string()
# print(out_str)
# print(type(out_str))

# with open('default.txt', mode='w') as f:
#     f.write(f'{out_str}\n')

# with open('out.html', mode='w') as f:
#     out_str = x.get_html_string()
#     f.write(f'{out_str}\n')
#
# with open('out.json', mode='w') as f:
#     # 此处需要指定ensure_ascii=False，否则中文乱码
#     out_str = x.get_json_string(ensure_ascii=False)
#     f.write(f'{out_str}\n')
#
# with open('out.csv', mode='w') as f:
#     out_str = x.get_csv_string()
#     f.write(f'{out_str}\n')


# from prettytable import PrettyTable, ALL, FRAME, HEADER, NONE
#
# rows = [
#     [1, '北京', '2023/4/30', 11, 25],
#     [2, '上海', '2023/4/30', 15, 24],
#     [3, '深圳', '2023/4/30', 20, 26],
#     [4, '哈尔滨', '2023/4/30', 1, 9],
#     [5, '呼和浩特', '2023/4/30', 7, 21],
# ]

# x = PrettyTable()
# x.title = '表 12 天气详情 默认样式'
# x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
# x.add_rows(rows)
# print(x)
# x.title = '表 12 天气详情 高级样式设置'
# # 设置列数据左侧的空格数
# x.left_padding_width = 4
# # 设置列数据右侧的空格数
# x.right_padding_width = 4
# # 设置绘制垂直线的单个字符串
# x.vertical_char = '$'
# # 设置绘制水平线的单个字符串
# x.horizontal_char = '='
# # 设置整数数据打印方式的字符串, 整数设置宽为3，不够3位左侧补0
# x.int_format = '03'
# # 控制行后水平方向的打印
# # ALL全部打印
# # FRAME打印头部行、字段行、最后行下面的水平线
# # HEADER 只打印头部
# # NONE 不打印
# x.hrules = ALL
# print(x)


from prettytable.colortable import ColorTable, Themes, Theme

rows = [
    [1, '北京', '2023/4/30', 11, 25],
    [2, '上海', '2023/4/30', 15, 24],
    [3, '深圳', '2023/4/30', 20, 26],
    [4, '哈尔滨', '2023/4/30', 1, 9],
    [5, '呼和浩特', '2023/4/30', 7, 21],
]

# 使用海洋主题
x = ColorTable(theme=Themes.OCEAN)
print('\n表 13 天气详情 使用系统自带海洋主题 改变表格颜色')
x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
x.add_rows(rows)
print(x)

# 自定义主题
MYTHEME = Theme(
    default_color="31",  # 默认使用红色前景色
    vertical_color="44",  # 垂直线使用蓝色背景色
    horizontal_color="33",  # 水平线使用黄色前景色
    junction_color="97",  # 连接线使用亮白色前景色
)

x = ColorTable(theme=MYTHEME)
print('\n表 13 天气详情 使用自定义主题 改变表格颜色')
x.field_names = ["序号", "城市", "日期", "最低气温", "最高气温"]
x.add_rows(rows)
print(x)

y = x[1:3]
print('\n获取第2和第3行子表')
print(y)
print('\n\n获取第1和第3行子表')
z = x[0:4:2]
print(z)

