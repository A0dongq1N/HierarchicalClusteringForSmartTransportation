#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""测试类,未使用单元测试标准方式测试"""

__author__ = 'Aodongq1n'

from HCFST.objects.car import Car
from HCFST.objects.point import Point
from HCFST.objects.user_schedule import UserSchedule
from HCFST.objects.cluster_group import ClusterGroup
from HCFST.objects.user_schedule_group import UserScheduleGroup
import HCFST.conf as conf
from HCFST.scheduling.scheduling import car_user_duration, user_destination_duration, run
from HCFST.ride_sharing.ride_sharing import save_usg, load_usg


def user_schedule_test(usa, usb):
    print('user_schedule_test:', usa.duration(usb), usb.duration(usa))


def user_schedule_group_test_add(usg, us):
    size = len(usg.user_schedules)
    shape = usg.duration_matrix.shape
    usg.add(us)
    assert len(usg.user_schedules) == size + 1, 'usg.user_schedules添加us失败'
    assert usg.duration_matrix.shape == (shape[0] + 1, shape[1] + 1), 'usg.duration_matrix添加行列失败'
    assert us.index == size, 'us更新index失败'


def user_schedule_group_test_remove(usg, us):
    size = len(usg.user_schedules)
    shape = usg.duration_matrix.shape
    usg.remove(us.us_id)
    assert len(usg.user_schedules) == size - 1, 'usg.user_schedules删除us失败'
    assert usg.duration_matrix.shape == (shape[0] - 1, shape[1] - 1), 'usg.duration_matrix删除行列失败'


def cluster_group_test_init(usg):
    cg = ClusterGroup(usg)
    assert cg.duration_matrix.shape == usg.duration_matrix.shape
    assert len(cg.clusters) == len(usg.user_schedules)
    for i in range(len(cg.clusters)):
        assert cg.clusters[i].ct_id == usg.user_schedules[i].us_id
        assert len(cg.clusters[i].user_schedules) == 1
        assert cg.clusters[i].user_schedules[0] == usg.user_schedules[i]
    return cg


def cluster_group_test_run(cg):
    print('cluster_group_test_run')
    return cg.run()


def scheduling_test_car_user_duration(car_list, user_schedules):
    print('scheduling_test_car_user_duration')
    print(car_user_duration(car_list, user_schedules))


def scheduling_test_user_destination_duration(user_schedules, d_gps):
    print('scheduling_test_user_destination_duration')
    print(user_destination_duration(user_schedules, d_gps))


def scheduling_test_run(car_list, line_id, start_date, earliest_start_time, d_gps):
    print('scheduling_test_run')
    result = run(car_list, line_id, start_date, earliest_start_time, d_gps)
    print(result)


