import pandas as pd
import re
from datetime import datetime

# ★修正1：必要な定数をここで定義する★
DATE = datetime.today()
today = DATE.strftime('%Y%m%d')

def write_trees_to_excel(folder_data, output_filepath=f'Project_Tree_Report_{today}.xlsx'):
    """
    フォルダ名:ツリーリストの辞書を受け取り、各フォルダ名をシート名としてExcelに書き出す関数。
    
    Args:
        folder_data (dict): generate_visual_tree_recursive 関数から返された辞書。
        output_filepath (str): 出力するExcelファイルのパスと名前。
    """
    print(f'📊 Excelファイルへの書き出しを開始します: {output_filepath}')
    
    # 各フォルダ名ごとにシートを作成し、そのフォルダ配下すべてのフォルダ・ファイルのツリー構成(ツリーリスト)を書き込む
    try:
        #ファイルパスとファイル名を指定とExcelファイルへの書き込み方法(xlsxwriter)を指定する。
        # writerオブジェクトが初期化され、ファイルが開かれる。
        with pd.ExcelWriter(output_filepath, engine= 'xlsxwriter') as writer:
            #フォルダ名(キー)とツリーリスト(値)を一つずつ取り出す。
            for folder_name, tree_lines in folder_data.items():
                #シート名に設定できない文字・記号は’_’に置き換える。
                sheet_name = re.sub(r'[\\/\*\?:\[\]]+', '_', folder_name)
                #シート名の先頭あるいは最後に’_’がある場合はそれを取り除く。
                #シート名に’<’または’>’がある場合は’_’に置き換える。
                sheet_name = sheet_name.replace('<','_').replace('>','_').strip('_')
                #シート名が空の場合は’ルート’とし、それ以外はシート名の文字数は31文字以内とし、sheet_nameに格納する。
                sheet_name = 'ルート' if not sheet_name else sheet_name[:31]

                #列名：'Path'としてツリーリスト(tree_lines)によるデータフレームを作成する。
                df = pd.DataFrame(tree_lines, columns=['Path'])
                #データフレーム(df)をExcelファイルのシート名：sheet_nameに書き込む。
                df.to_excel(writer, sheet_name = sheet_name, index= False)
                try:
                    #指定のシート(sheet_name)を開き、worksheetに格納する。
                    worksheet = writer.sheets[sheet_name]
                    #シートのA列(0列目)の列幅を100に設定する。
                    worksheet.set_column(0, 0, 100)
                #列幅の設定に失敗しても、ファイル作成自体には影響させないため、エラーを無視して処理を続行する。
                except Exception:
                    pass
        print(f'✅Excelファイルが正常に作成されました：{output_filepath}')
    #例外(ファイルが開けない、権限がないなど)が生じた場合はエラーメッセージを返し、処理を中断する。
    except Exception as e:
        print (f'✖Excelファイル書き出し中に致命的なエラーが発生しました：{e}')