import sys
import subprocess

def default_workflow_output_handler(process):
    sys.stdout.flush()
    while True:
        next_line = process.stdout.readline()
        if not next_line:
            break
        print "\r" + next_line
        sys.stdout.flush()

def run_workflow(step_tuple, output_handler = default_workflow_output_handler):
    p = subprocess.Popen(step_tuple[0], stdout=subprocess.PIPE)
    output_handler(p)
    p.communicate()
    if len(step_tuple) > 1 and step_tuple[1]:
        run_workflow(step_tuple[1])
