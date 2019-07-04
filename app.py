from aiocqhttp import CQHttp
import aiohttp
import asyncio
import re
import random 
import aioredis
import pickle
import os
import logging
import sys
import json
import time
logging.basicConfig(stream=sys.stdout)

bot = CQHttp(enable_http_post=False)
pat_iamge = re.compile('\[CQ:image,file=.+?\]')
pat_2 = re.compile('.*色图片')
pat_3 = re.compile('[\d]+?_')

class Daemon:
    pass

daemon_reids = Daemon()

YOUR_QQ = 341000000      # 机器人QQ号
RANDOM_CHAT_HLIMIT = 300 # 随机回复最长间隔
RANDOM_CHAT_LLIMIT = 50  # 随机回复最短间隔
SETU_BUFFER_NUM = 200    # 色图缓存张数
TULING_KEY = "c9ebb7fe3*************************" # 图灵APIKEY
TULING_MAX = 500         # 图灵每天最大回复数量
TULING_TIMEOUT = 5       # 图灵请求超时
GROUP_CD_TIME = 10       # 单个群组请求色图最短间隔
tuling_count = 0
random_chat_count = 0
random_chat_target = random.randint(RANDOM_CHAT_LLIMIT,RANDOM_CHAT_HLIMIT)
CWD_PATH = os.path.abspath('/root/coolq-data/data/image/setu')
group_cd = {}
REDIS_HOST = '172.18.0.3' 
REDIS_PORT = 6379
REDIS_PASS = "redispassword"

dig_conv = {'1':'一','2':'二','3':'叁','4':'肆','5':'伍','6':'六','7':'柒','8':'八','9':'玖','0':'零'}

# init
if not os.path.exists(os.path.join(CWD_PATH , 'pic_infos.pickle')):
    pic_infos = {}
    with open(os.path.join(CWD_PATH , 'pic_infos.pickle'),'wb') as fa:
        pickle.dump(pic_infos , fa)
else:
    with open(os.path.join(CWD_PATH , 'pic_infos.pickle'),'rb') as fa:
        pic_infos = pickle.load(fa)


async def tuling(msg ,id_):
    global tuling_count

    tuling_count += 1
    if tuling_count > TULING_MAX:
        return "图灵今天累了，要歇了，有缘大书库的boss门前再见吧"

    params = {"key":TULING_KEY , "info":msg ,"userid":id_}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('http://www.tuling123.com/openapi/api', params = params,timeout = TULING_TIMEOUT) as resp:
                ret_val = json.loads(await resp.text())
                return ret_val['text']
        except Exception as e:
            logging.warning(f"{type(e)}:{e}")
            return "电波不佳，听不懂你在说什么"

async def get_music(music_name):
    params = { "type":"search" ,"search_type":1 ,"s":music_name ,"limit":5}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('https://api.imjad.cn/cloudmusic/', params = params,timeout = TULING_TIMEOUT) as resp:
                ret_val = json.loads(await resp.text())
                return f"[CQ:music,type=163,id={ret_val['result']['songs'][0]['id']}]"
        except Exception as e:
            logging.warning(f"{type(e)}:{e}")
            return f"网络中断，老司机翻车了，并没有找到歌"

