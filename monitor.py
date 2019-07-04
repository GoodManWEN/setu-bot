import time
import os

pid = os.getpid()
current_path = os.getcwd()

with open(os.path.join(current_path , "pidlog.out"),'a') as f:
    f.write("[{0}] current pid = {1}\n".format(time.ctime(time.time()),pid))

path = r'/root/coolq-data/aside/Random-colorpic-robot/app.py'
start_time = os.stat(path).st_mtime
docker_command = 'docker run -d --name=pybot --restart=always --network=web -v /root:/root python:bot python3 /root/coolq-data/aside/Random-colorpic-robot/app.py'

os.system('docker stop pybot')
os.system('docker rm pybot')
os.system(docker_command)

while True:
    time.sleep(0.5)
    update_time = os.stat(path).st_mtime
    if update_time != start_time:
        os.system('docker stop pybot')
        os.system('docker rm pybot')
        os.system(docker_command)
        start_time = update_time