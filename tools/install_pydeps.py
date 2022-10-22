"""CI/CD script for installing python dependencies in test runners"""


import subprocess
import time


def attempt(arg_list, max_attempts=1, name=''):
    retries = 0
    while retries < max_attempts:
        proc = subprocess.Popen(arg_list)

        # Keep running until finish or failure (may hang)
        while proc.poll() is None:
            time.sleep(.1)

        # Proc finished, check for valid return code
        if proc.returncode == 0:
            print(f"\n[INSTALL_PYDEPS] SUCCESS for process '{name}'\n")
            break
        else:
            # Likely failure, retry
            print(f"\n[INSTALL_PYDEPS] FAILURE for process '{name}', retrying!\n")
            retries += 1
    else:
        # Retries exceeded
        raise Exception(f"[INSTALL_PYDEPS] Retries exceeded for proc '{name}'!")


def run():
    steps = {
        'step1': """python -m pip install -U pip setuptools wheel""".split(' '),
        'step2': """pip install pytest-playwright""".split(' '),
        'step3': """playwright install""".split(' '),
        'step4': """pip install .[test]""".split(' '),
    }

    for step_name, step_arglist in steps.items():
        print(f"\n[INSTALL_PYDEPS] Attempt '{step_name}' -> Run '{' '.join(step_arglist)}'\n")
        attempt(step_arglist, max_attempts=3, name=step_name)


if __name__ == '__main__':
    run()
