#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""参数配置"""

__author__ = 'Aodongq1n'

#from HCFST.objects.point import Point

# MAX_USER_SCHEDULE_NUM = 100  # 一起拼车的最大用户行程数，超过设置时需在拼车前拆分行程组
DURATION_INFINITE = 10000  # 1万分钟视为行程时间最大值
MAX_TICKET_COUNT = 5  # 每车最多能卖出的票数
MAX_PICK_UP_DURATION = 15  # 接客最大行程时间
MAX_SCHEDULING_TIME = 30  # 调度确认后到乘客最早上车的预留时间
GPS_DISTANCE_THRESHOLD = 8  # km, gps距离阈值，用户与车的gps距离大于该值时不调度该车

TENCENT_MAP_KEY = '2M4BZ-WQBCX-SGY42-TVYL3-XZLO6-QPFPP'  # 腾讯地图秘钥，我的秘钥为：'TQABZ-NOSHV-R3FPX-UCFNH-LDWI5-V2FNH'


def get_ride_sharing_deadline(earliest_start_unixttime):
    return earliest_start_unixttime - 40 * 60  # 在接第一个人前40分钟
