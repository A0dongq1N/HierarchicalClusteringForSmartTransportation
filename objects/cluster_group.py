#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""簇组类，用于有限制条件的层次聚类法"""

__author__ = 'Aodongq1n'

import itertools

import numpy as np

import HCFST.conf as conf
from HCFST.objects.cluster import Cluster


class ClusterGroup:

    def __init__(self, usg):
        self.usg = usg
        self.clusters = []
        for us in usg.user_schedules:
            self.clusters.append(Cluster(us))
        self.duration_matrix = usg.duration_matrix.copy()  # 簇与簇间的距离是对称的

    def __add(self, cluster):
        """
        簇组（clusters）增加新簇，duration_matrix需扩充对应行列，扩充方法如下： \n
        a = np.array([[1]]) \n
        b = np.array([[2]]) \n
        c = np.r_[a, b] \n
        d = np.array([[3, 4]]) \n
        e = np.c_[c, d.T] --> array([[1, 3],\[2, 4]]) \n
        :param cluster: 新簇
        """
        r, c = [], []
        for ct in self.clusters:
            du = self.__duration(cluster, ct)  # 簇与簇间的距离是对称的
            r.append(du)
            c.append(du)
        if len(r) != 0:
            self.duration_matrix = np.r_[self.duration_matrix, np.array([r])]
        c.append(conf.DURATION_INFINITE)
        if len(c) == 1:
            self.duration_matrix = np.array([c])
        else:
            self.duration_matrix = np.c_[self.duration_matrix, np.array([c]).T]

        self.clusters.append(cluster)

    # def __remove(self, cluster):
    #     """
    #     合并簇后删除旧簇，簇组（clusters）删除该簇，duration_matrix删除对应行列 \n
    #     :param cluster: 待删除簇
    #     """
    #     remove_index = -1
    #     for i in range(len(self.clusters)):
    #         if self.clusters[i].ct_id == cluster.ct_id:
    #             remove_index = i
    #             self.duration_matrix = np.delete(self.duration_matrix, remove_index, 0)
    #             self.duration_matrix = np.delete(self.duration_matrix, remove_index, 1)
    #             break
    #     if remove_index != -1:
    #         del self.clusters[remove_index]

    def __delete(self, index):
        """
        合并后根据索引删除旧簇，簇组（clusters）删除该簇，duration_matrix删除对应行列 \n
        :param index: 待删除簇对应索引
        """
        if 0 <= index < len(self.clusters):
            self.duration_matrix = np.delete(self.duration_matrix, index, 0)
            self.duration_matrix = np.delete(self.duration_matrix, index, 1)
            del self.clusters[index]

    def __duration(self, cluster1, cluster2):  # 若行程时间是conf.MAX_PICK_UP_DURATION，表示该两簇合并不满足限制条件
        if cluster1.ticket_count + cluster2.ticket_count > conf.MAX_TICKET_COUNT:  # 限制1. 两个簇乘客总人数要<=5
            return conf.DURATION_INFINITE
        min_duration = conf.DURATION_INFINITE
        user_schedules = cluster1.user_schedules.copy()
        user_schedules.extend(cluster2.user_schedules)
        for p in itertools.permutations(range(len(user_schedules))):  # 全排列，遍历所有行程顺序
            duration = 0
            for i in range(len(p) - 1):
                a = user_schedules[p[i]].index
                b = user_schedules[p[i + 1]].index
                duration += self.usg.duration_matrix[a][b]
            if duration < min_duration:
                min_duration = duration
        if min_duration <= conf.MAX_PICK_UP_DURATION:  # 限制2. 簇内从第一个点到最后一个点的行程总时长 <= 接客最大行程时间
            return min_duration - cluster1.total_duration - cluster2.total_duration
        return conf.DURATION_INFINITE

    def __find_best_cluster_pair(self):
        """
        :return: 距离最近的且满足限制条件（在计算距离时已加入限制条件信息）的簇对对应索引，没有满足条件的簇对时返回None
        """
        if self.duration_matrix.size == 0:
            return None
        i = np.unravel_index(np.argmin(self.duration_matrix), self.duration_matrix.shape)
        return i if self.duration_matrix[i] <= conf.MAX_PICK_UP_DURATION else None
        # return i if self.duration_matrix[i] <= conf.MAX_PICK_UP_DURATION- 等待时间*接客次数 else None

    def __concat_cluster_pair(self, index1, index2):
        cluster1 = self.clusters[index1]
        cluster2 = self.clusters[index2]
        # 合并成新簇
        new_cluster = cluster1
        new_cluster.ct_id += '\t' + cluster2.ct_id
        new_cluster.user_schedules.extend(cluster2.user_schedules)
        new_cluster.total_duration += cluster2.total_duration + self.duration_matrix[index1][index2]
        new_cluster.ticket_count += cluster2.ticket_count
        # 删除旧簇
        self.__delete(index1)
        if index2 > index1:
            index2 -= 1
        self.__delete(index2)
        # 判断新簇乘客人数是否满conf.MAX_TICKET_COUNT人，未满需将新簇加入到簇组中
        if new_cluster.ticket_count < conf.MAX_TICKET_COUNT:
            self.__add(new_cluster)
            return None
        return new_cluster

    def run(self):
        result_clusters = []  # 拼车订单队列，结果中每个簇就是一个拼车订单
        while True:  # python中None视为False
            i = self.__find_best_cluster_pair()
            if not i:
                break
            cluster = self.__concat_cluster_pair(i[0], i[1])
            if cluster:
                result_clusters.append(cluster)
        result_clusters.extend(self.clusters)
        return result_clusters
