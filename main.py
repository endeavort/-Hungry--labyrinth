import tkinter

# 迷路情報データ
map_data = [
    [0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0],
    [0, 2, 3, 3, 2, 1, 1, 2, 3, 3, 2, 0],
    [0, 3, 0, 0, 3, 3, 3, 3, 0, 0, 3, 0],
    [0, 3, 1, 1, 3, 0, 0, 3, 1, 1, 3, 0],
    [0, 3, 2, 2, 3, 0, 0, 3, 2, 2, 3, 0],
    [0, 3, 0, 0, 3, 1, 1, 3, 0, 0, 3, 0],
    [0, 3, 1, 1, 3, 3, 3, 3, 1, 1, 3, 0],
    [0, 2, 3, 3, 2, 0, 0, 2, 3, 3, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


# 迷路を描く関数
def draw_screen():
    for y in range(9):
        for x in range(12):
            canvas.create_image(x * 60 + 30, y * 60 + 30, image=img_bg[map_data[y][x]])


root = tkinter.Tk()  # ウィンドウの作成
root.title("はらはら　ペンギン　ラビリンス")  # タイトル
root.resizable(False, False)  # ウィンドウサイズ変更不可
canvas = tkinter.Canvas(width=720, height=540)  # キャンバスの作成
canvas.pack()  # キャンバスの配置

img_bg = [
    tkinter.PhotoImage(file="images/chip00.png"),
    tkinter.PhotoImage(file="images/chip01.png"),
    tkinter.PhotoImage(file="images/chip02.png"),
    tkinter.PhotoImage(file="images/chip03.png"),
]

draw_screen()
root.mainloop()
