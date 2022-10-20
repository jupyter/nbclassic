"""CI/CD debug script"""


import os
import subprocess
import time


def run():
    for stepnum in range(10):
        print(f'[RUNSUITE_REPEAT] {os.getcwd()} :: {[os.path.exists("nbclassic"), os.path.exists("nbclassic/tests"), os.path.exists("nbclassic/tests/end_to_end"), os.path.exists("tools/runsuite_repeat.py")]}')
        try:
            proc = subprocess.run('pytest -sv tests/end_to_end')
        except Exception:
            print(f'\n[RUNSUITE_REPEAT] Run {stepnum} -> Exception')
            continue
        print(f'\n[RUNSUITE_REPEAT] Run {stepnum} -> {"Success" if proc.returncode == 0 else proc.returncode}\n')


if __name__ == '__main__':
    run()
