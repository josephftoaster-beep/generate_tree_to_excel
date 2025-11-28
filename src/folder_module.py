import pandas as pd
import os
import re
from datetime import datetime

# ----------------------------------------------------------------------
# 1. 定数と初期設定
# ----------------------------------------------------------------------

# 処理対象のフォルダパス (実行環境に合わせて変更)
PROJECT_PATH = r'C:\Users\robek\OneDrive\デスクトップ\windows編'
# 出力するExcelファイル名
OUTPUT_FILE = 'Project_Document_Breakdown_Recursive.xlsx'

DATE = datetime.today()
today = DATE.strftime('%Y%m%d')

# ツリー描画用の文字
SPACE = '    '
PIPE_SPACE = '│' + SPACE
PIPE_ITEM = '├── '
CORNER_ITEM = '└── '
FILE_ICON = '📄'
FOLDER_ICON = '📂'

# ----------------------------------------------------------------------
# 2. 再帰スキャン関数 (ロジックの核心)
# ----------------------------------------------------------------------

def _recursive_scan_dir(current_path, indent_prefix, current_tree_list):
    current_dir_file_list = os.listdir(current_path)

    dirs = []
    files = []

    for source in current_dir_file_list:
        full_path = os.path.join(current_path,source)

          # フォルダとファイルを分離
        if os.path.isdir(full_path):
            dirs.append(source)
        else:
            files.append(source)

    dirs.sort()
    files.sort()
    all_children = dirs + files

    for i, item in enumerate(all_children):
        is_dir = item in dirs
        is_last = (i == len(all_children) -1)
        
        prefix = CORNER_ITEM if is_last else PIPE_ITEM
        next_indent = SPACE if is_last else PIPE_SPACE


# ----------------------------------------------------------------------
# 3. メインのデータ生成関数
# ----------------------------------------------------------------------

def generate_visual_tree_recursive(startpath):
    try:
        items = sorted(os.listdir(startpath))
    except Exception as e:
        return {'エラー': [f'ルートフォルダの読み込み中にエラーが発生しました: {e}']}
    
    folder_dictionary = {}

    root_dir_name = os.path.basename(startpath) + os.sep
    root_lines = [root_dir_name]
    _recursive_scan_dir(startpath,
                        '',
                        root_lines)
    folder_dictionary[root_dir_name] = root_lines


    top_level_dir = [item for item in items if os.path.isdir(os.path.join(startpath, item))]

    for dir_name in top_level_dir:
        sheet_key = dir_name + os.sep
        dir_lines = [sheet_key]
        dir_path = os.path.join(startpath, dir_name)
        _recursive_scan_dir(dir_path, 
                                '', 
                                dir_lines)
        folder_dictionary[sheet_key] = dir_lines


# ----------------------------------------------------------------------
# 4. Excelファイル作成
# ----------------------------------------------------------------------


def write_trees_to_excel(folder_data, output_filepath=f'Project_Tree_Report_{today}.xlsx'):
    """
    フォルダ名:ツリーリストの辞書を受け取り、各フォルダ名をシート名としてExcelに書き出す関数。
    
    Args:
        folder_data (dict): generate_visual_tree 関数から返された辞書。
        output_filepath (str): 出力するExcelファイルのパスと名前。
    """
    print(f'📊 Excelファイルへの書き出しを開始します: {output_filepath}')
    
    # 各フォルダ名ごとにシートを作成し、ツリーリストを書き込む
    try:
        with pd.ExcelWriter(output_filepath, engine= 'xlsxwriter') as writer:

            for folder_name, tree_lines in folder_data.items():

                sheet_name = re.sub(r'[\\/\*\?:\[\]]+', '_', folder_name)
                sheet_name = sheet_name.replace('<','_').replace('>','_').strip('_')
                sheet_name = 'ルート' if not sheet_name else sheet_name[:31]

                df = pd.DataFrame(tree_lines, columns=['Path'])
                df.to_excel(writer, sheet_name = folder_name, index= False)
                try:
                    worksheet = writer.sheets[folder_name]
                    worksheet.set_column(0, 0, 100)
                except Exception:
                    pass
        print(f'✅Excelファイルが正常に作成されました：{output_filepath}')

    except Exception as e:
        print (f'✖Excelファイル書き出し中に致命的なエラーが発生しました：{e}')