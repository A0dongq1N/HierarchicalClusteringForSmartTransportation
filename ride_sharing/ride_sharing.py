#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""拼车流程"""

__author__ = 'Aodongq1n'

import os
import time

import HCFST.conf as conf
from HCFST.objects.cluster_group import ClusterGroup
from HCFST.objects.point import Point
from HCFST.objects.user_schedule import UserSchedule
from HCFST.objects.user_schedule_group import UserScheduleGroup
from HCFST.tools.single_pickle import load_object, save_object


def get_unixtime(date_, time_):
    return int(time.mktime(time.strptime(str(date_) + ' ' + str(time_), "%Y-%m-%d %H:%M:%S")))


def load_usg(usg_id):
    if os.access("../data/%s.pkl" % usg_id, os.F_OK):
        usg = load_object("../data/%s.pkl" % usg_id)
    else:
        usg = UserScheduleGroup(usg_id)
    return usg


def save_usg(usg):
    save_object(usg, "../data/%s.pkl" % usg.usg_id)


def add_schedule_run(us_id, line_id, o_address, o_gps, d_address, d_gps, start_date,
                     earliest_start_time, latest_start_time, ticket_count):
    # todo 调用之前需要先通过规则判断车辆是否足够，需要用规则判断max_car_num
    # 注：与数据库内同名的参数，参数含义、格式也相同
    earliest_start_unixtime = get_unixtime(start_date, earliest_start_time)
    latest_start_unixtime = get_unixtime(start_date, latest_start_time)

    usg_id = str(line_id) + str(conf.get_ride_sharing_deadline(earliest_start_unixtime))
    usg = load_usg(usg_id)
    user_schedule = UserSchedule(us_id, line_id, Point(o_address, o_gps), Point(d_address, d_gps),
                                 earliest_start_unixtime, latest_start_unixtime, ticket_count)
    usg.add(user_schedule)
    save_usg(usg)
    ctg = ClusterGroup(usg)
    return ctg.run()  # todo 最新的拼车方案，需将结果入撮合记录表


def remove_schedule_run(us_id, line_id, start_date, earliest_start_time):
    # 注：与数据库内同名的参数，参数含义、格式也相同
    earliest_start_unixtime = get_unixtime(start_date, earliest_start_time)
    usg_id = str(line_id) + str(conf.get_ride_sharing_deadline(earliest_start_unixtime))
    usg = load_usg(usg_id)
    usg.remove(us_id)
    save_usg(usg)
    ctg = ClusterGroup(usg)
    return ctg.run()  # todo 最新的拼车方案，需将结果入撮合记录表
