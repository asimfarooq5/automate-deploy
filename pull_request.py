import os
import shlex
import subprocess
from flask import Flask, request

app = Flask(__name__)


def run(command):
    subprocess.check_call(shlex.split(command))


def pull_and_restart(path, service_name):
    os.chdir(path)
    run('git pull')
    run(f"systemctl restart {service_name}")


def create_repo(path, repo_name):
    os.chdir(path)
    run(f'mkdir {repo_name}')
    run('git init')
    run('touch README.md')
    run('git add README.md')
    run('git commit -am "initial commit"')
    run(f'git remote add origin git@github.com:codebasepk/{repo_name}.git')
    run('git push -u origin master')


@app.route('/create_repo', methods=['POST'])
def created():
    create_repo(request.form['path'],  request.form['repo_name'])
    return 'Ok', 200


@app.route('/pull_restart', methods=['POST'])
def pull_restart():
    pull_and_restart('/root/warehouse-project', 'warehouse')
    return 'Ok', 200


if __name__ == '__main__':
    app.run(host='locahost', debug=True, threaded=True)
