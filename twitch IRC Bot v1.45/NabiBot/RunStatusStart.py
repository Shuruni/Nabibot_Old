import subprocess


with open("GUI/Status.nabi", "r+") as f:
	f.write("Running")
	f.truncate()

proc = subprocess.Popen(['python', 'run.py'])
proc.communicate()
if proc.returncode != 0:
	with open("GUI/Status.nabi", "r+") as f:
		f.write("Crashed")
		f.truncate()
else:
	with open("GUI/Status.nabi", "r+") as f:
		f.write("Not Running")
		f.truncate()