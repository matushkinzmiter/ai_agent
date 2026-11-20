import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the content of the text file as a string.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file with the content to get, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir == False:
            return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if os.path.isfile(target_dir) == False:
            return(f'Error: File not found or is not a regular file: "{file_path}"')

        with open(target_dir, "r", encoding="utf-8") as file:
            content = file.read(MAX_CHARS)
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content

    except ValueError:
        print("Error: Invalid path input.")
    except TypeError:
        print("Error: Invalid path input.")
    except OSError:
        print("Error: Invalid path input.")
