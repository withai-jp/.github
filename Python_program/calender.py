# -*- coding:utf-8 -*-


import tkinter as tk
import calendar
import datetime
import sqlite3

"""
最初データのみわけようと思ったが意味なかったので統合済み
class Calendar_data():

    def __init__(self):
        today = datetime.datetime.now()
        self.tdy_year = today.year
        self.tdy_month = today.month

    def now_calender(self):
        cal = calendar.Calendar()
        days = cal.monthdayscalendar(self.tdy_year, self.tdy_month)

        days_dict = {}
        for i in range (len(days)):
            dict_key = "week" + str(i)
            days_dict[dict_key]=days[i]

        return days_dict
"""


class C_frame():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("スケジュールカレンダー")
        self.root.geometry("320x460")
        todays = datetime.datetime.now()
        self.current_y = todays.year
        self.current_m = todays.month
        self.sq = Sql_sche()

    def now_calender(self):
        #カレンダーモジュールから指定年月のカレンダーデータを取得
        cal = calendar.Calendar()
        days = cal.monthdayscalendar(self.current_y, self.current_m)

        days_dict = {}
        for i in range (len(days)):
            dict_key = "week" + str(i)
            days_dict[dict_key]=days[i]

        return days_dict

    def plus_m(self):
        #>>ボタンで月をあげる処理と再描画の指示
        self.current_m += 1
        if self.current_m == 13:
            self.current_m = 1
            self.current_y += 1
        days_dict = self.now_calender()
        self.c_defo()
        self.c_date(days_dict, "reset")

    def minus_m(self):
        #<<ボタンで月を下げる処理と再描画の指示
        self.current_m -= 1
        if self.current_m == 0:
            self.current_m = 12
            self.current_y -= 1
        days_dict = self.now_calender()
        self.c_defo()
        self.c_date(days_dict, "reset")


    def c_defo(self):
        #年月及び週の描画（c_dateと分ける意味あんまなかったかも)

        frame_ym = tk.Frame(self.root)
        min_m = tk.Button(frame_ym, relief = "flat", text = "<<",
            font = ("",16), command = self.minus_m)
        min_m.pack(side = "left")
        pls_m = tk.Button(frame_ym, relief = "flat", text = ">>",
            font = ("",16), command = self.plus_m)
        pls_m.pack(side = "right")
        year_label = tk.Label(frame_ym, text = self.current_y, font = ("",16))
        year_label.pack(side = "left")
        month_label = tk.Label(frame_ym, text = self.current_m, font = ("",16))
        month_label.pack(side = "left")
        frame_ym.grid(row = 0, column = 0)

        week_name = {
            0 : "月", 1 : "火", 2 : "水", 3 : "木",
            4 : "金", 5 : "土", 6 : "日"
        }
        frame_week = tk.LabelFrame(self.root)
        for i in range(0, 7):
            button0 = tk.Button(frame_week, relief = "flat",
                width = 5, state = "disabled", text = week_name[i])
            button0.pack(side = "left")
        frame_week.grid(row = 1, column = 0)


    def c_date(self, days_dict, reset = None):
        #日の描画、日ボタンにはコマンドがあり、entrydataにイベントとボタンのテキストを渡す
        if reset:
            self.frame.destroy()
            #フレームごとボタンを初期化。reset定義せずとりあえず初期化でもよかったかも

        self.frame = tk.LabelFrame(self.root, bd = 3, relief = "ridge")

        for i in range(len(days_dict)):
            dict_key = "week" + str(i)
            week_days = days_dict[dict_key]

            for j in range(0,7):
                day = week_days[j]
                if day != 0 and j == 5:
                    button1 = tk.Button(self.frame, relief = "groove", bg = "#b4c5ff",
                        activebackground = "#ccc", width = 5, text = day)
                    button1.bind("<1>", self.entrydata)
                elif day != 0 and j == 6:
                    button1 = tk.Button(self.frame, relief = "groove", bg = "#f6c5d7",
                        activebackground = "#ccc", width = 5, text = day)
                    button1.bind("<1>", self.entrydata)
                elif day != 0:
                    button1 = tk.Button(self.frame, relief = "groove",
                        activebackground = "#ccc", width = 5, text = day)
                    button1.bind("<1>", self.entrydata)

                else:
                    continue
                button1.grid(row = i, column = j)
        self.frame.grid(row = 2, column = 0)


    def entrydata(self, event = None):
        #日付クリックで代入されるエントリーボックス
        frame2 = tk.LabelFrame(self.root, text = "予定日をクリックしてください")
        self.entry2 = tk.Entry(frame2, font = ("", 14), justify = "center", width = 30)
        if event:
            y = str(self.current_y)
            m = str(self.current_m)
            d = event.widget["text"]
            ymd = "{}-{}-{}".format(y,m,d)
            self.entry2.insert(tk.END, ymd)
        self.entry2.pack(side = "left")
        frame2.grid(row = 4 , column = 0)


    def entry(self):
        #ここもあとからどんどん追加したボタン郡のため、定義まとめてOK
        frame = tk.LabelFrame(self.root, text = "スケジュールを入力してください")
        self.entry1 = tk.Entry(frame, font = ("", 14), justify = "center", width = 30)
        self.entry1.pack(side = "left")
        frame.grid(row = 3 , column = 0)

        frame2 = tk.LabelFrame(self.root, text = "")
        get_button = tk.Button(frame2, text = "登録",font = ("", 12),
            command = self.touroku)
        get_button.pack(side = "left")

        """
        testprint = tk.Button(frame2, text = "testprint",
            font = ("", 12), command = self.sq.test_nowdata)
        testprint.pack(side = "left")
        """

        reset = tk.Button(frame2, text = "resetDatabase",
            font = ("", 12), command = self.sq.reset_table)
        reset.pack(side = "left")

        printb =  tk.Button(frame2, text = "予定を表示", font = ("", 12))
        printb.bind("<1>", self.textbox)
        printb.pack(side = "left")

        frame2.grid(row = 5 , column = 0)

    def textbox(self, event = None):
        #登録されたデータを表示するテキストボックス
        textbox = tk.Text(self.root, height = 10, width = 40)
        if event:
            datas = self.sq.return_all()
            for data in datas:
                row = float(data[0])
                text = "{}の予定は「{}」\n".format(data[1], data[2])
                textbox.insert(str(row), text)
        textbox.grid(row = 9, column= 0)

    def touroku(self):
        #登録ボタンの処理
        sche_data = str(self.entry1.get())
        date_data = str(self.entry2.get())
        datalist = [date_data, sche_data]
        self.sq.add_data(datalist)


    def main(self):
        self.c_defo()
        self.c_date(self.now_calender())
        self.entrydata()
        self.entry()
        self.textbox()
        self.root.mainloop()



