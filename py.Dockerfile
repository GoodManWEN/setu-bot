FROM python:3.7.3-slim

RUN pip3 install aiocqhttp \
 && pip3 install aiohttp \ 
 && pip3 install aioredis

