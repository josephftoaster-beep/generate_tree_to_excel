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
                df.to_excel(writer, sheet_name = sheet_name, index= False)
                try:
                    worksheet = writer.sheets[sheet_name]
                    worksheet.set_column(0, 0, 100)
                except Exception:
                    pass
        print(f'✅Excelファイルが正常に作成されました：{output_filepath}')

    except Exception as e:
        print (f'✖Excelファイル書き出し中に致命的なエラーが発生しました：{e}')