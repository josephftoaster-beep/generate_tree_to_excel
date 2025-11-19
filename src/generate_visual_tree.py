#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import re

# ----------------------------------------------------------------------
# 1. 定数と初期設定
# ----------------------------------------------------------------------

# 処理対象のフォルダパス (実行環境に合わせて変更)
PROJECT_PATH = r'C:\Users\robek\OneDrive\デスクトップ\windows編'
# 出力するExcelファイル名
OUTPUT_FILE = 'Project_Document_Breakdown_Recursive.xlsx'

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
    """
    再帰的にフォルダ構造をスキャンし、ツリー表示用の文字列をリストに追加するヘルパー関数。

    Args:
        current_path (str): 現在処理中のディレクトリのフルパス。
        indent_prefix (str): 現在の階層に適用すべきインデント（縦線）の文字列。
        current_tree_list (list): 結果を格納するツリー文字列のリスト。
    """
    # フォルダとファイルをリストアップし、ソートする（日本語ファイル名も考慮し、デフォルトのロケールソートを使用）
    try:
        items = sorted(os.listdir(current_path))
    except FileNotFoundError:
        return

    # フォルダとファイルを分離
    dirs = [item for item in items if os.path.isdir(os.path.join(current_path, item))]
    files = [item for item in items if os.path.isfile(os.path.join(current_path, item))]

    all_children = dirs + files

    for i, item in enumerate(all_children):
        is_dir = item in dirs
        is_last = (i == len(all_children) - 1)

        # 接続文字の決定（├── または └──）
        prefix = CORNER_ITEM if is_last else PIPE_ITEM

        # 次の階層へのインデント縦線の決定
        # 最後の要素なら縦線（│）は不要、それ以外なら必要
        next_indent = SPACE if is_last else PIPE_SPACE

        full_path = os.path.join(current_path, item)

        if is_dir:
            # フォルダ名の行を追加
            current_tree_list.append(
                f'{indent_prefix}{prefix}{FOLDER_ICON}{item}{os.sep}'
            )

            # 再帰呼び出し：次の階層のインデントを渡し、関数自身を呼び出す
            _recursive_scan_dir(
                full_path, 
                indent_prefix + next_indent, 
                current_tree_list
            )
        else:
            # ファイル名の行を追加
            current_tree_list.append(
                f'{indent_prefix}{prefix}{FILE_ICON}{item}'
            )

# ----------------------------------------------------------------------
# 3. メインのデータ生成関数
# ----------------------------------------------------------------------

def generate_visual_tree_recursive(startpath):
    """
    指定されたパスからフォルダ構造をスキャンし、Excelシート用の辞書を生成する。
    """
    if not os.path.isdir(startpath):
        return {'エラー': [f'指定されたフォルダが見つからないか、フォルダではありません。スキップします。']}

    folder_data = {}
    root_dir_name = os.path.basename(startpath) + os.sep

    # 1. ルートシート（全体概要）の作成
    root_lines = [root_dir_name]
    _recursive_scan_dir(startpath, '', root_lines)
    folder_data[root_dir_name] = root_lines

    # 2. トップレベルフォルダごとのシートの作成
    # ルート直下の要素を取得（トップレベルのシートキー）
    try:
        root_items = sorted(os.listdir(startpath))
    except FileNotFoundError:
         return {'エラー': [f'ルートフォルダの読み取り中にエラーが発生しました。']}

    top_level_dirs = [item for item in root_items if os.path.isdir(os.path.join(startpath, item))]

    for dir_name in top_level_dirs:
        sheet_key = dir_name + os.sep
        dir_lines = [sheet_key] # シートの見出しとしてフォルダ名を追加

        # トップレベルフォルダの中身を再帰的にスキャン
        # ルートフォルダ直下なので、初期インデントは ''
        _recursive_scan_dir(
            os.path.join(startpath, dir_name), 
            '', 
            dir_lines
        )
        folder_data[sheet_key] = dir_lines

    return folder_data

# ----------------------------------------------------------------------
# 4. Excel出力関数 (シート名処理を改良)
# ----------------------------------------------------------------------

def write_trees_to_excel(folder_data, output_filepath):
    # (中略：前回のコードとほぼ同じ。Pandasの処理)
    print(f'\n📊 Excelファイルへの書き出しを開始します: {output_filepath}')

    try:
        with pd.ExcelWriter(output_filepath, engine='xlsxwriter') as writer:

            for folder_name, tree_lines in folder_data.items():

                if folder_name == 'エラー':
                    print(f"  警告：データにエラー情報が含まれていました。スキップします: {tree_lines[0]}")
                    continue

                df = pd.DataFrame(tree_lines, columns=['Path']) 

                # ★★★ シート名の改良: Excelの禁止文字を置換 ★★★
                # Excelの禁止文字: \ / ? * [ ] :
                sheet_name = re.sub(r'[\\/\*\?:\[\]]+', '_', folder_name)
                sheet_name = sheet_name.replace('<', '_').replace('>', '_') # 追加
                sheet_name = sheet_name.strip('_')

                if not sheet_name: 
                    sheet_name = 'ルート'

                sheet_name = sheet_name[:31] # Excelのシート名最大長

                # ★★★ 最終チェック: 重複を避けるために一意な名前を生成するロジックも追加すべき（今回は割愛）

                df.to_excel(writer, sheet_name=sheet_name, index=False)

                try:
                    # 列幅の自動設定
                    worksheet = writer.sheets[sheet_name]
                    worksheet.set_column(0, 0, 50) 
                except Exception as e:
                    # 列幅設定でエラーが出ても無視する（xlsxwriterの仕様変更などに対応）
                    pass

        print(f"✅ Excelファイルが正常に作成されました。")

    except Exception as e:
        print(f"❌ Excelファイル書き出し中に致命的なエラーが発生しました: {e}")

# ----------------------------------------------------------------------
# 5. メイン処理の実行
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("--- 建築DXツール：フォルダ構造解析開始 (再帰バージョン) ---")

    # データを生成 (再帰関数を使用)
    tree_data = generate_visual_tree_recursive(PROJECT_PATH)

    # エラーチェック
    if 'エラー' in tree_data:
        print(f"🚨 処理中断：{tree_data['エラー'][0]}")
    else:
        # Excelに出力
        write_trees_to_excel(tree_data, OUTPUT_FILE)

    print("--- 処理完了 ---")

