#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""调度流程"""

__author__ = 'Aodongq1n'

import itertools
import math

import HCFST.conf as conf
from HCFST.objects.cluster_group import ClusterGroup
from HCFST.ride_sharing.ride_sharing import load_usg, get_unixtime
from HCFST.tools.tencent_direction import driving_direction


def gps_distance(gps1, gps2):
    """
    计算球面距离 \n
    :param lon_1: 坐标1经度
    :param lat_1: 坐标1纬度
    :param lon_2: 坐标2经度
    :param lat_2: 坐标2纬度
    :return: 球面距离，单位KM
    """
    # print(lon_1, lat_1, lon_2, lat_2)
    lat_1, lon_1 = gps1.split(',')
    lat_2, lon_2 = gps2.split(',')
    lat_1, lon_1, lat_2, lon_2 = float(lat_1), float(lon_1), float(lat_2), float(lon_2)
    if lon_1 == lon_2 and lat_1 == lat_2:
        return 0
    return 6371 * math.acos(math.cos(lat_1 * 3.1415926 / 180) * math.cos(lat_2 * 3.1415926 / 180) *
                            math.cos(lon_1 * 3.1415926 / 180 - lon_2 * 3.1415926 / 180) +
                            math.sin(lat_1 * 3.1415926 / 180) * math.sin(lat_2 * 3.1415926 / 180))


def car_user_duration(cars, user_schedules):  # todo：因为不用传时间，所以可以改成调用腾讯地图批量接口
    duration_dict = {}
    for car in cars:
        for us in user_schedules:
            gps_dis = gps_distance(car.gps, us.origin.gps)
            if gps_dis > conf.GPS_DISTANCE_THRESHOLD:
                duration = int(gps_dis * 1000)  # 用米数代表行程时间数
            else:
                _, duration, _ = driving_direction(car.gps, us.origin.gps)
            duration_dict[car.car_id + ',' + us.us_id] = duration
    return duration_dict


def user_destination_duration(user_schedules, d_gps):  # 乘客出发点到终点（机场）的时间
    # todo：因为不用传时间，所以可以改成调用腾讯地图批量接口
    user_destination_duration_dict = {}
    for us in user_schedules:
        _, duration, _ = driving_direction(us.origin.gps, d_gps)
        user_destination_duration_dict[us.us_id] = duration
    return user_destination_duration_dict


def run(cars, line_id, start_date, earliest_start_time, d_gps):
    """
    :param cars: 当前所有可用车辆
    :param line_id: 线路ID
    :param start_date: 开始日期
    :param earliest_start_time: 最早接客时间
    :param d_gps: 目的地GPS
    """
    # 注：与数据库内同名的参数，参数含义、格式也相同
    earliest_start_unixtime = get_unixtime(start_date, earliest_start_time)
    usg_id = str(line_id) + str(conf.get_ride_sharing_deadline(earliest_start_unixtime))
    usg = load_usg(usg_id)
    ctg = ClusterGroup(usg)
    result_clusters = ctg.run()  # todo 拼车方案需入调度表

    # 以下为调度过程
    car_user_duration_dict = car_user_duration(cars, usg.user_schedules)
    user_destination_duration_dict = user_destination_duration(usg.user_schedules, d_gps)
    results = []
    for rc in result_clusters:  # 遍历每个拼车订单
        min_scheduling_duration = conf.DURATION_INFINITE
        result_car = None  # 算法调度派的车
        result_order = None  # 接客顺序，如41230是先接rc.user_schedules列表中第4个用户行程，最后接第0个用户行程
        for p in itertools.permutations(range(len(rc.user_schedules))):  # 全排列，遍历所有行程顺序
            duration = 0
            for i in range(len(p) - 1):
                a = rc.user_schedules[p[i]].index
                b = rc.user_schedules[p[i + 1]].index
                duration += usg.duration_matrix[a][b]
            if duration <= conf.MAX_PICK_UP_DURATION:  # 接乘客行程总时间满足约束
                # duration 加上最后一个乘客出发点到终点（机场）的时间
                duration += user_destination_duration_dict[rc.user_schedules[p[-1]].us_id]
                for car in cars:
                    # 效率优化1：在此处才计算车辆和用户距离，不事先计算所有车辆和所有用户的距离
                    c_u_duration = car_user_duration_dict[car.car_id + ',' + rc.user_schedules[p[0]].us_id]
                    if c_u_duration > conf.MAX_SCHEDULING_TIME:
                        continue
                    tmp = duration + c_u_duration
                    if tmp < min_scheduling_duration:
                        min_scheduling_duration = tmp
                        # 效率优化2：若此时min_scheduling_duration已经足够小，是否可以直接派车，不再寻找最优？
                        result_car = car
                        result_order = p
        if result_car:
            results.append([rc.user_schedules, result_car, result_order])  # 一条调度结果依次是：哪些用户行程拼在一起，派哪辆车，接客顺序
        cars.remove(result_car)
    return results  # todo 调度方案需入调度表
