from api import *


def 执行用户任务(ckk, 任务序号):
    s.headers = {
        "authorization": ckk
    }
    签到成功 = False

    信息 = 获取用户信息()
    信息 = 信息['data']['user']
    用户名, 简介, uid, 等级, 喵币, 旧经验 = 信息['name'], 信息['bio'], 信息['id'], 信息['level_id'], 信息[
        'neko_coin'], 信息['exp']
    等级 = 获取等级(等级)
    msg = f'''
                当前用户({任务序号}): {用户名} ({uid})
                简介: {简介}
                喵币数量: {喵币}
                经验: {等级} ({旧经验})'''

    log.info('获取信息成功!' + msg)
    if 执行签到任务:
        log.success("开始执行签到任务")
        ret = 签到()
        if '签到成功' in str(ret) or '已签到' in str(ret):
            签到成功 = True
        ret = ret['msg']
        if 签到成功:
            log.success(f"签到执行任务成功: {ret}")
        else:
            log.error(f"签到执行任务失败: {ret}")

    信息 = 获取用户信息()
    信息 = 信息['data']['user']
    经验 = 信息['exp']
    经验差 = 经验 - 旧经验
    msg = msg[:-1] + f'''+{经验差})
                今日任务执行完毕!
                签到成功: {签到成功}
                ----------------------------------------------'''
    return msg


def 推送任务(info):
    try:
        总msg = ''
        for msg in info:
            总msg += msg
        with open(f'log.log', 'r', encoding='utf-8') as f:
            内容 = f.read()
            总msg += f'''
            详细调试信息:
            {内容}'''
        print(总msg)
        if Server酱_key != '':
            Server酱推送(总msg)
            return True
        if pushplus_key != '':
            pushplus推送(总msg)
            return True
        log.warning(f'未配置推送地址!')
        return False
    except Exception as e:
        log.warning(e)
        return False


def main():
    import os
    if os.path.exists("log.log"):
        os.remove("log.log")
    log.warning(f"当前版本为: {ver}")
    log.info("m站新站辅助工具")
    log.add('log.log', encoding='utf-8', retention=0)
    num = 0
    info = []
    for ckk in ck:
        num += 1
        任务序号 = f'{num}/{len(ck)}'
        if '#' in ckk:
            try:
                ckk = 登录(ckk[:ckk.find('#')], ckk[ckk.find('#') + 1:])
            except Exception as e:
                log.error("登录失败: " + ckk[:ckk.find('#')] + "," + ckk[ckk.find('#') + 1:])
                log.warning(f"任务执行失败! 跳过执行第 {任务序号} 个用户任务,错误信息:\n{e}")
                continue
        log.success(f"登录成功,authorization={ckk}")
        log.info(f"当前开始执行第 {任务序号} 个用户任务")
        info.append(执行用户任务(ckk, 任务序号))

    log.info(f'共 {num} 个用户 所有任务执行完毕，开始推送！')
    if 推送任务(info):
        log.success("推送任务执行成功")
    else:
        log.error("推送任务执行失败")


def handler(event, context):
    main()
    return 'success'


if __name__ == '__main__':
    main()
