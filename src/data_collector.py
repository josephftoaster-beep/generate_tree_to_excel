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
        #startpath配下すべての要素(フォルダ名・ファイル名)をソートし、itemsにリストを格納する。
        items = sorted(os.listdir(startpath))
        #例外(startpathが存在しない、アクセス権がないなど)が発生した場合、エラーを出力し、プログラムを中断する。
    except Exception as e:
        return {'エラー': [f'ルートフォルダの読み込み中にエラーが発生しました: {e}']}
    #最終的な出力データ(フォルダ名：ツリーリスト)を格納するための空の辞書を用意する。
    folder_dictionary = {}
    
    #フォルダのフルパス(startpath)からフォルダ名だけ取り出し、フォルダ名の後に’/’を付与して、root_dir_nameに格納する。
    root_dir_name = os.path.basename(startpath) + os.sep
    #ルートフォルダ自身の名前をリストの先頭に格納する。
    root_lines = [root_dir_name]
    #root_linesにstartpath配下の全階層のツリー構造を追記する。
    _recursive_scan_dir(startpath,
                        '',
                        root_lines)
    #出力されたツリーリスト(root_lines)をキー：root_dir_name,値：root_linesとして辞書に格納する。
    folder_dictionary[root_dir_name] = root_lines

    #itemsからフォルダのみを抽出し、Excelのシートをして作成する「トップレベルのサブフォルダ名」のみをリストとして格納する。
    top_level_dir = [item for item in items if os.path.isdir(os.path.join(startpath, item))]
    #サブフォルダ名ごとのシートを作成し、サブフォルダ配下のツリー描画をシートに表示する。
    #ルートシート以外の、各トップレベルフォルダごとのサブシートを作成する。
    for dir_name in top_level_dir:
        #サブフォルダ名に’/’を付加し、Excelシート名をsheet_keyに格納する。
        sheet_key = dir_name + os.sep
        #sheet_key(サブフォルダ名)をツリーリスト(dir_lines)の先頭に格納する。
        dir_lines = [sheet_key]
        #サブフォルダのフルパスを作成し、dir_pathに格納する。
        dir_path = os.path.join(startpath, dir_name)
        #dir_linesにサブフォルダ配下のすべてのツリー構造を追記する。
        _recursive_scan_dir(dir_path, 
                                '', 
                                dir_lines)
        #ツリーリスト(dir_lines)を値、sheet_keyをキーとして、辞書に格納する。
        folder_dictionary[sheet_key] = dir_lines
    #ルートフォルダおよびサブフォルダのツリーリストが格納された辞書を返す。
    return folder_dictionary
