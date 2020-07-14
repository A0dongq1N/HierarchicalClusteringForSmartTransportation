#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""腾讯地图路径规划API, departure_time（unix时间戳），distance（米）, duration（分钟）"""

__author__ = 'Aodongq1n'

import requests
import HCFST.conf as conf

def driving_direction(origin_gps, destination_gps, departure_time=None, key=conf.TENCENT_MAP_KEY):
    url = """http://apis.map.qq.com/ws/distance/v1/matrix/?mode=driving&from=%s&to=%s&output=json&callback=cb&key=%s"""
    url = url % (origin_gps, destination_gps, key)
    if departure_time:
        url += '&departure_time=%d' % departure_time
    result = requests.get(url).json()
    # if result['status'] == 0:
    #     distance = result['result']['routes'][0]['distance']  # unit: meter
    #     duration = result['result']['routes'][0]['duration']  # unit: minute
    # else:
    #     distance = -1
    #     duration = -1
    # return distance, duration, result
    print  len(result['result']['rows']) , len(result['result']['rows'][0]['elements']), result['result']['rows'][0]['elements']


if __name__ == '__main__':
    r = driving_direction('39.915285,116.403857', '39.015285,116.803857;'
                                                  '39.115235,116.803857;'
                                                  '39.215245,116.803857;'
                                                  '39.315255,116.803857;'
                                                  '39.415265,116.803857;'
                                                  '39.515275,116.803857;'
                                                  '39.615295,116.803857;'
                                                  '39.715185,116.803857;'
                                                  '39.815285,116.803857;'
                                                  '39.915385,116.803857;'
                                                  '31.915485,116.803857;'
                                                  '32.915585,116.803857;'
                                                  '33.915685,116.803857;'
                                                  '34.915785,116.803857;'
                                                  '35.915885,116.803857;'
                                                  '36.915985,116.803857;'
                                                  '37.914285,116.803857;'
                                                  '38.915285,116.803857;'
                                                  '38.921285,116.803857;'
                                                  '38.932285,116.803857;'
                                                  '38.943285,116.803857;'
                                                  '38.956285,116.803857;'
                                                  '38.967285,116.803857;'
                                                  '38.978285,116.803857;'
                                                  '38.989285,116.803857;'
                                                  '38.990285,116.803857;'
                                                  '38.815285,116.803857;'
                                                  '38.725285,116.803857;'
                                                  '38.635285,116.803857;'
                                                  '38.545285,116.803857;'
                                                  '38.455285,116.803857;'
                                                  '38.365285,116.803857;'
                                                  '38.275285,116.803857;'
                                                  '38.9185285,116.803857;'
                                                  '38.115285,116.803857;'
                                                  '39.905285,116.803857;'
                                                  '39.835285,116.803857;'
                                                  '39.845285,116.803857;'
                                                  '39.855285,116.803857;'
                                                  '39.865285,116.803857;'
                                                  '39.875285,116.803857;'
                                                  '39.885285,116.803857;'
                                                  '39.895285,116.803857;'
                                                  '39.915285,116.803857;'
                                                  '39.415285,116.803857;'
                                                  '39.315285,116.803857;'
                                                  '39.215285,116.803857', None)  # 5/22 11：21 39295m, 59min
    print(r)
    # r = driving_direction('39.915285,116.403857', '39.915285,116.803857', 1558569660)  # 5/23 8：1 39246m, 51min
    # print(r)
    # r = driving_direction('39.915285,116.403857', '39.915285,116.803857', 1558581660)  # 5/23 11：21 39295m, 52min
    # print(r)
