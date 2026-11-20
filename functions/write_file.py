import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Adding the text content to existing text file in a specified directory relative to the working directory. If file does not exist in a specified directory, it is created there.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to update, relative to the working directory (default is the working directory itself). If file is missing in a specified location, it is created.",
                },
                "content": {
                    "type": "string",
                    "description": "String which is to be added to the specified file.",
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir == False:
            print(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target_dir) == True:
            print(f'Error: Cannot write to "{file_path}" as it is a directory')

        new_target_dir = os.path.dirname(target_dir)
        os.makedirs(new_target_dir, exist_ok=True)

        with open(target_dir, "w", encoding="utf-8") as file:
             file.write(content)
        return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')

    except ValueError:
        return("Error: Invalid path input.")
    except TypeError:
        return("Error: Invalid path input.")
    except OSError:
        return("Error: Invalid path input.")
