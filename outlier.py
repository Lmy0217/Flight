#coding=utf-8

import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
import json
from tkinter import scrolledtext


class Outlier(object):

    def __init__(self, path='data.json'):
        # 数据文件路径
        self.path = path
        # 分析数据
        self.data = self._proccess(self._load(self.path))

    # 加载数据文件
    def _load(self, path):
        with open(path, 'r') as json_file:
            data = json.load(json_file)
        return data

    # 数据预处理
    def _proccess(self, data):
        d = []
        # 数据备份到dimage
        dimage = []
        for c, city in zip(data.keys(), data.values()):
            for da, date in zip(city.keys(), city.values()):
                for flight in date:
                    d += [flight[1:]]
                    dh = int(math.floor(flight[2] / 60))
                    dm = flight[2] % 60
                    ah = int(math.floor((flight[2] + flight[3]) / 60))
                    ah = ah if ah < 24 else ah - 24
                    am = (flight[2] + flight[3]) % 60
                    dh = str(dh).zfill(2)
                    dm = str(dm).zfill(2)
                    ah = str(ah).zfill(2)
                    am = str(am).zfill(2)
                    dimage += [[c, flight[0], da + ' ' + dh + ':' + dm, da + ' ' + ah + ':' + am, flight[1]]]
        self.dataimage = dimage

        return np.array(d)

    def _extreme(self, fig, scr, data, number=5):
        kmeans = KMeans(n_clusters=1)
        # kmean聚类
        kmeans.fit(data)
        if fig is None:
            fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_title("Extreme Analytics")
        ax.scatter(data[:, 1], data[:, 2], data[:, 0], label='Points')
        # 簇心
        ax.scatter(kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:, 2], kmeans.cluster_centers_[:, 0],
                   label='Centroid', color='r')
        ax.legend()
        distances = kmeans.transform(data)
        # 按照到簇心距离排序
        sorted_idx = np.argsort(distances.ravel())[::-1][:number]
        out = []
        for i in range(len(sorted_idx)):
            print(self.dataimage[sorted_idx[i]])
            out.append(self.dataimage[sorted_idx[i]])
            if isinstance(scr, scrolledtext.ScrolledText):
                scr.insert('end', str(self.dataimage[sorted_idx[i]]) + '\n')
        if isinstance(scr, scrolledtext.ScrolledText):
            scr.insert('end', '\n')
        # 异常值
        ax.scatter(data[sorted_idx][:, 1], data[sorted_idx][:, 2], data[sorted_idx][:, 0],
                   label='Extreme Value', edgecolors='g', facecolors='none', s=100)
        ax.legend(loc='best')
        if scr is None:
            plt.show()
        return out

    def extreme(self, fig=None, scr=None, number=5):
        return self._extreme(fig, scr, self.data, number)


if __name__ == "__main__":

    outlier = Outlier('2018-05-23.json')
    outlier.extreme(number=5)
