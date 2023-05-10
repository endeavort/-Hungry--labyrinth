import tkinter

# キー入力
key = ""
koff = False


# キーを押したときの処理
def key_down(e):
    global key, koff
    key = e.keysym
    koff = False


# キーを離したときの処理
def key_up(e):
    global koff
    koff = True


DIR = [0, 1, 2, 3]  # 向き[上,下,左,右]
ANIMATION = [0, 1, 0, 2]  # アニメーション番号

tmr = 0  # タイマー
score = 0  # スコア

# プレイヤー
pl_posx = 90  # 位置ｘ
pl_posy = 90  # 位置ｙ
pl_d = 1  # 向き
pl_a = 0  # 画像番号

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


# 描画処理
def draw_screen():
    canvas.delete("SCREEN")  # 全ての画像を削除
    # マップ描画
    for y in range(9):
        for x in range(12):
            canvas.create_image(
                x * 60 + 30, y * 60 + 30, image=img_bg[map_data[y][x]], tag="SCREEN"
            )
    # プレイヤー描画
    canvas.create_image(pl_posx, pl_posy, image=img_pl[pl_a], tag="SCREEN")
    draw_txt("SCORE " + str(score), 200, 30, 30, "white")


# 文字描画処理
def draw_txt(txt, x, y, siz, col):
    fnt = ("Times New Roman", siz, "bold")
    canvas.create_text(x + 2, y + 2, text=txt, fill="black", font=fnt, tag="SCREEN")
    canvas.create_text(x, y, text=txt, fill=col, font=fnt, tag="SCREEN")


# 壁を調べる処理
def check_wall(cx, cy, di, dot=20):
    chk = False
    # 上向きの時
    if di == DIR[0]:
        mx = int((cx - 30) / 60)
        my = int((cy - 30 - dot) / 60)
        if map_data[my][mx] <= 1:  # 左上
            chk = True
        mx = int(((cx + 29) / 60))
        if map_data[my][mx] <= 1:  # 右上
            chk = True
    # 下向きの時
    if di == DIR[1]:
        mx = int((cx - 30) / 60)
        my = int((cy + 29 + dot) / 60)
        if map_data[my][mx] <= 1:  # 左下
            chk = True
        mx = int(((cx + 29) / 60))
        if map_data[my][mx] <= 1:  # 右下
            chk = True
    # 左向きの時
    if di == DIR[2]:
        mx = int((cx - 30 - dot) / 60)
        my = int((cy - 30) / 60)
        if map_data[my][mx] <= 1:  # 左上
            chk = True
        my = int(((cy + 29) / 60))
        if map_data[my][mx] <= 1:  # 左下
            chk = True
    # 右向きの時
    if di == DIR[3]:
        mx = int((cx + 29 + dot) / 60)
        my = int((cy - 30) / 60)
        if map_data[my][mx] <= 1:  # 右上
            chk = True
        mx = int(((cy + 29) / 60))
        if map_data[my][mx] <= 1:  # 右下
            chk = True
    return chk


# プレイヤーの移動処理
def move_pl():
    global pl_posx, pl_posy, pl_d, pl_a, score
    # 上キー
    if key == "Up":
        pl_d = 0
        if check_wall(pl_posx, pl_posy, DIR[0]) == False:
            pl_posy -= 20
    # 下キー
    if key == "Down":
        pl_d = 1
        if check_wall(pl_posx, pl_posy, DIR[1]) == False:
            pl_posy += 20
    # 左キー
    if key == "Left":
        pl_d = 2
        if check_wall(pl_posx, pl_posy, DIR[2]) == False:
            pl_posx -= 20
    # 右キー
    if key == "Right":
        pl_d = 3
        if check_wall(pl_posx, pl_posy, DIR[3]) == False:
            pl_posx += 20
    # アニメーション番号の計算
    pl_a = pl_d * 3 + ANIMATION[tmr % 4]
    mx = int(pl_posx / 60)
    my = int(pl_posy / 60)
    if map_data[my][mx] == 3:
        score += 100
        map_data[my][mx] = 2


# メインループ
def main():
    global key, koff, tmr
    tmr += 1
    draw_screen()
    move_pl()
    if koff:
        key = ""
        koff = False
    root.after(100, main)  # 300ミリ秒後にmain関数を実行


root = tkinter.Tk()  # ウィンドウの作成
root.title("はらはら　ペンギン　ラビリンス")  # タイトル
root.resizable(False, False)  # ウィンドウサイズ変更不可
root.bind("<KeyPress>", key_down)  # キーを押したときに実行する処理の指定
root.bind("<KeyRelease>", key_up)  # キーを離したときに実行する処理の指定
canvas = tkinter.Canvas(width=720, height=540)  # キャンバスの作成
canvas.pack()  # キャンバスの配置

# 画像
# マップ
img_bg = [
    tkinter.PhotoImage(file="images/chip00.png"),
    tkinter.PhotoImage(file="images/chip01.png"),
    tkinter.PhotoImage(file="images/chip02.png"),
    tkinter.PhotoImage(file="images/chip03.png"),
]
# プレイヤー
img_pl = [
    tkinter.PhotoImage(file="images/pen00.png"),
    tkinter.PhotoImage(file="images/pen01.png"),
    tkinter.PhotoImage(file="images/pen02.png"),
    tkinter.PhotoImage(file="images/pen03.png"),
    tkinter.PhotoImage(file="images/pen04.png"),
    tkinter.PhotoImage(file="images/pen05.png"),
    tkinter.PhotoImage(file="images/pen06.png"),
    tkinter.PhotoImage(file="images/pen07.png"),
    tkinter.PhotoImage(file="images/pen08.png"),
    tkinter.PhotoImage(file="images/pen09.png"),
    tkinter.PhotoImage(file="images/pen10.png"),
    tkinter.PhotoImage(file="images/pen11.png"),
]

main()
root.mainloop()
