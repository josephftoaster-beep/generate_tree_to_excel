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
