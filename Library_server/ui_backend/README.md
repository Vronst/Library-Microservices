# Python part of this project

To configure python, you have to have [python](https://www.python.org/downloads/release/python-3131/) installed.
Then as per docker configuration you need to create .env file (see main readme).
After that just create your enviroment
Windows:
```bash
python -m venv .venv
```
Linux (you may also need to apt install python3-venv)
```bash
python3 -m venv .venv
```
Activate virtual enviroment (you should be in /Library_AM)
Windows:
```bash
./.venv/Scripts/activate
```
Linux:
```bash
source /.venv/bin/activate
```
And now install requirements (now you should be in Library_AM/ui_backend):
Windows:
```bash
pip install -r requirements.txt
```
Linux
```bash
pip3 install -r requirements.txt
```
