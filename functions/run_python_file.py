import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python file in a specified location relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "The optional command-line arguments passed to the script for Python file execution.",
                },
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir == False:
            return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if os.path.isfile(target_dir) == False:
            return(f'Error: "{file_path}" does not exist or is not a regular file')
        if file_path.endswith(".py") == False:
            return(f'Error: "{file_path}" is not a Python file')

        command = ["python", target_dir]
        if args:
            command.extend(args)
        process_output = subprocess.run(command, cwd = working_dir_abs, capture_output = True, text = True, timeout = 30)
        output_string = ""
        if process_output.returncode != 0:
            output_string = output_string + f"Process exited with code {process_output.returncode}\n"
        if not process_output.stdout and not process_output.stderr:
            output_string = output_string + "No output produced"
        #if not process_output.stdout:
            #output_string = output_string + f"STDERR: {process_output.stderr}"
        else:
            output_string = output_string + f"STDOUT: {process_output.stdout}\nSTDERR: {process_output.stderr}"
        return output_string

    except (ValueError, TypeError, OSError) as e:
        return (f"Error: executing Python file: {e}")
