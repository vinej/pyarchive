import shlex
import subprocess
cmd = '''curl http://www.google.ca'''
args = shlex.split(cmd)
process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
print(stdout)
print(stderr)