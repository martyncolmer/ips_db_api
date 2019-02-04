from IPS_Package import main
import time
import sys
import ast


print("In RUN_IPS.py")

# Get run id and steps to run from the system arguments
run_id = sys.argv[1]
steps_to_run = sys.argv[2]

steps_to_run = ast.literal_eval(steps_to_run)

print("Calling calculations")
main.run_ips(run_id, steps_to_run)
print("Finished calculations")
