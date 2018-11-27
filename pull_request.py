import os
import subprocess
from flask import Flask

app = Flask(__name__)


def pull_and_restart(path, service_name):
    os.chdir(path)
    subprocess.check_call(['git', 'pull'])
    subprocess.check_call(['systemctl', 'restart', service_name])


@app.route('/pull_restart', methods=['POST'])
def pull_restart():
    pull_and_restart('/root/warehouse-project', 'warehouse')
    return 'Ok', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
