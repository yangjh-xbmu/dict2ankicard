#!/usr/bin/python
# encoding: utf-8

import sys
from workflow import Workflow3

reload(sys)
sys.setdefaultencoding('utf8')


def get_means(query):
    import subprocess
    import ast

    # 使用子进程得到词语解释
    cmd = 'python ./lib/get_data.py ' + query
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, executable="/bin/bash")
    while p.poll() is None:
        line = p.stdout.readline()
        user_dict = ast.literal_eval(line)
        wf.add_item(title=user_dict['word'], arg=user_dict.__str__(), valid=True)
        wf.add_item(title=user_dict['pinyin'])
        for jieshi in user_dict['jieshi']:
            wf.add_item(title=jieshi)
        return user_dict
    try:
        p.kill()
    except OSError:
        pass


def get_query(wf):
    query = wf.args[0].strip().replace("\\", "")

    if not isinstance(query, unicode):
        query = query.decode('utf8')

    return query


def main(wf):
    # 得到查询字符串
    query = get_query(wf)
    # 得到该字符串的解释
    get_means(query)
    # 输出到Alferd
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3(libraries=['./lib'])
    # Assign Workflow logger to a global variable for convenience
    # log = wf.logger
    sys.exit(wf.run(main))
