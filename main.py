#coding=utf-8

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox as mBox
from tkinter import filedialog

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import datetime
import threading

import flight
import outlier
import analytics


# 标题
win = tk.Tk()
win.title("机票数据爬取分析预测")
win.resizable(0, 0)


# 三个页面
tabControl = ttk.Notebook(win)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text='爬取')
tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text='分析')
tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text='预测')
tabControl.pack(expand=1, fill="both")


# 参数框
monty = ttk.LabelFrame(tab1, text='')
monty.grid(column=0, row=0, padx=8, pady=4)
labelsFrame = ttk.LabelFrame(monty, text=' 参数 ')
labelsFrame.grid(column=0, row=0)


# 城市标签
ttk.Label(labelsFrame, text="城市:").grid(column=0, row=0, sticky='W')

# 城市输入框
city = tk.Text(labelsFrame, width=20, height=10)
city.insert(tk.END, "'SHA', 'SIA', 'BJS', 'CAN', 'SZX', 'CTU', 'HGH', 'WUH', 'CKG', 'TAO', 'CSX', 'NKG', 'XMN', 'KMG', 'DLC', 'TSN', 'CGO', 'SYX', 'TNA', 'FOC'")
city.grid(column=1, row=0, sticky='W')


# 起始日期标签
ttk.Label(labelsFrame, text="起始日期:").grid(column=0, row=1, sticky='W')

# 起始日期输入框
date1 = tk.StringVar()
da_days = datetime.datetime.now() + datetime.timedelta(days=1)
date1.set(da_days.strftime('%Y-%m-%d'))
date1Entered = ttk.Entry(labelsFrame, textvariable=date1)
date1Entered.grid(column=1, row=1, sticky='W')


# 截止日期标签
ttk.Label(labelsFrame, text="截止日期:").grid(column=0, row=2, sticky='W')

# 截止日期输入框
date2 = tk.StringVar()
da_days2 = datetime.datetime.now() + datetime.timedelta(days=1)
date2.set(da_days2.strftime('%Y-%m-%d'))
date2Entered = ttk.Entry(labelsFrame, textvariable=date2)
date2Entered.grid(column=1, row=2, sticky='W')


# Log框
scrolW = 91;
scrolH = 37;
scr = scrolledtext.ScrolledText(monty, width=scrolW, height=scrolH, wrap=tk.WORD)
scr.grid(column=3, row=0, sticky='WE', rowspan=5)


# 爬取数据
def spider_flight():
    spider_flight.flight = flight.spider(city.get("0.0", "end"), date1.get(), date2.get(), scr)


spider_flight.flight = None


def run_spider_flight():
    scr.insert(tk.END, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n爬取数据：\n城市：'
               + str(city.get("0.0", "end")) + '\n日期：' + str(date1.get()) + ' 至 ' + str(date2.get()) + '\n\n')
    t = threading.Thread(target=spider_flight)
    t.start()


# 爬取标签
spider = ttk.Button(labelsFrame, text="爬取", width=10, command=run_spider_flight)
spider.grid(column=0, row=4, sticky='W')


