# AAParserProject
Clone repo to whatever folder
Bash:
git clone https://github.com/OrestisDrow/AAParserProject

Navigate to repo
Bash:
cd AAParserProject

Set up Venv 
Bash:
python -m venv venv

Activate Venv
Bash
source venv/bin/activate for Linux/MacOS
venv\Scripts\activate for Windows Command Prompt
.\venv\Scripts\Activate.ps1 for Windows Powershell

Note: If you use Windows powershell in win11, you might want to change the default execution policy im addition to running PowerShell as admin in order to activate venv:
i.e.
PowerShell
 Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

Installl Package Locally
(venv) pip install.

(Optional) Run the tests I have pre-defined
pytest tests/

Usage:
From the command line, after activating venv, you can do:
Bash:
run-logparser


When done playing with this package deactivate the venv:
bash:
deactivate