@bot.on_message('group')
async def handle_msg(context):
    global random_chat_count , random_chat_target ,RANDOM_CHAT_LLIMIT ,RANDOM_CHAT_HLIMIT
    # await bot.send(context , repr(context['message']))

    msg = context['message']
    ret_val = False

    # 被at
    if f'[CQ:at,qq={YOUR_QQ}]' in msg:

        msg = msg.replace(f'[CQ:at,qq={YOUR_QQ}]','').strip()

        pic_find = pat_iamge.findall(msg)
        # 没有图
        if not pic_find and msg != "":
            if 'zaima' in msg:
                ret_val = "buzai, cnm !" 
            else:
                request_user_id = context['user_id']
                ret_val = await tuling(msg ,request_user_id)
            
            if ret_val:
                return {'reply' : ret_val}
        # 有图不应答
        else:
            pass
    # 未被at
    else:
        msg = msg.strip()

        if '辣鸡' in msg or "垃圾" in msg:
            ret_val = "你才辣鸡呢，你全家都辣鸡！"
        elif '傻吊' in msg or "傻屌" in msg:
            ret_val = "傻屌！"
        elif '丢人' in msg:
            ret_val = "丢人，你退群吧！"
        elif '色图' in msg:
            pat_2_mode = pat_2.findall(msg)
            group_id = context['group_id']

            if pat_2_mode:
                return {'reply': "你说你[CQ:emoji,id=128052]呢？"}

            current_time = time.time()
            if group_id not in group_cd:
                group_cd[group_id] = current_time
            else:
                if current_time - group_cd[group_id] < GROUP_CD_TIME:
                    return {'reply': "车速太快啦，这谁顶得住啊！"}
                else:
                    group_cd[group_id] = current_time


            if len(pic_infos) > 0:
                try:
                    request_user_id = context['user_id']
                    for paths in os.walk(CWD_PATH):
                        paths = paths[2];break
                    if paths:
                        while True:
                            samp_path = random.sample(paths,1)[0]
                            if samp_path not in ['pic_infos.pickle']:
                                break
                        pic_id = pat_3.findall(samp_path)[0][:-1]
                        pic_id_max = ''
                        for i in pic_id:
                            pic_id_max += dig_conv[i]
                        title , author = pic_infos[pic_id]
                        rvalue = await bot.send(context, f'[CQ:at,qq={request_user_id}] [CQ:image,file=\\setu\\{samp_path}]\n 【标题】：{title} \n 【作者】：{author} \n 【ID】：{pic_id_max}\n')

                        if rvalue['message_id']:
                            os.remove(os.path.join(CWD_PATH,samp_path))
                            pic_infos.pop(pic_id)
                        else:
                            await bot.send(context, f'[CQ:at,qq={request_user_id}] 老司机翻车啦！')
                    else:
                        await bot.send(context, f'[CQ:at,qq={user_id}] 色图姬已经被榨干啦，没有色图啦')
                except:
                    pass

            ret_val = False
        elif msg[:2] in ["开车","发车","车来","车来"] and len(msg) < 4:
            ret_val = "发NMB的车"
            #
        elif msg[:2] == '一首' and '送给' in msg:
            songname = msg[msg.index('一首')+2:msg.index('送给')].strip()
            if '届かない恋' in songname or '届不到的恋' in songname:
                if "爱衣" in msg or "茅衣" in msg or "茅野爱衣" in msg:
                    ret_val = '[CQ:music,type=163,id=509106602]'
                elif "冬马" in msg or "冬马和纱" in msg or "天生目仁美" in msg:
                    ret_val = '[CQ:music,type=163,id=449818930]'
                elif "雪菜" in msg or "米泽圆" in msg or "米澤円" in msg:
                    ret_val = '[CQ:music,type=163,id=32272866]'
                elif "千晶" in msg or "和泉千晶" in msg:
                    ret_val = '[CQ:music,type=163,id=775851]'
                elif "原版" in msg or "上原" in msg or '上原れな' in msg:
                    ret_val = '[CQ:music,type=163,id=27594382]'
                else:
                    song_dict = [("爱衣版",'[CQ:music,type=163,id=509106602]'),
                                ("冬马版",'[CQ:music,type=163,id=449818930]'),
                                ("雪菜版",'[CQ:music,type=163,id=32272866]'),
                                ("千晶版",'[CQ:music,type=163,id=775851]'),
                                ("原版",'[CQ:music,type=163,id=27594382]')]
                    samples = random.sample(song_dict,1)[0]
                    # await bot.send(context , f"[CQ:image,file=\\todokanai\\kuma.gif]一首{samples[0]}届かない恋送给在座的各位！")
                    ret_val = samples[1]
            else:
                ret_val = await get_music(songname)
        else:
            random_chat_count += 1
            if random_chat_count >= random_chat_target:
                request_user_id = context['user_id']
                ret_val = ret_val = await tuling(msg ,request_user_id)
                random_chat_count = 0
                random_chat_target = random.randint(RANDOM_CHAT_LLIMIT,RANDOM_CHAT_HLIMIT)
            else:
                ret_val = False
        
        if ret_val:
            return {'reply': ret_val}

@bot.on_notice('group_increase')
async def handle_group_increase(context):
    await bot.send(context, message='欢迎新人～',
                   at_sender=True, auto_escape=True)

@bot.on_request('group')
async def handle_request(context):
    return {'approve': True}

@bot.on_request('friend')
async def handle_friend_request(context):
    approve_ = True if context['comment'] == '天王盖地虎' else False
    return {'approve': approve_}

async def download_pics():
    global daemon_reids

    daemon_reids._pool = await aioredis.create_redis_pool((REDIS_HOST, REDIS_PORT),password = REDIS_PASS, minsize=2, maxsize=10, loop=loop)

    await asyncio.sleep(2)

    while True:
        for files in os.walk('/root/coolq-data/data/image/setu'):
            files = files[2];break
        if len(files) < SETU_BUFFER_NUM:
            while True:
                getted_pid = await daemon_reids._pool.randomkey()
                getted_pid = getted_pid.decode('utf-8')
                if getted_pid not in ['informations'] and getted_pid not in pic_infos:
                    break
            pic_url = await daemon_reids._pool.get(getted_pid)
            pic_url = pic_url.decode('utf-8')
            infos = await daemon_reids._pool.hget("informations",getted_pid)
            splited = infos.decode('utf-8').split('$`$~')
            title , author = splited[0] , splited[1]

            rvalue = os.system(f'wget --header="Referer: https://www.pixiv.net" -P {CWD_PATH} {pic_url}')
            if rvalue == 0:
                pic_infos[getted_pid] = (title,author)
                with open(os.path.join(CWD_PATH , 'pic_infos.pickle'),'wb') as fa:
                    pickle.dump(pic_infos , fa)
            await asyncio.sleep(2)
        else:
            await asyncio.sleep(120)

async def tuling_everyday():
    global tuling_count
    while True:
        await asyncio.sleep(86400)
        tuling_count = 0

loop = asyncio.get_event_loop()
loop.create_task(download_pics())
loop.create_task(tuling_everyday())
bot.run(host='172.18.0.4', port=8700)