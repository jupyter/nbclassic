"""CI/CD debug script"""


import subprocess
import time


def run():
    for stepnum in range(10):
        proc = subprocess.run('pytest -sv nbclassic/tests/end_to_end')
        print(f'\n[RUNSUITE_REPEAT] Run {stepnum} -> {"Success" if proc.returncode == 0 else proc.returncode}\n')


if __name__ == '__main__':
    run()
