#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""地图点类，包含位置和经纬度"""

__author__ = 'Aodongq1n'


class Point:
    def __init__(self, address, gps):
        """
        :param address: 位置，形如："南山区深南大道10000号"
        :param gps: 经纬度，形如:"23.3243,113.3224"，统一纬度在前
        """
        self.address = address
        self.gps = gps
