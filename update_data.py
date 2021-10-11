import runpy

# This python script runs the below python scripts that import
# data into my databased

runpy.run_path(path_name="committees.py")

runpy.run_path(path_name="members.py")

runpy.run_path(path_name="reports.py")

runpy.run_path(path_name="subcommittees.py")

runpy.run_path(path_name="legislators.py")