if __name__ == '__main__':
    AIRPORT_POINT = Point('山东省青岛市城阳区青岛国际机场T2号航站楼', '36.268130,120.386090')
    # 第一个拼车时间段
    earliest_start_unixtime, latest_start_unixtime = 1560211200, 1560213000
    us1 = UserSchedule('us1', 'line1', Point('黄岛区1', '35.9755056588,120.1758384705'), AIRPORT_POINT,
                       earliest_start_unixtime, latest_start_unixtime, 2)
    us2 = UserSchedule('us2', 'line1', Point('黄岛区2', '35.9650859641,120.2292251587'), AIRPORT_POINT,
                       earliest_start_unixtime, latest_start_unixtime, 1)
    # user_schedule_test(us1, us2)  # 14 18
    us3 = UserSchedule('us3', 'line1', Point('黄岛区3', '35.9570271239,120.2331733704'), AIRPORT_POINT,
                       earliest_start_unixtime, latest_start_unixtime, 3)
    us4 = UserSchedule('us4', 'line1', Point('黄岛区4', '35.9488284946,120.2058792114'), AIRPORT_POINT,
                       earliest_start_unixtime, latest_start_unixtime, 3)
    us5 = UserSchedule('us5', 'line1', Point('黄岛区5', '35.9349305694,120.1742935181'), AIRPORT_POINT,
                       earliest_start_unixtime, latest_start_unixtime, 2)
    usg1 = load_usg(str('line1') + str(conf.get_ride_sharing_deadline(earliest_start_unixtime)))
    if len(usg1.user_schedules) == 0:
        print('测试usg增删us')
        user_schedule_group_test_add(usg1, us1)
        user_schedule_group_test_remove(usg1, us1)
        user_schedule_group_test_add(usg1, us1)
        user_schedule_group_test_add(usg1, us2)
        user_schedule_group_test_remove(usg1, us2)
        user_schedule_group_test_add(usg1, us2)
        user_schedule_group_test_add(usg1, us3)
        user_schedule_group_test_add(usg1, us4)
        user_schedule_group_test_add(usg1, us5)
        save_usg(usg1)
    # cg1 = cluster_group_test_init(usg1)
    # chr1 = cluster_group_test_run(cg1)
    # 第二个拼车时间段
    earliest_start_unixtime, latest_start_unixtime = 1560232800, 1560234600
    us6 = UserSchedule('us6', 'line1', Point('黄岛区6', '35.9521636329,120.1665687561'), AIRPORT_POINT,
                       earliest_start_unixtime, latest_start_unixtime, 1)
    us7 = UserSchedule('us7', 'line1', Point('黄岛区7', '35.9672394804,120.1638221741'), AIRPORT_POINT,
                       earliest_start_unixtime, latest_start_unixtime, 1)
    us8 = UserSchedule('us8', 'line1', Point('黄岛区8', '35.9782145541,120.1688003540'), AIRPORT_POINT,
                       earliest_start_unixtime, latest_start_unixtime, 2)
    usg2 = load_usg(str('line1') + str(conf.get_ride_sharing_deadline(earliest_start_unixtime)))
    if len(usg2.user_schedules) == 0:
        print('测试usg2增删us')
        user_schedule_group_test_add(usg2, us6)
        user_schedule_group_test_add(usg2, us7)
        user_schedule_group_test_add(usg2, us8)
        save_usg(usg2)
    # cg2 = cluster_group_test_init(usg2)
    # chr2 = cluster_group_test_run(cg2)

    car1 = Car('car1', 7, '35.958000,120.183563')
    car2 = Car('car2', 7, '35.953553,120.204163')
    car3 = Car('car3', 7, '35.971338,120.175323')
    car4 = Car('car4', 7, '36.166705,120.086060')
    car5 = Car('car5', 7, '35.986896,120.165710')
    car6 = Car('car6', 7, '35.942992,120.174637')
    car7 = Car('car7', 7, '36.268130,120.386090')
    cars = [car1, car2, car3, car4, car5, car6, car7]

    # scheduling_test_car_user_duration(cars, usg1.user_schedules)
    # scheduling_test_car_user_duration(cars, usg2.user_schedules)
    # scheduling_test_user_destination_duration(usg1.user_schedules, AIRPORT_POINT.gps)
    # scheduling_test_user_destination_duration(usg2.user_schedules, AIRPORT_POINT.gps)
    import time

    start = time.clock()
    scheduling_test_run(cars, 'line1', '2019-06-11', '08:00:00', AIRPORT_POINT.gps)
    # [[['us5', 'us4'],'car6',(0,1)], [['us1'], 'car3',(0,)], [['us2', 'us3'],'car2', (0,1)]]
    print("Time used:", time.clock() - start)  # 40次地图接口 20.73s
    scheduling_test_run(cars, 'line1', '2019-06-11', '14:00:00', AIRPORT_POINT.gps)
    # [[['us8','us7','us6'],'car5',(0,1,2)]]
    print("Time used:", time.clock() - start)  # 40+15次地图接口 23.54s
