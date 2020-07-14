#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""簇类，一个簇包含一个或多个用户行程"""

__author__ = 'Aodongq1n'


class Cluster:
    def __init__(self, user_schedule):
        self.ct_id = user_schedule.us_id
        self.user_schedules = [user_schedule]
        self.total_duration = 0
        self.ticket_count = user_schedule.ticket_count
