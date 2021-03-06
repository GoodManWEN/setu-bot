RUNPWD=`dirname $0`

su

# update apt & install enviorment
apt update
apt upgrade

apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common \
    htop \
    vim \
    wget

# install docker-ce
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

apt-key fingerprint 0EBFCD88

add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

apt-get update
apt-get install docker-ce docker-ce-cli containerd.io

# docker network
docker network create web

# docker coolq
cd /root
mkdir coolq-data
docker pull coolq/wine-coolq

docker run --name=coolq -d --restart=always -p 8080:9000 -p 5700:5700  --network web -v /root/coolq-data:/home/user/coolq -e VNC_PASSWD=yourpassword -e COOLQ_ACCOUNT=78888888 -e COOLQ_URL=http://dlsec.cqp.me/cqp-tuling coolq/wine-coolq

# coolq http plug-in
cd /root/coolq-data/app
wget https://github.com/richardchien/coolq-http-api/releases/download/v4.10.0/io.github.richardchien.coolqhttpapi.cpk
cd /root/coolq-data/data/app
mkdir io.github.richardchien.coolqhttpapi
cd io.github.richardchien.coolqhttpapi
cp $RUNPWD/coolqhttpapi.config.json ./config.json
cd $RUNPWD

# docker redis
docker pull redis:5.0
docker run -d --name=redis --restart=always --network=web redis:5.0 redis-server --appendonly yes --requirepass "redispassword"

# docker python-reverse-ws-server
/root/coolq-data/data/image/setu
mkdir /root/coolq-data/aside
cd  /root/coolq-data/aside
mkdir Random-colorpic-robot
cd Random-colorpic-robot
cp $PWD/app.py ./app.py
cp $PWD/py.Dockerfile ./Dockerfile
docker build -t python:bot .
docker run -d --name=pybot --restart=always --network=web -v /root:/root python:bot python3 /root/coolq-data/aside/Random-colorpic-robot/app.py

# docker node-we-server
cd  /root/coolq-data/aside
mkdir CQ-picfinder-robot
cd CQ-picfinder-robot
cp $PWD/picfinder.config.json ./config.json
cp $PWD/node.Dockerfile ./Dockerfile
docker build -t node:bot .
docker run -d --name=jsbot --restart=always --network=web -v /root/coolq-data/aside/CQ-picfinder-robot/config.json:/root/CQ-picfinder-robot/config.json node:bot npm start

# monitor
cd  /root/coolq-data/aside
mkdir daemon
cd daemon
cp $PWD/monitor.py ./monitor.py
nohup python3 monitor.py > nohup.out 2>&1 &
