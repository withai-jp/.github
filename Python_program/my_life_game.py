# -*- coding:utf-8 -*-

from random import randint
import tkinter as tk

# 以下3つの値は変更すれば、ゲームの描画サイズを変えれます。
CELLSIZE = 20
ROWS = 30
COLS = 40

STOP_FIG = True

root = tk.Tk()
root.title("LifeGame")
cv = tk.Canvas(root, width = CELLSIZE * COLS, height = CELLSIZE * ROWS)
cv.pack()

data = []
for y in range(0, ROWS):
    data.append([(randint(0, 9) == 0) for x in range(0, COLS)])



def random_cell():
    data.clear()
    for y in range(0, ROWS):
        data.append([(randint(0, 9) == 0) for x in range(0, COLS)])
    draw_cell()

def clear_cell():
    data.clear()
    for y in range(0, ROWS):
        data.append([False for x in range(0, COLS)])
    draw_cell()


# データを元に描画
def draw_cell():
    cv.delete("all")
    for y in range(ROWS):
        y1 = y * CELLSIZE
        y2 = y1 + CELLSIZE
        for x in range(COLS):
            x1 = x * CELLSIZE
            x2 = x1 + CELLSIZE
            tf = data[y][x]

            if tf == 0: continue
            cv.create_rectangle(x1, y1, x2, y2,
                fill = "gray", outline = "black", width = 5)


# ライフゲームの仕様
def count_cell(x, y):

    count = 0
    around = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

    for a in around:
        ax = x + a[1]
        ay = y + a[0]

        # 枠の端は逆側に繋がるように設定
        if ax == -1:
            ax = COLS -1
        elif ax == COLS:
            ax = 0
        if ay == -1:
            ay = ROWS -1
        elif ay == ROWS:
            ay = 0

        if data[ay][ax]:
            count += 1

    if data[y][x]:
        if count == 2 or count == 3:
            return True
        else: return False
    else:
        if count == 3:
            return True
        else: return False


# 次世代のデータを作る
def next_gen():
    global data
    next_data = []
    for y in range(0, ROWS):
        next_data.append([count_cell(x, y) for x in range(0, COLS)])
    data = next_data


# 左クリックでCellを追加
def dragged_l(event):
    nowx = event.x // CELLSIZE
    nowy = event.y // CELLSIZE
    # 範囲外（ボタンウィジェットの行とか)でのエラー回避
    try:
        data[nowy][nowx] = True
        draw_cell()
    except:
        pass

# 右クリックでCellを消去
def dragged_r(event):
    nowx = event.x // CELLSIZE
    nowy = event.y // CELLSIZE
    try:
        data[nowy][nowx] = False
        draw_cell()
    except:
        pass

def gen_start():
    global STOP_FIG
    STOP_FIG = False
    gen_loop()

def gen_loop(looptime = 500):
    if not STOP_FIG:
        next_gen()
        draw_cell()
        root.after(looptime, gen_loop)

def gen_stop():
    global STOP_FIG
    STOP_FIG = True

"""
tkinterのボタンは読み込み時コマンド実行するので
ループするようなWhileやTk.afterループを組み込むと動かない
STOP_FIGの真偽でループの稼働をスイッチ
"""

cv.bind("<ButtonPress-3>", dragged_r)
cv.bind("<ButtonPress-1>", dragged_l)
cv.bind("<B1-Motion>", dragged_l)
cv.bind("<B3-Motion>", dragged_r)

clear_button = tk.Button(root, text = "clear", command = clear_cell)
clear_button.pack(side = "right")
random_button = tk.Button(root, text = "random", command = random_cell)
random_button.pack(side = "right")
start_button = tk.Button(root, text = "start", command = gen_start)
start_button.pack(side = "right")
stop_button = tk.Button(root, text = "stop", command = gen_stop)
stop_button.pack(side = "right")

draw_cell()
root.mainloop()
