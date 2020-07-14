#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""用户行程类，一个对象代表一个用户行程"""

__author__ = 'Aodongq1n'

from HCFST.tools.tencent_direction import driving_direction
import HCFST.conf as conf


class UserSchedule:
    def __init__(self, us_id, line_id, origin, destination, earliest_start_unixtime, latest_start_unixtime,
                 ticket_count):
        """
        :index: 用户行程组内索引，表示该行程在所属行程组中的位置
        :param us_id: 用户行程id
        :param line_id: 线路ID
        :param origin: 用户的起始点，Point对象
        :param destination: 用户的目的地，Point对象
        :param earliest_start_unixtime: 最早出发时间戳
        :param latest_start_unixtime: 最迟出发时间戳
        :param ticket_count: 所需座位数
        """
        self.index = -1
        self.us_id = us_id
        self.line_id = line_id
        self.origin = origin
        self.destination = destination
        self.earliest_start_time = earliest_start_unixtime
        self.latest_start_time = latest_start_unixtime
        self.ticket_count = ticket_count

    def change_index(self, index):
        self.index = index

    def duration(self, us):
        """
        计算起始点到另一用户行程起始点的行程时间\n
        :param us: 另一用户行程
        :return: 行程时间
        """
        if self.ticket_count + us.ticket_count > conf.MAX_TICKET_COUNT:
            return conf.DURATION_INFINITE
        _, duration, _ = driving_direction(self.origin.gps, us.origin.gps, self.earliest_start_time)
        return duration
