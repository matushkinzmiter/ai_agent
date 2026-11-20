import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir == False:
            return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        if os.path.isdir(target_dir) == False:
            return(f'Error: "{directory}" is not a directory')
        if valid_target_dir == True:
            files_list = os.listdir(target_dir)
            files_info = ""
            for file in files_list:
                file_path = os.path.join(target_dir, file)
                files_info = files_info + f"- {file}: file_size={os.path.getsize(file_path)} byes, is_dir={os.path.isdir(file_path)}\n"
            files_info = f"Result for {directory} directory:\n{files_info[:-1]}"
            return(files_info)
    except ValueError:
        print("Error: Invalid path input.")
    except TypeError:
        print("Error: Invalid path input.")
    except OSError:
        print("Error: Invalid path input.")
