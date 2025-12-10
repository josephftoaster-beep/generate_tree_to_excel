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
    
    for i, item in enumerate(all_children):
        #itemがフォルダに該当する場合、Trueを返す。
        #Trueの場合、ICONの判別と、次の階層への再帰呼び出しを行う際にの分岐に利用する。
        is_dir = item in dirs
        #インデックスとリスト内の最後の要素のインデックスが等しければTrueを返す。
        #prefixおよびnext_indentの変数がis_lastによって変わる。
        is_last = (i == len(all_children) -1)
        
        #is_last(TrueまたはFalse)に基づいて、接続文字と次のインデントを決定する。
        #最後の要素(True)の場合、prefixは’└──’(CORNER_ITEM)となり、
        #next_indentは縦線を切断する SPACE が格納される。 
        prefix = CORNER_ITEM if is_last else PIPE_ITEM
        next_indent = SPACE if is_last else PIPE_SPACE
        #再帰呼び出し（サブフォルダへの移動）の引数として利用するため、フルパスを格納する。
        full_path = os.path.join(current_path, item)

        
        if is_dir:
            #is_dirがTrueのとき、current_tree_listにツリー描画(フォルダ)を追加する。
            current_tree_list.append(
                f'{indent_prefix}{prefix}{FOLDER_ICON}{item}{os.sep}'
                )
            #再帰呼び出しを行い、階層を一つ深く潜る。
            #※次のindent_prefix(next_indent)を引数に渡すことで、再帰的なインデントを実現する。
            _recursive_scan_dir(
                full_path,
                indent_prefix + next_indent,
                current_tree_list
                )
        else:
            #is_dirがFalseの場合、current_tree_listにツリー描画(ファイル)を追加する。
            current_tree_list.append(f'{indent_prefix}{prefix}{FILE_ICON}{item}')
    #すべての要素の処理と再帰呼び出しが完了したため、
    #呼び出し元(一つ上の階層)に制御を戻す。(再帰処理の巻き戻し)
    return
