import os

SPACE = '    '
PIPE_SPACE = '│' + SPACE
PIPE_ITEM = '├── '
CORNER_ITEM = '└── '
FILE_ICON = '📄'
FOLDER_ICON = '📂'

def _recursive_scan_dir(current_path, indent_prefix, current_tree_list):
    #親フォルダ配下にあるすべてのフォルダ名・ファイル名をリスト化する。(フルパスではない)
    current_dir_file_list = os.listdir(current_path)
    #フォルダとファイルを分離していれる空のリストを用意する。
    dirs = []
    files = []
    
    for source in current_dir_file_list:
        #親フォルダ配下にあるフォルダやファイルのフルパスをfull_pathに格納する。
        full_path = os.path.join(current_path,source)

        # フォルダとファイルを分離する。
        if os.path.isdir(full_path):
            dirs.append(source)
        else:
            files.append(source)
    #ルール(五十音順、昇順など)に従いソートする。
    dirs.sort()
    files.sort()
    #ツリー描画の慣習に従い、フォルダを先、ファイルを後の順序で結合する。
    all_children = dirs + files
    #
    for i, item in enumerate(all_children):
        is_dir = item in dirs
        is_last = (i == len(all_children) -1)
        
        prefix = CORNER_ITEM if is_last else PIPE_ITEM
        next_indent = SPACE if is_last else PIPE_SPACE

        full_path = os.path.join(current_path, item)

        if is_dir:
            current_tree_list.append(
                f'{indent_prefix}{prefix}{FOLDER_ICON}{item}{os.sep}'
                )
            
            _recursive_scan_dir(
                full_path,
                indent_prefix + next_indent,
                current_tree_list
                )
        else:
            current_tree_list.append(f'{indent_prefix}{prefix}{FILE_ICON}{item}')

    return
