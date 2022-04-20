import pygame as p
import sys
import traceback
import myplane
import enemy
import bullet
import supply
import random
from pygame.locals import *

p.init()
p.mixer.init()

#初始化游戏窗口
bg_size = width, height = 480, 700
screen = p.display.set_mode(bg_size)
p.display.set_caption("Thunder -- Wyb Demo")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

#载入图片
background = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\background.png").convert()
pause_nor_image = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\pause_nor.png").convert_alpha()
pause_pressed_image = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\pause_pressed.png").convert_alpha()
resume_nor_image = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\resume_nor.png").convert_alpha()
resume_pressed_image = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\resume_pressed.png").convert_alpha()
bomb_image = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\bomb.png").convert_alpha()
life_image = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\life.png").convert_alpha()
again_image = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\again.png").convert_alpha()
gameover_image = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\gameover.png").convert_alpha()

#载入音乐
p.mixer.music.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\sound\\bgm.mp3")
p.mixer.music.set_volume(0.2)
enemy3_fly_sound = p.mixer.Sound("C:\\Users\\dell\\Desktop\\python\\Thunder\\sound\\enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.1)
enemy1_down_sound = p.mixer.Sound("C:\\Users\\dell\\Desktop\\python\\Thunder\\sound\\enemy1_down.wav")
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = p.mixer.Sound("C:\\Users\\dell\\Desktop\\python\\Thunder\\sound\\enemy2_down.wav")
enemy2_down_sound.set_volume(0.1)
enemy3_down_sound = p.mixer.Sound("C:\\Users\\dell\\Desktop\\python\\Thunder\\sound\\enemy3_down.wav")
enemy3_down_sound.set_volume(0.1)
me_down_sound = p.mixer.Sound("C:\\Users\\dell\\Desktop\\python\\Thunder\\sound\\me_down.wav")
me_down_sound.set_volume(0.1)
upgrade_sound = p.mixer.Sound("C:\\Users\\dell\\Desktop\\python\\Thunder\\sound\\upgrade.wav")
upgrade_sound.set_volume(0.1)
bomb_sound = p.mixer.Sound("C:\\Users\\dell\\Desktop\\python\\Thunder\\sound\\bomb.wav")
bomb_sound.set_volume(0.1)
supply_sound = p.mixer.Sound("C:\\Users\\dell\\Desktop\\python\\Thunder\\sound\\supply.wav")
supply_sound.set_volume(0.1)
supply_get_sound = p.mixer.Sound("C:\\Users\\dell\\Desktop\\python\\Thunder\\sound\\supply_get.wav")
supply_get_sound.set_volume(0.1)
bullet_sound = p.mixer.Sound("C:\\Users\\dell\\Desktop\\python\\Thunder\\sound\\bullet.wav")
bullet_sound.set_volume(0.1)

#设置字体
score_font = p.font.Font("C:\\Users\\dell\\Desktop\\python\\Thunder\\font\\font.ttf", 36)
bomb_font = p.font.Font("C:\\Users\\dell\\Desktop\\python\\Thunder\\font\\font.ttf", 48)
gameover_font = p.font.Font("C:\\Users\\dell\\Desktop\\python\\Thunder\\font\\font.ttf", 48)

def inc_speed(target, inc):
    for each in target:
        each.speed += inc

def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def main():
    #生成背景音乐
    p.mixer.music.play(-1)

    #用于切换图片
    switch_image = True

    #用于延迟
    delay = 100

    #设置难度级别
    level = 1

    #设置子弹频率
    FREQ = 10

    #设置生命数
    life_rect = life_image.get_rect()
    life_num = 3

    #无敌时间定时器
    INVINCIBLE_TIME = USEREVENT + 2

    #全屏炸弹
    bomb_rect = bomb_image.get_rect()
    bomb_num = 3

    #每一段时间发放补给包
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    p.time.set_timer(SUPPLY_TIME, 25 * 1000)

    #超级子弹定时器
    DOUBLE_BULLET_TIME = USEREVENT + 1

    #标志是否使用超级子弹
    is_double_bullet = False

    #用于阻止循环
    recorded = False

    #生成我方飞机
    me = myplane.MyPlane(bg_size)

    #生成敌方飞机
    enemies = p.sprite.Group()
    #生成小型敌机
    small_enemies = p.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)
    #生成中型敌机
    mid_enemies = p.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)
    #生成大型敌机
    big_enemies = p.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    #生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    #生成超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))

    #中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    #统计得分
    score = 0

    #是否暂停游戏
    paused = False
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image

    #游戏结束画面
    again_rect = again_image.get_rect()
    gameover_rect = gameover_image.get_rect()

    clock = p.time.Clock()

    running = True

    while running:
        for event in p.event.get():
            if event.type == QUIT:
                p.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        p.time.set_timer(SUPPLY_TIME, 0)
                        p.mixer.music.pause()
                        p.mixer.pause()
                    else:
                        p.time.set_timer(SUPPLY_TIME, 25 * 1000)
                        p.mixer.music.unpause()
                        p.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if random.choice([True,False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                p.time.set_timer(DOUBLE_BULLET_TIME, 0)
                FREQ = 10

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                p.time.set_timer(INVINCIBLE_TIME, 0)

        #绘制背景图片
        screen.blit(background, (0,0))

        #根据得分增加难度
        if level == 1 and score > 20000:
            level = 2
            upgrade_sound.play()
            #增加3架小型敌机，2架中型敌机，1架大型敌机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            #提升小型敌机的速度
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 100000:
            level = 3
            upgrade_sound.play()
            #增加5架小型敌机，3架中型敌机，2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #提升小型、中型敌机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 300000:
            level = 4
            upgrade_sound.play()
            #增加5架小型敌机，3架中型敌机，2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #提升小型、中型敌机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 4 and score > 600000:
            level = 5
            upgrade_sound.play()
            #增加5架小型敌机，3架中型敌机，2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #提升小型、中型、大型敌机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            inc_speed(big_enemies, 1)


        if not paused and life_num:
            #检测键盘操作
            key_pressed = p.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()
            if key_pressed[K_i]:
                me.invincible = not me.invincible
            if key_pressed[K_b]:
                bomb_num = 3
            if key_pressed[K_o]:
                is_double_bullet = not is_double_bullet

            #绘制炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if p.sprite.collide_mask(bomb_supply, me):
                    supply_get_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            #绘制子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if p.sprite.collide_mask(bullet_supply, me):
                    supply_get_sound.play()
                    #发射超级子弹
                    is_double_bullet = True
                    p.time.set_timer(DOUBLE_BULLET_TIME, 20 * 1000)
                    bullet_supply.active = False
                    FREQ = 5

            #发射子弹
            if not(delay % FREQ):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullet1[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            #检测子弹是否命中
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = p.sprite.spritecollide(b, enemies, False, p.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False

            #绘制大型敌机
            for each in big_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        #绘制被击中特效
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    #绘制血槽
                    p.draw.line(screen, BLACK, \
                                (each.rect.left, each.rect.top - 5),\
                                (each.rect.right, each.rect.top - 5),2)
                    #生命大于20%，显示绿色，否则红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain >0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    p.draw.line(screen, energy_color, \
                                (each.rect.left, each.rect.top - 5),\
                                (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)

                    #即将出现在画面中，播放音效
                    if -50 < each.rect.bottom < 0:
                        enemy3_fly_sound.play(-1)
                    if each.rect.bottom > 0:
                        enemy3_fly_sound.stop()
                else:
                    #毁灭
                    if not(delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            score += 10000
                            each.reset()
            #绘制中型敌机
            for each in mid_enemies:
                if each.active:
                    each.move()
                    if each.hit:
                        #绘制被击中特效
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    #绘制血槽
                    p.draw.line(screen, BLACK, \
                                (each.rect.left, each.rect.top - 5),\
                                (each.rect.right, each.rect.top - 5),2)
                    #生命大于20%，显示绿色，否则红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain >0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    p.draw.line(screen, energy_color, \
                                (each.rect.left, each.rect.top - 5),\
                                (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)
                else:
                    #毁灭
                    if not(delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()

            #绘制小型敌机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    #毁灭
                    if not(delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()

            #我方飞机碰撞检测
            enemies_down = p.sprite.spritecollide(me, enemies, False, p.sprite.collide_mask)
            if enemies_down:
                if not me.invincible:
                    me.active = False
                for e in enemies_down:
                    e.active = False


            #绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                #毁灭
                    if not(delay % 3):
                        if me_destroy_index == 0:
                            me_down_sound.play()
                        screen.blit(me.destroy_images[me_destroy_index], me.rect)
                        me_destroy_index = (me_destroy_index + 1) % 4
                        if me_destroy_index == 0:
                            life_num -= 1
                            me.reset()
                            p.time.set_timer(INVINCIBLE_TIME, 3 * 1000)


            #绘制炸弹数量
            bomb_text = bomb_font.render("× %d" % bomb_num, True, WHITE)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

            #绘制生命数量
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image,\
                                (width - 10 - (i + 1) * life_rect.width,\
                                height - 10 - life_rect.height))
            #绘制分数
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)
            screen.blit(score_text, (10, 5))

        elif not life_num:
            #游戏结束
            #背景音乐停止
            p.mixer.music.stop()
            #游戏音效停止
            p.mixer.stop()
            #停止发放补给
            p.time.set_timer(SUPPLY_TIME, 0)

            if not recorded:
                recorded = True
                #读取历史最高得分
                with open("C:\\Users\\dell\\Desktop\\python\\Thunder\\record.txt","r") as f:
                    record_score = int(f.read())

                if score > record_score:
                    with open("C:\\Users\\dell\\Desktop\\python\\Thunder\\record.txt","w") as f:
                        f.write(str(score))
                        record_score = score

            #绘制游戏结束界面
            record_score_text = score_font.render("Best: %d" % record_score, True, WHITE)
            screen.blit(record_score_text, (50, 50))

            gameover_text1 =gameover_font.render("Your Score", True, WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) //2,\
                                                                height // 2
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 =gameover_font.render(str(score), True, WHITE)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = (width - gameover_text2_rect.width) //2,\
                                                                gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = (width - again_rect.width) // 2, \
                                                gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = (width - gameover_rect.width) // 2, \
                                                    again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            #检测鼠标操作
            #如果按下鼠标左键
            if p.mouse.get_pressed()[0]:
                #获取鼠标坐标
                pos = p.mouse.get_pos()
                #如果重新开始
                if again_rect.left < pos[0] < again_rect.right and\
                    again_rect.top < pos[1] < again_rect.bottom:
                    #调用main()函数，重新开始游戏
                    main()
                #如果结束游戏
                if gameover_rect.left < pos[0] < gameover_rect.right and\
                    gameover_rect.top < pos[1] < gameover_rect.bottom:
                    p.quit()
                    sys.exit()

        #绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        #切换图片
        if not (delay % 5):
            switch_image = not switch_image
        delay -= 1
        if not delay:
            delay = 100

        p.display.flip()
        clock.tick(64)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        p.quit()
        input()