class Sql_sche():
    #データベース関係を先に作ったやつ
    def __init__(self):
        sqlite_path = "db/sche.sqlite"
        self.connection = sqlite3.connect(sqlite_path)
        self.cursor = self.connection.cursor()


    def reset_table(self):
        self.cursor.execute("DROP TABLE sche")
        self.cursor.execute("VACUUM")
        self.cursor.execute("CREATE TABLE sche(id INTEGER PRIMARY KEY, date TEXT, task TEXT)")

    def add_data(self, data):
        self.cursor.execute("INSERT INTO sche(date, task) VALUES(?, ?)", data)
        # なんかクォーテーションがかぶって認識しないので、シングルと混ぜて使うこと
        self.connection.commit()

    def test_nowdata(self):
        self.cursor.execute('SELECT * FROM sche')
        res = self.cursor.fetchall()
        print(res)

    def return_all(self):
        self.cursor.execute('SELECT * FROM sche')
        res = self.cursor.fetchall()
        return res

    def close(self):
        self.connection.close()

"""
SQLとカレンダーで別々に作って
あとで纏めとようと作ったら
定義ばっかになった失敗例
結局定義したものをまとめてmain()で呼び出してる
カレンダー側はもうちょっと普通に書いてよかった
"""


cf = C_frame()

cf.main()
