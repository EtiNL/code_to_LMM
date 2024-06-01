#!/home/etin_l/.pyenv/versions/code_to_LMM/bin/python

import os
import sys

def aggregate_code_from_folder(folder_path):
    aggregated_code = ""

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.rs') or file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                aggregated_code += f"// {file_path}\n{file_content}\n\n"
    
    return aggregated_code

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: aggregate_code.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    aggregated_code = aggregate_code_from_folder(folder_path)

    try:
        import pyperclip
        pyperclip.copy(aggregated_code)
        print("Aggregated code copied to clipboard!")
    except ImportError:
        print("pyperclip module not installed. Install it to enable clipboard functionality.")

