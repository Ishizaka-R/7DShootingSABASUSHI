import pygame
import sys
import math
import random
import os
from pygame.locals import *


# ライブラリのインポート
import sqlite3
# データベースへの接続（ない場合は作成）
conn = sqlite3.connect('sample.db')
print('データベースを作成しました。')
# 接続の切断
conn.close()

# スクリプトのディレクトリを取得
script_dir = os.path.dirname(__file__)

# カラーパレット
BLACK = (  0,   0,   0)
SILVER= (192, 208, 224)
RED   = (255,   0,   0)
CYAN  = (  0, 224, 255)

# 画像の読み込み
# img_galaxy = pygame.image.load(os.path.join(script_dir, "image_gl/galaxy.png"))

img_galaxy = pygame.image.load(os.path.join(script_dir, "image_gl/haikei2.png"))


img_sship = [
    # pygame.image.load(os.path.join(script_dir, "image_gl/syari2.png")),
    # pygame.image.load(os.path.join(script_dir, "image_gl/syari3l.png")),
    # pygame.image.load(os.path.join(script_dir, "image_gl/syari3r.png")),

    pygame.image.load(os.path.join(script_dir, "image_gl/sabasushi1.png")),
    pygame.image.load(os.path.join(script_dir, "image_gl/sabasushi1l.png")),
    pygame.image.load(os.path.join(script_dir, "image_gl/sabasushi1r.png")),

    # pygame.image.load(os.path.join(script_dir, "image_gl/magurosushi1.png")),
    # pygame.image.load(os.path.join(script_dir, "image_gl/magurosushi1l.png")),
    # pygame.image.load(os.path.join(script_dir, "image_gl/magurosushi1r.png")),

    # pygame.image.load(os.path.join(script_dir, "image_gl/ikurasushi1.png")),
    # pygame.image.load(os.path.join(script_dir, "image_gl/ikurasushi1l.png")),
    # pygame.image.load(os.path.join(script_dir, "image_gl/ikurasushi1r.png")),

    # pygame.image.load(os.path.join(script_dir, "image_gl/sakesushi2.png")),
    # pygame.image.load(os.path.join(script_dir, "image_gl/sakesushi2l.png")),
    # pygame.image.load(os.path.join(script_dir, "image_gl/sakesushi2r.png")),

    # pygame.image.load(os.path.join(script_dir, "image_gl/ebisushi1.png")),
    # pygame.image.load(os.path.join(script_dir, "image_gl/ebisushi1l.png")),
    # pygame.image.load(os.path.join(script_dir, "image_gl/ebisushi1r.png")),
 
]
img_weapon = pygame.image.load(os.path.join(script_dir, "image_gl/kome1.png"))
# img_shield = pygame.image.load(os.path.join(script_dir, "image_gl/shield.png"))

img_shield = pygame.image.load(os.path.join(script_dir, "image_gl/hp.png"))

img_enemy = [
    pygame.image.load(os.path.join(script_dir, "image_gl/wasabi6.png")),
    pygame.image.load(os.path.join(script_dir, "image_gl/saba3.png")),
    pygame.image.load(os.path.join(script_dir, "image_gl/ebi3.png")),
    pygame.image.load(os.path.join(script_dir, "image_gl/sake3.png")),
    pygame.image.load(os.path.join(script_dir, "image_gl/maguro3.png")),
    pygame.image.load(os.path.join(script_dir, "image_gl/tako3.png")),
    pygame.image.load(os.path.join(script_dir, "image_gl/tako4.png"))
]
img_explode = [
    None,
    pygame.image.load(os.path.join(script_dir, "image_gl/explosion1.png")),
    pygame.image.load(os.path.join(script_dir, "image_gl/explosion2.png")),
    pygame.image.load(os.path.join(script_dir, "image_gl/explosion3.png")),
    pygame.image.load(os.path.join(script_dir, "image_gl/explosion4.png")),
    pygame.image.load(os.path.join(script_dir, "image_gl/explosion5.png"))
]
img_title = [
    # pygame.image.load(os.path.join(script_dir, "image_gl/nebula.png")),
    pygame.image.load(os.path.join(script_dir, "image_gl/logo2.png"))
]

# SEを読み込む変数
# se_barrage = pygame.mixer.Sound(os.path.join(script_dir, "sound_gl/barrage.ogg"))
# se_damage = pygame.mixer.Sound(os.path.join(script_dir, "sound_gl/damage.ogg"))
# se_explosion = pygame.mixer.Sound(os.path.join(script_dir, "sound_gl/explosion.ogg"))
# se_shot = pygame.mixer.Sound(os.path.join(script_dir, "sound_gl/shot.ogg"))

