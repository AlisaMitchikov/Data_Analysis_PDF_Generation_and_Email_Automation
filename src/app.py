import subprocess
import os
import sys

# Get the directory of the current file (app.py)
current_directory = os.path.dirname(os.path.abspath(__file__))

# Define the path to the virtual environment's Python executable
venv_python = os.path.join(os.path.dirname(sys.executable), 'python')

# Define the scripts you want to run
scripts = [
    'load_data_from_sources_to_dfs.py',
    'analysis_of_dfs_to_pdf.py',
    'send_pdf_via_email.py'
]

# Run each script in sequence
for script in scripts:
    script_path = os.path.join(current_directory, script)
    print('----')
    print(f'Running {script}...')
    result = subprocess.run([venv_python, script_path])
    
    # Check if the script ran successfully
    if result.returncode != 0:
        print(f'Error occurred while running {script_path}')
        break
