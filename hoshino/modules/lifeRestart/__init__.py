# coding=utf-8
from hoshino import R, Service, priv
from hoshino.typing import HoshinoBot, CQEvent
from .Life import Life
from .PicClass import *
import traceback
import time
import random

sv = Service(
    name='人生重来模拟器',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.SUPERUSER,  # 管理权限
    visible=True,  # False隐藏
    enable_on_default=True,  # 是否默认启用
    bundle='娱乐',  # 属于哪一类
)


def genp(prop):
    ps = []
    # for _ in range(4):
    #     ps.append(min(prop, 8))
    #     prop -= ps[-1]
    while True:
        for i in range(0, 4):
            if i == 3:
                ps.append(prop)
            else:
                if prop >= 10:
                    ps.append(random.randint(0, 10))
                else:
                    ps.append(random.randint(0, prop))
                prop -= ps[-1]
        if ps[3] < 10:
            break
        else:
            prop = 20
            ps.clear()
    return {
        'CHR': ps[0],
        'INT': ps[1],
        'STR': ps[2],
        'MNY': ps[3]
    }


@sv.on_fullmatch("人生重来", '人生重启')
async def remake(bot, ev: CQEvent):
    Life.load(FILE_PATH + '/data')
    life = Life()
    life.setErrorHandler(lambda e: traceback.print_exc())
    life.setTalentHandler(lambda ts: random.choice(ts).id)
    life.setPropertyhandler(genp)

    life.choose()

    choice = 0
    person = "你本次重生的基本信息如下：\n\n【你的天赋】\n"
    for t in life.talent.talents:
        choice = choice + 1
        person = person + str(choice) + "、天赋：【" + t.name + "】" + " 效果:" + t.desc + "\n"

    person = person + "\n【基础属性】\n"
    person = person + "   美貌值:" + str(life.property.CHR) + "  "
    person = person + "智力值:" + str(life.property.INT) + "  "
    person = person + "体质值:" + str(life.property.STR) + "  "
    person = person + "财富值:" + str(life.property.MNY) + "  "
    pic = ImgText(person)
    await bot.send(ev, "你的命运正在重启....")
    time.sleep(5)
    await bot.send(ev, pic.draw_text(), at_sender=True)
    res = life.run()
    mes = '\n'.join('\n'.join(x) for x in res)
    pic = ImgText(mes)
    await bot.finish(ev, pic.draw_text(), at_sender=True)