idx = 0
tmr = 0
score = 0
bg_y = 0

ss_x = 0
ss_y = 0
ss_d = 0
ss_shield = 0
ss_muteki = 0
key_spc = 0
key_z = 0

MISSILE_MAX = 200
msl_no = 0
msl_f = [False]*MISSILE_MAX
msl_x = [0]*MISSILE_MAX
msl_y = [0]*MISSILE_MAX
msl_a = [0]*MISSILE_MAX

ENEMY_MAX = 100
emy_no = 0
emy_f = [False]*ENEMY_MAX
emy_x = [0]*ENEMY_MAX
emy_y = [0]*ENEMY_MAX
emy_a = [0]*ENEMY_MAX
emy_type = [0]*ENEMY_MAX
emy_speed = [0]*ENEMY_MAX
emy_shield = [0]*ENEMY_MAX
emy_count = [0]*ENEMY_MAX

EMY_BULLET = 0
EMY_ZAKO = 1
EMY_BOSS = 5
LINE_T = -80
LINE_B = 800
LINE_L = -80
LINE_R = 1040

EFFECT_MAX = 100
eff_no = 0
eff_p = [0]*EFFECT_MAX
eff_x = [0]*EFFECT_MAX
eff_y = [0]*EFFECT_MAX


def get_dis(x1, y1, x2, y2): # 二点間の距離を求める
    return( (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) )


def draw_text(scrn, txt, x, y, siz, col): # 文字の表示
    fnt = pygame.font.Font(None, siz)
    sur = fnt.render(txt, True, col)
    x = x - sur.get_width()/2
    y = y - sur.get_height()/2
    scrn.blit(sur, [x, y])


def move_starship(scrn, key): # 自機の移動
    global idx, tmr, ss_x, ss_y, ss_d, ss_shield, ss_muteki, key_spc, key_z
    ss_d = 0
    if key[K_UP] == 1:
        ss_y = ss_y - 20
        if ss_y < 80:
            ss_y = 80
    if key[K_DOWN] == 1:
        ss_y = ss_y + 20
        if ss_y > 640:
            ss_y = 640
    if key[K_LEFT] == 1:
        ss_d = 1
        ss_x = ss_x - 20
        if ss_x < 40:
            ss_x = 40
    if key[K_RIGHT] == 1:
        ss_d = 2
        ss_x = ss_x + 20
        if ss_x > 920:
            ss_x = 920
    key_spc = (key_spc+1)*key[K_SPACE]
    if key_spc%5 == 1:
        set_missile(0)
        se_shot.play()
    key_z = (key_z+1)*key[K_z]
    if key_z == 1 and ss_shield > 10:
        set_missile(10)
        ss_shield = ss_shield - 10
        se_barrage.play()

    if ss_muteki%2 == 0:
        # scrn.blit(img_sship[3], [ss_x-8, ss_y+40+(tmr%3)*2])
        scrn.blit(img_sship[ss_d], [ss_x-37, ss_y-48])

    if ss_muteki > 0:
        ss_muteki = ss_muteki - 1
        return
    elif idx == 1:
        for i in range(ENEMY_MAX): # 敵とのヒットチェック
            if emy_f[i] == True:
                w = img_enemy[emy_type[i]].get_width()
                h = img_enemy[emy_type[i]].get_height()
                r = int((w+h)/4 + (74+96)/4)
                if get_dis(emy_x[i], emy_y[i], ss_x, ss_y) < r*r:
                    set_effect(ss_x, ss_y)
                    ss_shield = ss_shield - 10
                    if ss_shield <= 0:
                        ss_shield = 0
                        idx = 2
                        tmr = 0
                    if ss_muteki == 0:
                        ss_muteki = 60
                        se_damage.play()
                    if emy_type[i] < EMY_BOSS:
                        emy_f[i] = False


def set_missile(typ): # 自機の発射する弾をセットする
    global msl_no
    if typ == 0: # 単発
        msl_f[msl_no] = True
        msl_x[msl_no] = ss_x
        msl_y[msl_no] = ss_y-50
        msl_a[msl_no] = 270
        msl_no = (msl_no+1)%MISSILE_MAX
    if typ == 10: # 弾幕
        for a in range(160, 390, 10):
            msl_f[msl_no] = True
            msl_x[msl_no] = ss_x
            msl_y[msl_no] = ss_y-50
            msl_a[msl_no] = a
            msl_no = (msl_no+1)%MISSILE_MAX


