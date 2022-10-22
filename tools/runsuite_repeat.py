"""CI/CD debug script"""


import os
import subprocess
import time


def run():
    for stepnum in range(10):
        try:
            proc = subprocess.run(['pytest', '-sv', 'nbclassic/tests/end_to_end'])
        except Exception:
            print(f'\n[RUNSUITE_REPEAT] Exception -> Run {stepnum}\n')
            continue
        print(f'\n[RUNSUITE_REPEAT] {"Success" if proc.returncode == 0 else proc.returncode} -> Run {stepnum}\n')


if __name__ == '__main__':
    run()
