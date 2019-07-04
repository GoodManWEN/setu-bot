FROM node:12-slim as builder

WORKDIR /build

RUN apt-get update \
 && apt-get install -y git \
 && git clone https://github.com/Tsuk1ko/CQ-picfinder-robot.git \
 && cd CQ-picfinder-robot \
 && cat config.default.json | sed 's/127.0.0.1/172.18.0.2/g;44d;43a "default": "",' > config.json \
 && npm i

FROM node:12-slim 

COPY --from=builder /build/CQ-picfinder-robot /root/CQ-picfinder-robot
WORKDIR /root/CQ-picfinder-robot
CMD ["npm","start"]