def move_missile(scrn): # 弾の移動
    for i in range(MISSILE_MAX):
        if msl_f[i] == True:
            msl_x[i] = msl_x[i] + 36*math.cos(math.radians(msl_a[i]))
            msl_y[i] = msl_y[i] + 36*math.sin(math.radians(msl_a[i]))
            img_rz = pygame.transform.rotozoom(img_weapon, -90-msl_a[i], 1.0)
            scrn.blit(img_rz, [msl_x[i]-img_rz.get_width()/2, msl_y[i]-img_rz.get_height()/2])
            if msl_y[i] < 0 or msl_x[i] < 0 or msl_x[i] > 960:
                msl_f[i] = False


def bring_enemy(): # 敵を出す
    sec = tmr/30 # タイマーのカウント値 tmrを30で割ることで、秒数に換算
    if 0 < sec and sec < 18 and tmr%60 == 0: # 0から15秒の間で、かつ1秒ごとに敵を出現させるタイミングを狙っています
        '''
        random.randint(20, 940)で、画面横幅（20から940ピクセル）のランダムな位置に敵が出現します。
        LINE_T、敵が出現するY座標（画面の上部）を示しています。
        90は敵の移動方向（90度 = 水平移動）を示しており、敵が右方向に移動することを意味します。
        EMY_ZAKOは敵のタイプを指定する定数。敵の種類や特徴に関連しています。
        8は敵のスピード、1は敵の耐久力（体力）などを示す値です。
        これで、最初の敵がランダムなX座標で出現します。
        '''
        set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO, 8, 1) # 敵1
        set_enemy(random.randint(20, 940), LINE_T, 90, EMY_ZAKO+1, 12, 1) # 敵2
        set_enemy(random.randint(100, 860), LINE_T, random.randint(60, 120), EMY_ZAKO+2, 6, 3) # 敵3
        set_enemy(random.randint(100, 860), LINE_T, 90, EMY_ZAKO+3, 12, 2) # 敵4
    if tmr == 30*20: # ボス出現(20秒経過したとき)
        set_enemy(480, -210, 90, EMY_BOSS, 4, 200)


def set_enemy(x, y, a, ty, sp, sh): # 敵機をセットする
    global emy_no
    while True:
        if emy_f[emy_no] == False:
            emy_f[emy_no] = True
            emy_x[emy_no] = x
            emy_y[emy_no] = y
            emy_a[emy_no] = a
            emy_type[emy_no] = ty
            emy_speed[emy_no] = sp
            emy_shield[emy_no] = sh
            emy_count[emy_no] = 0
            break
        emy_no = (emy_no+1)%ENEMY_MAX


