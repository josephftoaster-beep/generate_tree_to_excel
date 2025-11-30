import os

SPACE = '    '
PIPE_SPACE = '│' + SPACE
PIPE_ITEM = '├── '
CORNER_ITEM = '└── '
FILE_ICON = '📄'
FOLDER_ICON = '📂'

from tree_scanner import _recursive_scan_dir

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

    return folder_dictionary
