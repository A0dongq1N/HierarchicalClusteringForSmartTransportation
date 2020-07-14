#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""用户行程组类，同一目的地同一拼车时间段的用户行程属于同一用户行程组"""

__author__ = 'Aodongq1n'

import numpy as np
import HCFST.conf as conf


class UserScheduleGroup:
    def __init__(self, usg_id):
        """
        :usg_id: str(线路ID) + str(截止拼车时间戳) 组成usg_id
        :user_schedules: 该用户行程组中的所有用户行程
        :duration_matrix: 行程时间矩阵，矩阵值是该用户行程组中任意两个出发点之间的行程时间，类型为numpy数组
        """
        self.usg_id = usg_id
        self.user_schedules = []
        self.duration_matrix = np.empty((0, 0), int)

    def add(self, user_schedule):
        """
        行程组（user_schedules）增加新行程，duration_matrix需扩充对应行列，扩充方法如下： \n
        a = np.array([[1]]) \n
        b = np.array([[2]]) \n
        c = np.r_[a, b] \n
        d = np.array([[3, 4]]) \n
        e = np.c_[c, d.T] --> array([[1, 3],\[2, 4]]) \n
        :param user_schedule: 新行程
        """
        r, c = [], []
        for us in self.user_schedules:
            r.append(user_schedule.duration(us))
            c.append(us.duration(user_schedule))
        if len(r) != 0:
            self.duration_matrix = np.r_[self.duration_matrix, np.array([r])]
        c.append(conf.DURATION_INFINITE)
        if len(c) == 1:
            self.duration_matrix = np.array([c])
        else:
            self.duration_matrix = np.c_[self.duration_matrix, np.array([c]).T]

        self.user_schedules.append(user_schedule)
        user_schedule.change_index(len(self.user_schedules) - 1)

    def remove(self, us_id):
        """
        用户取消订单，行程组（user_schedules）删除该行程，duration_matrix需删除对应行列，之后行程的index需要-1 \n
        :param us_id: 待删除行程id
        """
        remove_index = -1
        delta_index = 0
        for us in self.user_schedules:
            if us.us_id == us_id:
                remove_index = us.index
                self.duration_matrix = np.delete(self.duration_matrix, remove_index, 0)
                self.duration_matrix = np.delete(self.duration_matrix, remove_index, 1)
                delta_index = -1
                continue
            us.change_index(us.index + delta_index)
        if remove_index != -1:
            del self.user_schedules[remove_index]