# 保存文件
def save_file():
    if spider_flight.flight is not None:
        fname = tk.filedialog.asksaveasfilename(filetypes=[("JSON", ".json")], defaultextension='.json')
        if fname is not '':
            spider_flight.flight.save(fname)
        scr.insert(tk.END, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n数据保存到 ' + fname + '\n\n')
    else:
        mBox.showwarning('Python Message Warning Box', '请先爬取数据！')


# 保存标签
save = ttk.Button(labelsFrame, text="保存", width=10, command=save_file)
save.grid(column=1, row=4, sticky='E')


for child in labelsFrame.winfo_children():
    child.grid_configure(padx=8, pady=4)
for child in monty.winfo_children():
    child.grid_configure(padx=3, pady=1)


# 参数框
monty2 = ttk.LabelFrame(tab2, text='')
monty2.grid(column=0, row=0, padx=8, pady=4)
labelsFrame2 = ttk.LabelFrame(monty2, text=' 参数 ')
labelsFrame2.grid(column=0, row=0)


# Log框
scrolW = 34;
scrolH = 25;
scr2 = scrolledtext.ScrolledText(monty2, width=scrolW, height=scrolH, wrap=tk.WORD)
scr2.grid(column=0, row=3, sticky='WE')


# 数据标签
ttk.Label(labelsFrame2, text="数据:").grid(column=0, row=0, sticky='W')


# 打开文件
def data_file():
    fname = tk.filedialog.askopenfilename(filetypes=[("JSON", ".json")], defaultextension='.json')
    if fname is not '':
        data_file.outlier = outlier.Outlier(fname)
    scr2.insert(tk.END, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n打开文件 ' + fname + '\n\n')


data_file.outlier = None


# 打开文件按钮
data = ttk.Button(labelsFrame2, text="打开文件", width=10, command=data_file)
data.grid(column=1, row=0, sticky='E')


# 异常数标签
ttk.Label(labelsFrame2, text="异常数:").grid(column=0, row=1, sticky='W')

# 异常数输入框
diff = tk.IntVar()
diff.set(5)
diffEntered = ttk.Entry(labelsFrame2, textvariable=diff)
diffEntered.grid(column=1, row=1, sticky='W')


# 图框
def drawdiff():
    try:
        num_diff = int(diffEntered.get())
    except:
        num_diff = 5
        diffEntered.delete(0, tk.END)
        diffEntered.insert(0, 5)

    drawdiff.f.clf()
    drawdiff.out = data_file.outlier.extreme(drawdiff.f, scr2, num_diff)
    drawdiff.canvas.show()


drawdiff.out = None
drawdiff.f = plt.figure()
drawdiff.canvas = FigureCanvasTkAgg(drawdiff.f, master=monty2)
drawdiff.canvas.show()
drawdiff.canvas.get_tk_widget().grid(column=1, row=0, rowspan=4)


def run_drawdiff():
    if data_file.outlier is not None:
        scr2.insert(tk.END, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n分析数据（设定 '
                    + str(diffEntered.get()) + ' 个异常值）...\n\n异常值：\n')
        t = threading.Thread(target=drawdiff)
        t.start()
    else:
        mBox.showwarning('Python Message Warning Box', '请先打开文件！')


# 分析按钮
da = ttk.Button(labelsFrame2, text="分析", width=10, command=run_drawdiff)
da.grid(column=0, row=2, sticky='W')


# 保存文件
def save_file2():
    if drawdiff.out is not None:
        fname = tk.filedialog.asksaveasfilename(filetypes=[("JSON", ".json")], defaultextension='.json')
        if fname is not '':
            with open(fname, 'w') as f1:
                f1.write(str(drawdiff.out))
        scr2.insert(tk.END, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n异常值保存到 ' + fname + '\n\n')
    else:
        mBox.showwarning('Python Message Warning Box', '请先分析数据！')


# 保存按钮
save2 = ttk.Button(labelsFrame2, text="保存", width=10, command=save_file2)
save2.grid(column=1, row=2, sticky='E')


for child in labelsFrame2.winfo_children():
    child.grid_configure(padx=8, pady=4)
for child in monty2.winfo_children():
    child.grid_configure(padx=8, pady=4)


# 参数框
monty3 = ttk.LabelFrame(tab3, text='')
monty3.grid(column=0, row=0, padx=8, pady=4)
labelsFrame3 = ttk.LabelFrame(monty3, text=' 参数 ')
labelsFrame3.grid(column=0, row=0)


# Log框
scrolW = 34;
scrolH = 25;
scr3 = scrolledtext.ScrolledText(monty3, width=scrolW, height=scrolH, wrap=tk.WORD)
scr3.grid(column=0, row=3, sticky='WE')


# 数据标签
ttk.Label(labelsFrame3, text="数据:").grid(column=0, row=0, sticky='W')


# 打开文件
def data_file2():
    fname = tk.filedialog.askopenfilename(filetypes=[("JSON", ".json")], defaultextension='.json')
    if fname is not '':
        data_file2.analytics = analytics.Analytics(fname)
    scr3.insert(tk.END, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n打开文件 ' + fname + '\n\n')


data_file2.analytics = None


# 打开文件按钮
data2 = ttk.Button(labelsFrame3, text="打开文件", width=10, command=data_file2)
data2.grid(column=1, row=0, sticky='E')


# 预测天数标签
ttk.Label(labelsFrame3, text="预测天数:").grid(column=0, row=1, sticky='W')

# 预测天数输入框
days = tk.IntVar()
days.set(30)
daysEntered = ttk.Entry(labelsFrame3, textvariable=days)
daysEntered.grid(column=1, row=1, sticky='W')


# 图框
def drawpredict():
    try:
        num_day = int(daysEntered.get())
    except:
        num_day = 30
        daysEntered.delete(0, tk.END)
        daysEntered.insert(0, 30)

        # 清空图像，以使得前后两次绘制的图像不会重叠
    drawpredict.f.clf()
    drawpredict.out = data_file2.analytics.predict(num_day, scr3)
    drawpredict.canvas.show()


drawpredict.out = None
drawpredict.f = plt.figure()
drawpredict.canvas = FigureCanvasTkAgg(drawpredict.f, master=monty3)
drawpredict.canvas.show()
drawpredict.canvas.get_tk_widget().grid(column=1, row=0, rowspan=4)


def run_drawpredict():
    if data_file2.analytics is not None:
        scr3.insert(tk.END, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n分析数据（设定预测 '
                    + str(daysEntered.get()) + ' 天）...\n\n训练过程：\n轮次/总轮次 [损失]\n')
        t = threading.Thread(target=drawpredict)
        t.start()
    else:
        mBox.showwarning('Python Message Warning Box', '请先打开文件！')


# 预测按钮
pr = ttk.Button(labelsFrame3, text="预测", width=10, command=run_drawpredict)
pr.grid(column=0, row=2, sticky='W')


# 保存文件
def save_file3():
    if drawpredict.out is not None:
        fname = tk.filedialog.asksaveasfilename(filetypes=[("JSON", ".json")], defaultextension='.json')
        with open(fname, 'w') as f1:  # 打开文件
            f1.write(str(drawpredict.out))
        scr3.insert(tk.END, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n训练过程和预测结果保存到 ' + fname + '\n\n')
    else:
        mBox.showwarning('Python Message Warning Box', '请先预测数据！')


# 保存按钮
save = ttk.Button(labelsFrame3, text="保存", width=10, command=save_file3)
save.grid(column=1, row=2, sticky='E')


for child in labelsFrame3.winfo_children():
    child.grid_configure(padx=8, pady=4)
for child in monty3.winfo_children():
    child.grid_configure(padx=8, pady=4)


if __name__ == "__main__":
    win.mainloop()
