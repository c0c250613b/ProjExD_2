import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, 5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんまたは爆弾のRect
    戻り値：タプル(横方向判定結果,縦方向判定結果)
    画面内ならTrue, 画面外ならFalse
    """
    yoko , tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横の判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:  # gameover関数
    """
    引数:Surface
    戻り値:なし
    こうかとんと爆弾が衝突した時にgameoverを表示する
    """
    end_img = pg.Surface((WIDTH, HEIGHT))
    end_img.set_alpha(200)  # 背景がブラックになるように透明度設定
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))  # 文字の表示
    end_img.blit(txt, [WIDTH/2 - 180, HEIGHT/2 - 50])
    naki_img_left = pg.image.load("fig/8.png") 
    naki_img_right = pg.image.load("fig/8.png")
    end_img.blit(naki_img_left, [300, 260])  # こうかとん左右に配置
    end_img.blit(naki_img_right, [700, 260])
    screen.blit(end_img, [0, 0])
    pg.display.update()
    time.sleep(5)  # 5秒表示


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:  # 時間経過に応じて爆弾の大きさ、速さを変化させるための関数
    """
    引数: なし
    戻り値: 爆弾画像Surfaceのリスト, 爆弾加速度のリスト
    大きくなる爆弾の画像Surfaceと加速度をリストに格納して返す
    """
    bb_imgs = []
    bb_accs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))  # 空のSurface
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))  # 黒い部分透過
        bb_imgs.append(bb_img)
        bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:  # こうかとん回転辞書
    """
    引数: なし
    戻り値: こうかとんの画像Surfaceの辞書
    こうかとんの画像Surfaceを方向ごとに辞書に格納して返す
    """
    kk_dict = {
        (0, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1.0),
        (+5, 0): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 0, 1.0),
        (-5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 1.0),
        (0, +5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), -90, 1.0),
        (0, -5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 90, 1.0),
        (+5, +5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), -45, 1.0),
        (+5, -5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 45, 1.0),
        (-5, +5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 1.0),
        (-5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 1.0),
    }
    return kk_dict


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習2赤い爆弾
    bb_img.set_colorkey((0, 0, 0))  # 黒い部分透過
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 横、縦座標乱数
    vx, vy = +5, +5  # 爆弾横方向速度+5、縦方向速度+5
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_accs = init_bb_imgs()  # 爆弾画像Surfaceと加速度リストの初期化
    kk_dict = get_kk_imgs()  # こうかとんの画像Surfaceの辞書
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):  # こうかとんとrectが重なっていたら
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key_press, tpl in DELTA.items():
            if key_lst[key_press]:
                sum_mv[0] += tpl[0]  # 上下
                sum_mv[1] += tpl[1]  # 左右
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # どこかはみ出てる
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 先程の動きをキャンセルする
        screen.blit(kk_img, kk_rct)

        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]  # 爆弾画像Surfaceの更新

        # bb_rct.move_ip(vx, vy)  # 爆弾移動
        bb_rct.move_ip(avx, avy)  # 爆弾加速度移動
        bb_rct.width = bb_img.get_rect().width  # 爆弾のRectの幅を更新
        bb_rct.height = bb_img.get_rect().height  # 爆弾のRectの高さを更新

        kk_img = kk_dict[tuple(sum_mv)]  # こうかとんの画像Surfaceの更新
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # yoko==false
            vx *= -1
        if not tate:  # tate==false
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
