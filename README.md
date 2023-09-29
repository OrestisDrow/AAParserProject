# AAParserProject - Specialized Log Parser

A specialized tool to parse log files searching for specific metrics with the ability to produce:
* A summary file for each metric as a Dictionary stored in a .txt file
* A parser error log file which contains any observed errors e.g. Corrupt Line structures, Missing Headers, Multiple Same Headers etc. 

## Features

* Extract and summarize key metrics from log files
* Generate detailed metrics and error reports
* Lightweight with zero non-standard library dependencies
* CLI command for easy parsing

# Installation
1) Clone the repo to your preferred folder:
   ```bash
    git clone https://github.com/OrestisDrow/AAParserProject.git
   ```
2) Navigate to the project directory:
    ```bash
    cd AAParserProject
    ```
3) (Recommended) Use a virtual environment:
    1) Create the venv:
       ```bash
       python -m venv venv
       ```
    2) Activate the venv:
 
        **Windows Command Prompt (cmd)**:
        ```cmd
        venv\Scripts\activate.bat
        ```
        
        **Windows PowerShell**:
        ```PowerShell
        .\venv\Scripts\Activate.ps1
        ```
        Remember, for running scripts in PowerShell, you might have to run powershell as admin
        and change the execution policy to allow scripts to run. You can do this with:
        ```PowerShell
        Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
        ```

        **Linux/Mac**:
        ```cmd
        source venv/bin/activate
        ```   
    3) When you are done checking this project out, *never forget* to deactivate the venv:
       ```bash
        deactivate
        ```   
4) Install the Package:
    ```bash
    pip install .
    ```   

# Usage
1) Command Line Usage:

   Simply run:
   ```bash
   run-logparser
   ```
   This will parse the logfile ../AAParserProject/logparser/logfile.txt and produce summaries and error reports under the ../AAParserProject/RunResults/ folder.

   **NOTE:** The default logfile I have included has a lot of errors, this is on purpose as a showcase for the first time you run the parser before trying
   out your own log files in order to get a good first glance of how the errors are reported.
   
   To test with your own log file, replace logfile.txt in the root directory with your own log file (keeping the same name) and run the above command again.
3) For Developers:
   
   You can use the LogFileParser class in your own Python projects:
   ```python
   from logparser.log_file_parser import LogFileParser

   log_file_path = "/path/to/log_file.txt"
   parser = LogFileParser(log_file_path)
   
   # Parse the log file
   parsed_data = parser.parse()
   
   # Save results to a file (Optional)
   parser.save()
   ```
# Testing

You can run my tests by simply:
```bash
pytest
```
