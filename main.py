from api import *


def 组织用户信息(任务序号):
    try:
        信息 = 获取用户信息()
        信息 = 信息['data']['user']
        用户名, 简介, uid, 等级, 喵币, 经验 = 信息['name'], 信息['bio'], 信息['id'], 信息['level_id'], 信息[
            'neko_coin'], 信息['exp']
        等级 = 获取等级(等级)
        msg = f'''
                    当前用户({任务序号}): {用户名} ({uid})
                    简介: {简介}
                    喵币数量: {喵币}
                    经验: {等级} ({经验})'''
        return msg

    except Exception as e:
        log.error(f"获取信息失败,错误信息:\n{e}")
        return


def 执行用户任务(ckk, 任务序号):
    s.headers = {
        "authorization": ckk
    }
    签到成功 = False
    msg = 组织用户信息(任务序号)
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
        if '#' in ckk:
            try:
                ckk = 登录(ckk[:ckk.find('#')], ckk[ckk.find('#') + 1:])
            except Exception as e:
                log.error("登录失败: " + ckk[:ckk.find('#')] + "," + ckk[ckk.find('#') + 1:])
                log.warning(f"任务执行失败! 跳过执行第 {num}/{len(ck)} 个用户任务,错误信息:\n{e}")
        log.info(f"当前开始执行第 {num}/{len(ck)} 个用户任务")
        info.append(执行用户任务(ckk, f'{num}/{len(ck)}'))

    # log.info(f'共 {num} 个用户 所有任务执行完毕，开始推送！')
    # if 推送任务(info):
    #     log.success("推送任务执行成功")
    # else:
    #     log.error("推送任务执行失败")


def handler(event, context):
    main()
    return 'success'


if __name__ == '__main__':
    main()
