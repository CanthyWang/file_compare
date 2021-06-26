"""
BMI calculation
^^^^^^^^^^^^^^^

Simple application for calculating `Body Mass Index <https://en.wikipedia.org/wiki/Body_mass_index>`_

:demo_host:`Demo </bmi-test>`, `Source code <https://github.com/CanthyWang/file_compare/edit/main/PyWebIO/demos/bmi.py>`_
"""
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio import session
from pywebio.session import info as session_info
import xlwt
import pandas as pd


def file_to_xls(filename, xlsname):
    """将文件格式转换成xls"""
    f = open(filename, encoding='utf-8')
    xls = xlwt.Workbook()
    sheet = xls.add_sheet('sheet1', cell_overwrite_ok=True)

    # 添加列名
    sheet.write(0, 0, 'column1')

    x = 1
    while True:
        # 按行循环，读取文本文件
        line = f.readline()
        item = line.split('\n')[0]
        if not line:
            break
        sheet.write(x, 0, item)
        x += 1
    f.close()
    xls.save(xlsname)


def file_compare(file1,file2):
    """文件筛除重复项"""
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    index = df2['column1'].isin(df1['column1'])
    duplicate = df2[index]
    df2_drop = df2[~index]
    df1_drop = df1[~df1['column1'].isin(duplicate['column1'])]

    return duplicate, df1_drop, df2_drop


def extract(file):
    """提取文件内容"""
    content = ''
    for item in file['column1']:
        content += str(item) + '\n'
    
    return str.encode(content)


def main():

    """FILE Calculation
    Compare files, Delete duplicate entries, Export them.
    文件对比，筛除重复项并导出
    """

    put_markdown("""## 筛除文件重复值

    点击【Browse】上传需要处理的文件

    """, strip_indent=4)

    info1 = file_upload("上传待处理文件一", accept='')
    info2 = file_upload("上传待处理文件二", accept='')
    
    file_to_xls(info1['filename'], info1['filename'] + '.xls')
    file_to_xls(info2['filename'], info2['filename'] + '.xls')

    duplicate_file, df1_drop, df2_drop = file_compare(info1['filename'] + '.xls', info2['filename'] + '.xls')

    duplicate = extract(duplicate_file)
    df1 = extract(df1_drop)
    df2 = extract(df2_drop)
   

    put_markdown("""## 文件下载
        """)

    put_markdown("""
    文本文档
        """, strip_indent=4)

    put_file('重复值.txt', duplicate, '重复值.txt')
    put_file(info1['filename'] + '_剔除重复值.txt', df1, info1['filename'] + '_剔除重复值.txt')
    put_file(info2['filename'] + '_剔除重复值.txt', df2, info2['filename'] + '_剔除重复值.txt')

    put_markdown("""
    XLS工作表
        """, strip_indent=2)
    put_file('重复值.xls', duplicate, '重复值.xls')
    put_file(info1['filename'] + '_剔除重复值.xls', df1, info1['filename'] + '_剔除重复值.xls')
    put_file(info2['filename'] + '_剔除重复值.xls', df2, info2['filename'] + '_剔除重复值.xls')

    # put_markdown("""
    # CSV工作表
    #     """, strip_indent=2)
    # put_file('重复值.csv', duplicate, '重复值.csv')
    # put_file(info1['filename'] + '_剔除重复值.csv', df1, info1['filename'] + '_剔除重复值.csv')
    # put_file(info2['filename'] + '_剔除重复值.csv', df2, info2['filename'] + '_剔除重复值.csv')

    put_markdown("""## 数据校验""")
    put_table([
        ['文件名', '文件大小'],
        [info1['filename'], pd.read_excel(info1['filename'] + '.xls').shape[0]],
        [info2['filename'], pd.read_excel(info2['filename'] + '.xls').shape[0]],
        ['重复值', duplicate_file.shape[0]],
        [info1['filename'] + '_剔除重复值', df1_drop.shape[0]],
        [info2['filename'] + '_剔除重复值', df2_drop.shape[0]]
    ])

    session.hold()
   

 
if __name__ == '__main__':
    start_server(main, debug=True, port=8080, cdn=False)
