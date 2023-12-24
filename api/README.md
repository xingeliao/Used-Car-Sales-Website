Python 3.9 

Initialize
`python3.9 -m venv .` inside the 'api' folder.
`source bin/activate` to activate the virtual environment (MacOS) or `. venv\scripts\activate` (for Windows)
`pip install -r requirements.txt`

How to run the API locally
`export FLASK_APP="team85:create_app()"`
`flask run --debug`