def move_enemy(scrn): # 敵機の移動

    
    global idx, tmr, score, ss_shield
    for i in range(ENEMY_MAX):
        if emy_f[i] == True:
            ang = -90-emy_a[i]
            png = emy_type[i]


            # ボス以外の敵のサイズを50%大きくする
            if emy_type[i] < 5:  # ボスでない敵
                img_rz = pygame.transform.rotozoom(img_enemy[png], ang, 1.5)  # サイズを1.5倍に
            else:  # ボスはそのまま
                img_rz = pygame.transform.rotozoom(img_enemy[png], ang, 1.0)


            # 敵の移動とロジック
            if emy_type[i] < EMY_BOSS: # ザコの動き
                emy_x[i] = emy_x[i] + emy_speed[i]*math.cos(math.radians(emy_a[i]))
                emy_y[i] = emy_y[i] + emy_speed[i]*math.sin(math.radians(emy_a[i]))
                if emy_type[i] == 4: # 進行方向を変える敵
                    emy_count[i] = emy_count[i] + 1
                    ang = emy_count[i]*10
                    if emy_y[i] > 240 and emy_a[i] == 90:
                        emy_a[i] = random.choice([50,70,110,130])
                        set_enemy(emy_x[i], emy_y[i], 90, EMY_BULLET, 6, 0)
                if emy_x[i] < LINE_L or LINE_R < emy_x[i] or emy_y[i] < LINE_T or LINE_B < emy_y[i]:
                    emy_f[i] = False
            else: # ボスの動き
                if emy_count[i] == 0:
                    emy_y[i] = emy_y[i] + 2
                    if emy_y[i] >= 200:
                        emy_count[i] = 1
                elif emy_count[i] == 1:
                    emy_x[i] = emy_x[i] - emy_speed[i]
                    if emy_x[i] < 200:
                        for j in range(0, 10):
                            set_enemy(emy_x[i], emy_y[i]+80, j*20, EMY_BULLET, 6, 0)
                        emy_count[i] = 2
                else:
                    emy_x[i] = emy_x[i] + emy_speed[i]
                    if emy_x[i] > 760:
                        for j in range(0, 10):
                            set_enemy(emy_x[i], emy_y[i]+80, j*20, EMY_BULLET, 6, 0)
                        emy_count[i] = 1
                if emy_shield[i] < 100 and tmr%30 == 0:
                    set_enemy(emy_x[i], emy_y[i]+80, random.randint(60, 120), EMY_BULLET, 6, 0)

            if emy_type[i] != EMY_BULLET: # プレイヤーの弾とのヒットチェック
                w = img_enemy[emy_type[i]].get_width()
                h = img_enemy[emy_type[i]].get_height()
                r = int((w+h)/4)+12
                er = int((w+h)/4)
                for n in range(MISSILE_MAX):
                    if msl_f[n] == True and get_dis(emy_x[i], emy_y[i], msl_x[n], msl_y[n]) < r*r:
                        msl_f[n] = False
                        set_effect(emy_x[i]+random.randint(-er, er), emy_y[i]+random.randint(-er, er))
                        if emy_type[i] == EMY_BOSS: # ボスはフラッシュさせる
                            png = emy_type[i] + 1
                        emy_shield[i] = emy_shield[i] - 1
                        score = score + 100
                        if emy_shield[i] == 0:
                            emy_f[i] = False
                            if ss_shield < 100:
                                ss_shield = ss_shield + 1
                            if emy_type[i] == EMY_BOSS and idx == 1: # ボスを倒すとクリア
                                idx = 3
                                tmr = 0
                                for j in range(10):
                                    set_effect(emy_x[i]+random.randint(-er, er), emy_y[i]+random.randint(-er, er))
                                se_explosion.play()

            img_rz = pygame.transform.rotozoom(img_enemy[png], ang, 1.0)
            scrn.blit(img_rz, [emy_x[i]-img_rz.get_width()/2, emy_y[i]-img_rz.get_height()/2])


def set_effect(x, y): # 爆発をセットする
    global eff_no
    eff_p[eff_no] = 1
    eff_x[eff_no] = x
    eff_y[eff_no] = y
    eff_no = (eff_no+1)%EFFECT_MAX


def draw_effect(scrn): # 爆発の演出
    for i in range(EFFECT_MAX):
        if eff_p[i] > 0:
            scrn.blit(img_explode[eff_p[i]], [eff_x[i]-48, eff_y[i]-48])
            eff_p[i] = eff_p[i] + 1
            if eff_p[i] == 6:
                eff_p[i] = 0





