#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""车辆类"""

__author__ = 'Aodongq1n'


class Car:
    def __init__(self, car_id, seat_count, location):
        """
        :param car_id: 车辆ID
        :param seat_count: 座位数
        :param location: 车辆当前位置gps
        """
        self.car_id = car_id
        self.seat_count = seat_count
        self.gps = location
