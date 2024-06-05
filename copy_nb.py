#!/home/etin_l/.pyenv/versions/code_to_LMM/bin/python

import json
import argparse

def parse_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as file:
        notebook_content = json.load(file)
        
    return notebook_content

def format_cell(cell):
    cell_type = cell['cell_type']
    if cell_type == 'markdown':
        content = ''.join(cell['source'])
        return f"### Markdown Cell:\n{content}\n"
    elif cell_type == 'code':
        content = ''.join(cell['source'])
        output = []
        for out in cell.get('outputs', []):
            if 'text' in out:
                output.append(''.join(out['text']))
            elif 'data' in out and 'text/plain' in out['data']:
                output.append(''.join(out['data']['text/plain']))
        output = '\n'.join(output)
        return f"### Code Cell:\n```python\n{content}\n```\n### Output:\n{output}\n"
    return ""

def format_notebook(notebook_content):
    cells = notebook_content['cells']
    formatted_cells = [format_cell(cell) for cell in cells]
    return '\n'.join(formatted_cells)

def main(notebook_path):
    notebook_content = parse_notebook(notebook_path)
    formatted_content = format_notebook(notebook_content)
    return formatted_content

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse and format a Jupyter Notebook (.ipynb) file.")
    parser.add_argument('notebook_path', type=str, help="Path to the Jupyter Notebook file.")
    args = parser.parse_args()
    nb_copy = main(args.notebook_path)
    try:
        import pyperclip
        pyperclip.copy(nb_copy)
        print("Notebook copied to clipboard!")
    except ImportError:
        print("pyperclip module not installed. Install it to enable clipboard functionality.")
