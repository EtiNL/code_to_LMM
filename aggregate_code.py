#!/home/etienne/code/Python/code_to_LMM/code_to_LLM/bin/python


import os
import sys

def aggregate_code_from_folder(
    folder_path: str,
    list_filename: str = "code_to_aggregate.txt",
    allowed_exts=None,
    exclude_dirs=("target",),
) -> str:
    """
    Aggregate source files into a single string. If `code_to_aggregate.txt`
    exists in `folder_path`, only the files/folders listed there are included.

    The list file supports:
      - Exact file paths relative to `folder_path`, e.g. `src/main.rs`
      - Folder paths to include everything under them with allowed extensions, e.g. `src`
      - Lines beginning with `//` are ignored
      - Inline comments after `//` are ignored, e.g. `src  // include all`

    Allowed extensions default to: .json, .rs, .py, .cu, .md, .toml, plus `Dockerfile` (case-insensitive).
    Any directory path containing a segment named in `exclude_dirs` (default: 'target') is skipped.
    """
    if allowed_exts is None:
        allowed_exts = {".json", ".rs", ".py", ".cu", ".md", ".toml"}
    # normalize to lower-case extensions for case-insensitive matching
    allowed_exts = {ext.lower() for ext in allowed_exts}

    root_abs = os.path.abspath(folder_path)

    def is_excluded_dir(path: str) -> bool:
        parts = os.path.abspath(path).split(os.sep)
        return any(seg in exclude_dirs for seg in parts if seg)

    def is_allowed_file(path: str) -> bool:
        base = os.path.basename(path)
        if base.lower() == "dockerfile":
            return True
        _, ext = os.path.splitext(base)
        return ext.lower() in allowed_exts

    def add_files_from_dir(dir_path: str, out_list: list, seen: set):
        for current_root, dirs, files in os.walk(dir_path):
            # prune and sort dirs to ensure deterministic traversal
            dirs[:] = sorted([d for d in dirs if d not in exclude_dirs])
            if is_excluded_dir(current_root):
                continue
            for fname in sorted(files):
                fpath = os.path.normpath(os.path.join(current_root, fname))
                if is_allowed_file(fpath) and fpath not in seen:
                    seen.add(fpath)
                    out_list.append(fpath)

    # Build the (ordered) list of files to aggregate
    files_ordered = []
    seen = set()
    list_path = os.path.join(folder_path, list_filename)

    if os.path.isfile(list_path):
        with open(list_path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("//"):
                    continue
                # strip inline comments
                if "//" in line:
                    line = line.split("//", 1)[0].strip()
                if not line:
                    continue

                # handle trailing slash for dirs nicely
                cand = line[:-1] if line.endswith(os.sep) or line.endswith("/") else line
                cand_path = os.path.normpath(os.path.join(folder_path, cand))

                # stay inside the root
                try:
                    common = os.path.commonpath([os.path.abspath(cand_path), root_abs])
                except ValueError:
                    # different drives (Windows) -> skip
                    continue
                if common != root_abs:
                    continue

                if os.path.isdir(cand_path):
                    if not is_excluded_dir(cand_path):
                        add_files_from_dir(cand_path, files_ordered, seen)
                elif os.path.isfile(cand_path):
                    parent = os.path.dirname(cand_path)
                    if not is_excluded_dir(parent) and is_allowed_file(cand_path) and cand_path not in seen:
                        seen.add(cand_path)
                        files_ordered.append(cand_path)
                else:
                    # silently ignore missing paths
                    pass
    else:
        # Fallback: scan entire tree (deterministic order)
        add_files_from_dir(folder_path, files_ordered, seen)

    aggregated_code = ""
    for file_path in files_ordered:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                file_content = f.read()
        rel = os.path.relpath(file_path, start=folder_path)
        aggregated_code += f"// {rel}\n{file_content}\n\n"

    return aggregated_code


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: aggregate_code <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    aggregated_code = aggregate_code_from_folder(folder_path)

    try:
        import pyperclip
        pyperclip.copy(aggregated_code)
        print("Aggregated code copied to clipboard!")
    except ImportError:
        print("pyperclip module not installed. Install it to enable clipboard functionality.")

