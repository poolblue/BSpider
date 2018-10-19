import utils
import time
import re
import os

if __name__ == '__main__':
    # dm_url_list = utils.history_dm_url_list('34039896', 10)
    #
    # for url in dm_url_list:
    #     dm_content = utils.get_dm_content(url)
    #     patten = re.compile(r'">(.*?)</d>')
    #     op = patten.findall(dm_content)
    #     print(len(op))
    #
    #     fd = os.open("kp", os.O_APPEND | os.O_CREAT | os.O_WRONLY)
    #     for ele in op:
    #         os.write(fd, bytes(ele + '\n', 'UTF-8'))
    #     os.close(fd)

    a_list = utils.get_aid_list()
    for aid in a_list:
        # 每个视频获取的天数，0表示只获取当天的
        dm_url_list = utils.history_dm_url_list(aid, 0)
        for url in dm_url_list:
            time.sleep(0.5)
            dm_content = utils.get_dm_content(url)
            patten = re.compile(r'">(.*?)</d>')
            op = patten.findall(dm_content)
            print(len(op))

            fd = os.open("kp", os.O_APPEND | os.O_CREAT | os.O_WRONLY)
            for ele in op:
                os.write(fd, bytes(ele + '\n', 'UTF-8'))
            os.close(fd)

