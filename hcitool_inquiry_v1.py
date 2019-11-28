import subprocess

while True:

    print(subprocess.Popen('hcitool inq', bufsize=0, shell=True, stdout=subprocess.PIPE, stderr=
    subprocess.STDOUT))


