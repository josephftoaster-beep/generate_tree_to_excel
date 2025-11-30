import sys
import pandas as pd
import os
import re
from datetime import datetime



# project_root = os.path.abspath(os.path.join(os.getcwd(), '..'))
# sys.path.append(project_root)
# src_path = os.path.join(project_root, 'src')
# sys.path.append(src_path)

from data_collector import generate_visual_tree_recursive
from excel_writer import write_trees_to_excel

DATE = datetime.today()
today = DATE.strftime('%Y%m%d')

PROJECT_PATH = r'C:\Users\robek\OneDrive\デスクトップ\windows編' 
OUTPUT_FILE = f'Project_Document_Breakdown_Recursive_{today}.xlsx'

# ツリー描画用の文字
# SPACE = '    '
# PIPE_SPACE = '│' + SPACE
# PIPE_ITEM = '├── '
# CORNER_ITEM = '└── '
# FILE_ICON = '📄'
# FOLDER_ICON = '📂'

if __name__ == '__main__':
    tree_data = generate_visual_tree_recursive(PROJECT_PATH)

    if "エラー" in tree_data:
        print(f'処理中断：{tree_data["エラー"][0]}')
    else:
        write_trees_to_excel(tree_data, OUTPUT_FILE)

    print('--- 処理完了 ---')
