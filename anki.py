#!/usr/bin/python
# encoding: utf-8
import json
import sys
import urllib2

from workflow import Workflow3
from workflow.notify import notify

reload(sys)
sys.setdefaultencoding('utf8')


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params))
    response = json.load(urllib2.urlopen(urllib2.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


def main(wf):
    import ast
    # 得到查询字符串
    user_dict = ast.literal_eval(wf.args[0])
    # 拼接卡片字段
    front = user_dict['pinyin']
    jieshi = '<br/>'.join(user_dict['jieshi'])
    back = user_dict['word'] + '<br>' + jieshi
    # 添加卡片信息
    note = {
        "deckName": u"字词",
        "modelName": "Basic",
        "fields": {
            "Front": front,
            "Back": back
        },
        "options": {
            "allowDuplicate": False
        },
        "tags": [
            "百度词典"
        ]
    }
    # 添加到Anki
    try:
        invoke('addNote', note=note)
        notify(title=u'已成功添加卡片信息', text=user_dict['word'])
    except:
        notify(u'添加卡片失败！')
    # Send output to Alfred
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3(libraries=['./lib'])
    # Assign Workflow logger to a global variable for convenience
    # log = wf.logger
    sys.exit(wf.run(main))