# データベース接続とテーブル作成
def setup_database():
    conn = sqlite3.connect('sample.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def record_score(player_name, score, condition):
    """
    スコアをデータベースに保存する関数
    condition: "CLEAR" または "GAME OVER"
    """
    conn = sqlite3.connect('sample.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scores (player_name, score)
        VALUES (?, ?)
    ''', (f"{player_name} ({condition})", score))
    conn.commit()
    conn.close()

    # トップスコアを取得する関数
def get_top_scores(limit=5):
    conn = sqlite3.connect('sample.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player_name, score, date
        FROM scores
        ORDER BY score DESC
        LIMIT ?
    ''', (limit,))
    scores = cursor.fetchall()
    conn.close()
    return scores

    # 前回のスコアを取得する関数
def get_last_score():
    conn = sqlite3.connect('sample.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player_name, score, date
        FROM scores
        ORDER BY id DESC
        LIMIT 1
    ''')
    row = cursor.fetchone()
    conn.close()
    return row  # (player_name, score, date) or None


def draw_text(scrn, txt, x, y, siz, col):
    """
    日本語対応の文字描画
    """
    try:
        font_path = os.path.join(script_dir, "meiryo.ttc")  # 日本語フォントのパス
        if not os.path.exists(font_path):
            font_path = r"C:\Windows\Fonts\meiryo.ttc"  # Windowsフォントフォルダ
        fnt = pygame.font.Font(font_path, int(siz * 0.5))  # サイズを50%に縮小
    except FileNotFoundError:
        fnt = pygame.font.Font(None, siz)  # フォントが見つからない場合、デフォルトフォントを使用
    sur = fnt.render(txt, True, col)
    scrn.blit(sur, (x - sur.get_width() // 2, y - sur.get_height() // 2))




def main(): # メインループ
    global idx, tmr, score, bg_y, ss_x, ss_y, ss_d, ss_shield, ss_muteki
    global se_barrage, se_damage, se_explosion, se_shot

    pygame.init()
    pygame.display.set_caption("Shooting Saba")
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()

    setup_database()  # データベースのセットアップ
    
    se_barrage = pygame.mixer.Sound(os.path.join(script_dir, "sound_gl/barrage.ogg"))
    se_damage = pygame.mixer.Sound(os.path.join(script_dir, "sound_gl/damage.ogg"))
    se_explosion = pygame.mixer.Sound(os.path.join(script_dir, "sound_gl/explosion.ogg"))
    se_shot = pygame.mixer.Sound(os.path.join(script_dir, "sound_gl/shot.ogg"))

    while True:
        tmr = tmr + 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_F1:
                    screen = pygame.display.set_mode((960, 720), FULLSCREEN)
                if event.key == K_F2 or event.key == K_ESCAPE:
                    screen = pygame.display.set_mode((960, 720))

        # 背景のスクロール
        bg_y = (bg_y+16)%720
        screen.blit(img_galaxy, [0, bg_y-720])
        screen.blit(img_galaxy, [0, bg_y])

        key = pygame.key.get_pressed()


        






        if idx == 0: # タイトル画面

            last_score = get_last_score()
            if last_score:
                player_name, score, date = last_score
                draw_text(screen, f"前回の得点: {score} ", 200, 50, 40, CYAN)

            top_scores = get_top_scores()
            
            y_offset = 100
            for rank, (player_name, score, date) in enumerate(top_scores, start=1):
                draw_text(screen, f"{rank}. {player_name}: {score}", 680, 100 + y_offset, 40, CYAN)
                y_offset += 50


            img_rz = pygame.transform.rotozoom(img_title[0], 0, 0.5)  # 0度回転、40%サイズ
            screen.blit(img_rz, [480 - img_rz.get_width() / 1, 280 - img_rz.get_height() / 2])  # 中央に配置



            draw_text(screen, "[SPACE]キーで開始します", 480, 600, 50, SILVER)

            if key[K_SPACE] == 1:
                idx = 1
                tmr = 0
                score = 0
                ss_x = 480
                ss_y = 600
                ss_d = 0
                ss_shield = 100
                ss_muteki = 0
                for i in range(ENEMY_MAX):
                    emy_f[i] = False
                for i in range(MISSILE_MAX):
                    msl_f[i] = False
                pygame.mixer.music.load(os.path.join(script_dir, "sound_gl/bgm.ogg"))
                pygame.mixer.music.play(-1)

        if idx == 1: # ゲームプレイ中
            move_starship(screen, key)
            move_missile(screen)
            bring_enemy()
            move_enemy(screen)

        if idx == 2: # ゲームオーバー
            move_missile(screen)
            move_enemy(screen)
            if tmr == 1:
                pygame.mixer.music.stop()
                record_score("Player", score, "GAME OVER")  # スコアを保存
            if tmr <= 90:
                if tmr%5 == 0:
                    set_effect(ss_x+random.randint(-60,60), ss_y+random.randint(-60,60))
                if tmr%10 == 0:
                    se_damage.play()
            if tmr == 120:
                pygame.mixer.music.load(os.path.join(script_dir, "sound_gl/gameover.ogg"))
                pygame.mixer.music.play(0)
            if tmr > 120:
                draw_text(screen, "シャリが飛散した。握りが甘かったようだ。", 480, 300, 80, (255, 255, 255))
            if tmr == 400:
                idx = 0
                tmr = 0

        if idx == 3: # ゲームクリア
            move_starship(screen, key)
            move_missile(screen)
            if tmr == 1:
                pygame.mixer.music.stop()
                record_score("Player", score, "CLEAR")  # スコアを保存
            if tmr == 2:
                pygame.mixer.music.load(os.path.join(script_dir, "sound_gl/gameclear.ogg"))
                pygame.mixer.music.play(0)
            if tmr > 20:
                draw_text(screen, "寿司キングは君だ！", 480, 300, 160, SILVER)
            if tmr == 300:
                idx = 0
                tmr = 0

        draw_effect(screen) # 爆発の演出

        

        if idx != 0: # スタート画面以外の場合
            draw_text(screen, "得点 "+str(score), 200, 30, 50, SILVER) # スコア表示
            screen.blit(img_shield, [40, 680]) # シールドの表示
            pygame.draw.rect(screen, (64,32,32), [40+ss_shield*4, 680, (100-ss_shield)*4, 12])

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':


    





    main()
