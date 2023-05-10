import tkinter
import random

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

phase = 0  # フェーズ
tmr = 0  # タイマー
score = 0  # スコア
candy = 0  # キャンディ

# プレイヤー
pl_x = 0  # 位置ｘ
pl_y = 0  # 位置ｙ
pl_d = 1  # 向き
pl_a = 0  # 画像番号

# 敵
red_x = 0  # 位置ｘ
red_y = 0  # 位置ｙ
red_d = 0  # 向き
red_a = 0  # 画像番号


# ステージ設定処理
def set_stage():
    global map_data, candy
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
    candy = 32


# キャラのスタート位置処理
def set_chara_pos():
    global pl_x, pl_y, pl_d, pl_a
    global red_x, red_y, red_d, red_a
    pl_x = 90
    pl_y = 90
    pl_d = DIR[1]
    pl_a = 3
    red_x = 630
    red_y = 450
    red_d = DIR[1]
    red_a = 3


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
    canvas.create_image(pl_x, pl_y, image=img_pl[pl_a], tag="SCREEN")
    # 敵描画
    canvas.create_image(red_x, red_y, image=img_red[red_a], tag="SCREEN")
    # スコア描画
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
        mx = int((cx + 29) / 60)
        if map_data[my][mx] <= 1:  # 右上
            chk = True
    # 下向きの時
    if di == DIR[1]:
        mx = int((cx - 30) / 60)
        my = int((cy + 29 + dot) / 60)
        if map_data[my][mx] <= 1:  # 左下
            chk = True
        mx = int((cx + 29) / 60)
        if map_data[my][mx] <= 1:  # 右下
            chk = True
    # 左向きの時
    if di == DIR[2]:
        mx = int((cx - 30 - dot) / 60)
        my = int((cy - 30) / 60)
        if map_data[my][mx] <= 1:  # 左上
            chk = True
        my = int((cy + 29) / 60)
        if map_data[my][mx] <= 1:  # 左下
            chk = True
    # 右向きの時
    if di == DIR[3]:
        mx = int((cx + 29 + dot) / 60)
        my = int((cy - 30) / 60)
        if map_data[my][mx] <= 1:  # 右上
            chk = True
        my = int((cy + 29) / 60)
        if map_data[my][mx] <= 1:  # 右下
            chk = True
    return chk


# プレイヤーの移動処理
def move_pl():
    global pl_x, pl_y, pl_d, pl_a, score, candy
    # 上キー
    if key == "Up":
        pl_d = DIR[0]
        if check_wall(pl_x, pl_y, pl_d) == False:
            pl_y -= 20
    # 下キー
    if key == "Down":
        pl_d = DIR[1]
        if check_wall(pl_x, pl_y, pl_d) == False:
            pl_y += 20
    # 左キー
    if key == "Left":
        pl_d = DIR[2]
        if check_wall(pl_x, pl_y, pl_d) == False:
            pl_x -= 20
    # 右キー
    if key == "Right":
        pl_d = DIR[3]
        if check_wall(pl_x, pl_y, pl_d) == False:
            pl_x += 20
    # アニメーション番号の計算
    pl_a = pl_d * 3 + ANIMATION[tmr % 4]
    # キャンディ取得
    mx = int(pl_x / 60)
    my = int(pl_y / 60)
    if map_data[my][mx] == 3:
        score += 100
        map_data[my][mx] = 2
        candy -= 1


# 敵の移動処理
def move_enemy():
    global red_x, red_y, red_d, red_a, phase, tmr
    speed = 10
    if red_x % 60 == 30 and red_y % 60 == 30:
        red_d = random.randint(0, 6)
        if red_d >= 4:
            if pl_y < red_y:
                red_d = DIR[0]
            if pl_y > red_y:
                red_d = DIR[1]
            if pl_x < red_x:
                red_d = DIR[2]
            if pl_x > red_x:
                red_d = DIR[3]
    if red_d == DIR[0]:
        if check_wall(red_x, red_y, red_d, speed) == False:
            red_y -= speed
    if red_d == DIR[1]:
        if check_wall(red_x, red_y, red_d, speed) == False:
            red_y += speed
    if red_d == DIR[2]:
        if check_wall(red_x, red_y, red_d, speed) == False:
            red_x -= speed
    if red_d == DIR[3]:
        if check_wall(red_x, red_y, red_d, speed) == False:
            red_x += speed
    red_a = red_d * 3 + ANIMATION[tmr % 4]
    # プレイヤーと接触判定
    if abs(red_x - pl_x) <= 40 and abs(red_y - pl_y) <= 40:
        phase = 2
        tmr = 0


# メインループ
def main():
    global key, koff, tmr, phase, score
    tmr += 1
    draw_screen()

    # タイトル画面
    if phase == 0:
        canvas.create_image(360, 200, image=img_title, tag="SCREEN")
        if tmr % 10 < 5:
            draw_txt("Press SPSCE !", 360, 380, 30, "yellow")
        if key == "space":
            score = 0
            set_stage()
            set_chara_pos()
            phase = 1

    # ゲーム画面
    if phase == 1:
        move_pl()
        move_enemy()
        if candy == 0:
            phase = 4
            tmr = 0

    # ゲームオーバー
    if phase == 2:
        draw_txt("GAME OVER", 360, 270, 40, "red")
        if tmr == 50:
            phase = 0

    # ステージクリア
    if phase == 4:
        draw_txt("STAGE CLEAR", 360, 270, 40, "pink")
        if tmr == 50:
            phase = 0
    if koff:
        key = ""
        koff = False
    root.after(100, main)  # 300ミリ秒後にmain関数を実行


root = tkinter.Tk()  # ウィンドウの作成

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
# 敵
img_red = [
    tkinter.PhotoImage(file="images/red00.png"),
    tkinter.PhotoImage(file="images/red01.png"),
    tkinter.PhotoImage(file="images/red02.png"),
    tkinter.PhotoImage(file="images/red03.png"),
    tkinter.PhotoImage(file="images/red04.png"),
    tkinter.PhotoImage(file="images/red05.png"),
    tkinter.PhotoImage(file="images/red06.png"),
    tkinter.PhotoImage(file="images/red07.png"),
    tkinter.PhotoImage(file="images/red08.png"),
    tkinter.PhotoImage(file="images/red09.png"),
    tkinter.PhotoImage(file="images/red10.png"),
    tkinter.PhotoImage(file="images/red11.png"),
]
# タイトル
img_title = tkinter.PhotoImage(file="images/title.png")

root.title("はらはら　ペンギン　ラビリンス")  # タイトル
root.resizable(False, False)  # ウィンドウサイズ変更不可
root.bind("<KeyPress>", key_down)  # キーを押したときに実行する処理の指定
root.bind("<KeyRelease>", key_up)  # キーを離したときに実行する処理の指定
canvas = tkinter.Canvas(width=720, height=540)  # キャンバスの作成
canvas.pack()  # キャンバスの配置
set_stage()
set_chara_pos()
main()
root.mainloop()
