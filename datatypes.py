"""
Label table widget.

Authors: caobinbin(caobinbin@baidu.com)
Date:    2017/10/03
"""
import collections


Rooms = ['素草', '木琴', '凡花', '八月', '黑白', '夏尔', '暖春', '小院']

Sources = ['携程-预付', '美团-预定', '艺龙-预付', '线下', '去哪-预付', '去哪-现付']

Columns = ['Date', 'Room', 'Source', 'Price', 'Commission', 'Adjustment', 'Comment']

Record = collections.namedtuple('Record', ['source', 'room', 'price', 'commission', 'adjustment', 'checkin', 'checkout', 'comment'])
