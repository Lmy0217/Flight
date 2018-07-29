#coding=utf-8

import numpy as np
import json
import sys
import math
import matplotlib.pyplot as plt
from tkinter import scrolledtext

from lstm import LstmParam, LstmNetwork


class ToyLossLayer:

    @classmethod
    def loss(self, pred, label):
        return (pred[0] - label) ** 2

    @classmethod
    def bottom_diff(self, pred, label):
        diff = np.zeros_like(pred)
        diff[0] = 2 * (pred[0] - label)
        return diff


class Analytics(object):

    def __init__(self, path):
        # 数据文件路径
        self.path = path
        # 加载数据文件
        self.data = self._proccess(self._load(self.path))
        # 数据文件长度
        self.length = self.data.shape[0]

    def _load(self, path):
        with open(path, 'r') as json_file:
            data = json.load(json_file)
        return data

    # 数据预处理
    def _proccess(self, data):
        d = []
        dimage = []
        for c, city in zip(data.keys(), data.values()):
            for da, date in zip(city.keys(), city.values()):
                sum = 0
                for flight in date:
                    sum += flight[1]
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
                d += [[sum / len(date)]]
        self.dataimage = dimage

        d = np.array(d)
        self.mean = np.mean(d)
        self.std = np.std(d)
        # 数据归一化
        d = (d - self.mean) / self.std

        return d

    def predict(self, num_days, scr=None):
        plt.clf()
        self.data = self.data[:self.length, :]
        r = np.transpose(self.data * self.std + self.mean)[0]
        # 画出原始数据
        plt.plot(range(r.shape[0]), r, 'x-b', label="Points")
        out = self._predict(num_days, scr)
        p = np.transpose(self.data * self.std + self.mean)[0][-num_days - 1:]
        # 画出预测的数据
        plt.plot(range(r.shape[0] - 1, r.shape[0] + num_days), p, 'x-r', label="Predict")
        plt.xlabel('Days')
        plt.ylabel('Prices')
        plt.legend()
        print(out)
        if scr is None:
            plt.show()
        return out

    # 预测
    def _predict(self, num_days, scr):
        # 初始化参数
        np.random.seed(0)
        mem_cell_ct = 100
        x_dim = 10
        lstm_param = LstmParam(mem_cell_ct, x_dim)
        lstm_net = LstmNetwork(lstm_param)
        days = 10
        # 需要预测的值
        y_list = self.data[days:, :]
        # 输入值
        input_val_arr = []
        for d in range(len(y_list)):
            if input_val_arr == []:
                input_val_arr = np.transpose(self.data[d:d+days, :])
            else:
                input_val_arr = np.concatenate((input_val_arr, np.transpose(self.data[d:d+days, :])), 0)

        out = ''
        # 训练1000次
        for cur_iter in range(1000):
            for ind in range(len(y_list)):
                # 训练
                lstm_net.x_list_add(input_val_arr[ind, :])

            # 计算损失
            loss = lstm_net.y_list_is(y_list, ToyLossLayer)
            # 反向误差
            lstm_param.apply_diff(lr=0.01)
            lstm_net.x_list_clear()
            if (cur_iter + 1) % 50 == 0:
                out += str(cur_iter + 1) + '/' + str(1000) + ' ' + str(loss) + '\n'
                if isinstance(scr, scrolledtext.ScrolledText):
                    scr.insert('end', str(cur_iter + 1) + '/' + str(1000) + ' ' + str(loss) + '\n')
        out += '\n'
        if isinstance(scr, scrolledtext.ScrolledText):
            scr.insert('end', '\n')

        # 查找最低的票价
        min_value = sys.maxint
        min_index = self.length
        for i in range(num_days):
            lstm_net.x_list_add(np.transpose(self.data[-days:, :])[0])
            self.data = np.append(self.data, [[lstm_net.lstm_node_list[0].state.h[0]]], 0)
            out += '预测第 ' + str(self.length + i + 1) + ' 天票价为 ' + str(lstm_net.lstm_node_list[0].state.h[0] * self.std + self.mean) + '\n'
            if lstm_net.lstm_node_list[0].state.h[0] < min_value:
                min_value = lstm_net.lstm_node_list[0].state.h[0]
                min_index = self.length + i + 1
            lstm_net.x_list_clear()
        out += '\n预测在第 ' + str(min_index) + ' 天取得最低票价 ' + str(min_value * self.std + self.mean) + '\n'
        if isinstance(scr, scrolledtext.ScrolledText):
            scr.insert('end', '预测在第 ' + str(min_index) + ' 天取得最低票价 ' + str(min_value * self.std + self.mean) + '\n\n')

        return out


if __name__ == "__main__":

    analytics = Analytics('out.json')
    analytics.predict(30)
