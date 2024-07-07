# Description 
This script copy every .rs or .py (except code in ./target) for you to paste it to a LLM.
it aggregates the code in form of:

// file1.rs or file1.py
Code
Code Code 

// file2.rs or file2.py
Code
Code Code 

# Make it executable from anywhere

1. **Make the Script Executable**:
    ```sh
    chmod +x /path/to/aggregate_code.py
    ```

2. **Move the Script to a Directory in Your PATH**:
    You can move the script to `/usr/local/bin/` or another directory that's in your PATH. Make sure to rename it to `aggregate_code` (without the `.py` extension) so you can run it directly:
    ```sh
    sudo cp -f aggregate_code.py /usr/local/bin/aggregate_code
    ```

3. **Ensure `/usr/local/bin` is in Your PATH**:
    Check your PATH to ensure `/usr/local/bin` is included:
    ```sh
    echo $PATH
    ```

    If `/usr/local/bin` is not in your PATH, you need to add it. Edit your `~/.zshrc` file (or `~/.bashrc` if you use bash) and add the following line:
    ```sh
    export PATH=$PATH:/usr/local/bin
    ```

    Then, reload your shell configuration:
    ```sh
    source ~/.zshrc
    ```

4. **Update the Shebang Line in Your Script**:
    Make sure the shebang line at the top of your script points to the correct Python interpreter in your virtual environment, once activated, one can find the path of this venv with 
    ```sh
    which python
    ```
    For example:
    ```sh
    #!/home/user/.pyenv/versions/my_custom_env/bin/python
    ```

5. **Test the Script**:
    Now you should be able to run the script from any directory:
    ```sh
    aggregate_code /path/to/your/folder
    ```

### Additional Troubleshooting Steps
If you still encounter issues, consider the following:

- **Verify the Script Path**:
    Make sure the script is indeed located in `/usr/local/bin` and named `aggregate_code`:
    ```sh
    ls -l /usr/local/bin/aggregate_code
    ```

- **Check for Typographical Errors**:
    Ensure you typed the command correctly. Even small typos can cause the command to not be found.

- **Restart Your Terminal**:
    Sometimes changes to the PATH might require a terminal restart to take effect.

These steps should help you get the script recognized and executable from any directory.