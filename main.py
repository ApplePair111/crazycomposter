# Crazy Composter'ı size sunmak için birkaç ay boyunca çalışıyoruz. Bu oyun için çok uğraştık.
# İyi Oyunlar Dileriz! ^_^

#!/usr/bin/env python3

import pygame
import sys
import random
import json
import os
import subprocess

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dir)

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load(resource_path("DockIcon.png")))
POINT_GET = pygame.USEREVENT
do_break = False
img_files = [
    resource_path("assets/apple.png"),
    resource_path("assets/carrot.png"),
    resource_path("assets/egg.png"),
    resource_path("assets/grass.png"),
    resource_path("assets/leaf.png"),
    resource_path("assets/wheat.png"),
    resource_path("assets/metal.png"),
    resource_path("assets/milk.png"),
    resource_path("assets/naylon.png"),
    resource_path("assets/plastic.png"),
    resource_path("assets/paper.png"),
    resource_path("assets/bone.png"),
    resource_path("assets/glass.png"),
    resource_path("assets/coin.png"),
]
point_dict = {
    resource_path("assets/apple.png"): 2,
    resource_path("assets/carrot.png"): 2,
    resource_path("assets/egg.png"): 2,
    resource_path("assets/grass.png"): 1,
    resource_path("assets/leaf.png"): 1,
    resource_path("assets/wheat.png"): 2,
    resource_path("assets/metal.png"): -3,
    resource_path("assets/glass.png"): -3,
    resource_path("assets/bone.png"): -3,
    resource_path("assets/milk.png"): -2,
    resource_path("assets/naylon.png"): -2,
    resource_path("assets/plastic.png"): -2,
    resource_path("assets/paper.png"): -1,
    resource_path("assets/coin.png"): 0,
}
with open(resource_path("data.json"), "r") as f:
    data = json.load(f)
percentages = [data["max_per"]]
scores = [data["high_score"]]
money = data["money"]
points_2 = data["points"]
speed_boosts_left = data["speed_boosts"]
def save():
    pygame.quit()
    with open(resource_path("data.json"), "w") as f:
        json.dump({"high_score": max(scores),
                   "max_per": max(percentages),
                   "money": money,
                   "points": points_2,
                   "speed_boosts": speed_boosts_left}, f)
def fixed_max(li):
    big = li[0]
    for i in li[1:]:
        if i > big:
            big = i
    return big
items_existed = []
run = True
in_main_menu = True
speed_boost_activated = False
coin_img = pygame.image.load(resource_path("assets/coin.png"))
coin_img = pygame.transform.scale_by(coin_img, 1/40)
point_img = pygame.image.load(resource_path("assets/point.png"))
point_img = pygame.transform.scale_by(point_img, 1/40)
speed_img = pygame.image.load(resource_path("assets/speed_boost.png"))
speed_img = pygame.transform.scale_by(speed_img, 5 / 128)
width, height = 800, 800
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("")
font = pygame.font.SysFont("Comic Sans", 20)
coin_text_font = pygame.font.SysFont("Comic Sans", 30)
class Button:
    def __init__(self, pos, screenobj, fontobject, topleft_border_radius = -1, topright_border_radius = -1, bottomleft_border_radius = -1, bottomright_border_radius = -1, hitbox="rect", width=100, height=50, text="", color=(255, 255, 255), text_color = (0, 0, 0), outline_color = (0, 0, 0), outline_width=1):
        self.width = width
        self.height = height
        self.pos = pos
        self.text = text
        self.color = color
        self.fontobject = fontobject
        self.text_color = text_color
        self.hitbox = hitbox
        if self.hitbox == "rect":
            self.bottom_right_rad = bottomright_border_radius
            self.top_left_rad = topleft_border_radius
            self.top_right_rad = topright_border_radius
            self.bottom_left_rad = bottomleft_border_radius
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.screenobj = screenobj
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.size = 100
        if hitbox not in ['rect', 'ellipse']:
            raise ValueError("Hitbox must be 'rect' or 'ellipse'.")
    def is_clicked(self):
        return self.is_on_hover() and any(pygame.mouse.get_pressed())
    def draw(self):
        if self.hitbox == 'ellipse':
            pygame.draw.ellipse(self.screenobj, self.color, self.rect, width=0)
            pygame.draw.ellipse(self.screenobj, self.outline_color, self.rect, width=self.outline_width)
            text_rendered = self.fontobject.render(self.text, True, self.text_color)
            text_rect = text_rendered.get_rect(center=self.rect.center)
            self.screenobj.blit(text_rendered, text_rect)
        if self.hitbox == 'rect':
            pygame.draw.rect(self.screenobj, self.color, self.rect, border_bottom_left_radius=self.bottom_left_rad, border_bottom_right_radius=self.bottom_right_rad, border_top_right_radius=self.top_right_rad, border_top_left_radius=self.top_left_rad)
            pygame.draw.rect(self.screenobj, self.outline_color, self.rect, width = self.outline_width, border_bottom_left_radius=self.bottom_left_rad, border_bottom_right_radius=self.bottom_right_rad, border_top_right_radius=self.top_right_rad, border_top_left_radius=self.top_left_rad)
            text_rendered = self.fontobject.render(self.text, True, self.text_color)
            text_rect = text_rendered.get_rect(center=self.rect.center)
            self.screenobj.blit(text_rendered, text_rect)
    def is_on_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.hitbox == 'ellipse':
            dx = mouse_pos[0] - self.rect.centerx
            dy = mouse_pos[1] - self.rect.centery
            rx = self.rect.width / 2
            ry = self.rect.height / 2
            return (dx**2) / (rx**2) + (dy**2) / (ry**2) <= 1
        if self.hitbox == 'rect':
            return (mouse_pos[0] > self.pos[0]) and (mouse_pos[0] < self.pos[0] + self.width) and (mouse_pos[1] > self.pos[1]) and (mouse_pos[1] < self.pos[1] + self.height)
class ImgBasedButton:
    def __init__(self, pos, img, screen_obj):
        self.pos = pos
        self.img = img
        self.rendered_image = pygame.image.load(self.img)
        self.screen_obj = screen_obj
        self.width = self.rendered_image.get_width()
        self.height = self.rendered_image.get_height()
        self.origin = pygame.image.load(self.img)
    def draw(self):
        self.screen_obj.blit(self.rendered_image, self.pos)
    def is_on_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        return mouse_pos[0] >= self.pos[0] and mouse_pos[0] <= self.pos[0] + self.width and mouse_pos[1] >= self.pos[1] and mouse_pos[1] <= self.pos[1] + self.height
    def is_clicked(self):
        return self.is_on_hover() and any(pygame.mouse.get_pressed())
    def scale(self, factor):
        genislik, yukseklik = self.origin.get_size()
        new_width = int(genislik * factor)
        new_height = int(yukseklik * factor)
        # Always reload from the file only once
        if not hasattr(self, '_original_loaded'):
            self.origin = pygame.image.load(self.img).convert_alpha()
            self._original_loaded = True
        scaled_image = pygame.transform.scale(self.origin, (new_width, new_height))
        self.rendered_image = scaled_image
        self.width = new_width
        self.height = new_height
class Composter:
    def __init__(self, pos, screen_obj):
        self.img = pygame.image.load(resource_path("assets/composter.png"))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.pos = pos
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.screen = screen_obj
        self.all_coords = []
        self.mask = pygame.mask.from_surface(self.img)
        self.origin = self.img
    def draw(self):
        self.update()
        self.screen.blit(self.img, self.hitbox)
    def update(self):
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
    def scale(self, factor):
        genislik, yukseklik = self.origin.get_size()
        self.img = pygame.transform.scale(self.img, (int(genislik * factor), int(yukseklik * factor)))
        self.width *= factor
        self.height *= factor
        self.width = int(self.width)
        self.height = int(self.height)
        self.all_coords = []
        self.mask = pygame.mask.from_surface(self.img)
class Item:
    def __init__(self):
        self.pos = [random.randint(-20,720), 0]
        self.type = random.choice(img_files)
        self.good = point_dict[self.type] > 0
        self.img = pygame.image.load(self.type)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.all_coords = []
        self.origin = self.img
        self.scale_number = 1
        self.mask =  pygame.mask.from_surface(self.img)
        self.caught = False
    def draw(self):
        screen.blit(self.img, self.pos)
    def scale(self, factor):
        genislik, yukseklik = self.origin.get_size()
        self.img = pygame.transform.scale(self.img, (int(genislik * factor), int(yukseklik * factor)))
        self.width *= factor
        self.height *= factor
        self.width = int(self.width)
        self.height = int(self.height)
        self.scale_number = factor
        self.mask = pygame.mask.from_surface(self.img)
    def has_overlap(self):
        return self.mask.overlap(composter.mask, (self.pos[0] - composter.pos[0], self.pos[1] - composter.pos[1]))
class Counter:
    def __init__(self):
        self.font = pygame.font.SysFont("Comic Sans", 30)
        self.text = ""
    def render_point(self, points, pos):
        points = str(points)
        self.text = "Puan: " + points
        rendered = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(rendered, pos)
class Timer:
    def __init__(self):
        self.font = pygame.font.SysFont("Comic Sans", 30)
        self.text = ""
    def render_time(self, time_left, pos):
        minutes = f"{time_left // 60}"
        seconds = f"{time_left % 60}"
        if int(minutes) < 10:
            minutes = "0" + minutes
        if int(seconds) < 10:
            seconds = "0" + seconds
        self.text = " Kalan Zaman: " + minutes + ":" + seconds
        rendered = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(rendered, pos)
def pause(is_paused):
    pause_button.img = resource_path("assets/start.png")
    pause_button.origin = pygame.image.load(pause_button.img)
    pause_button.scale(5 / 128)
    big_font = pygame.font.SysFont("Comic Sans", 80)
    paused_text = big_font.render("DURDURULDU", True, (0, 0, 0))
    paused_rect = paused_text.get_rect(center=(width // 2, height // 2))
    while is_paused:
        for event in pygame.event.get():
            if event.type == 256:
                save()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    is_paused = False
        if pause_button.is_clicked():
            is_paused = False
            while pause_button.is_clicked():
                for event in pygame.event.get():
                    if event.type == 256:
                        save()
                        sys.exit()
        screen.fill((255, 255, 255))
        pause_button.draw()
        screen.blit(paused_text, paused_rect)
        pygame.display.update()
    pause_button.img = resource_path("assets/pause.png")
    pause_button.origin = pygame.image.load(pause_button.img)
    pause_button.scale(5 / 128)
    return


marketplace_button = Button((450, 450), screen, font, text = "Market", outline_width = 2, hitbox = "ellipse", width = 140)
test_button = Button((100, 400), screen, font, text="Test", outline_width = 2, hitbox = 'ellipse')
play_button = Button((350, 400), screen, font, text="Oyna", outline_width = 2, hitbox = 'ellipse')
how_to_play_button = Button((600, 400), screen, font, text="Nasıl Oynanır?", outline_width = 2, width=150, hitbox = 'ellipse')
# Add update button
update_button = Button((350, 500), screen, font, text="Güncelleme", outline_width=2, hitbox='ellipse', width=140)
how_to_play_text1 = font.render('Oynamak için "Oyna" butonuna tıklayın. İyi şeyleri yakalayın, kötü şeyleri yakalamayın.', True, (0, 0, 0))
how_to_play_text2 = font.render('Kompost kutusunu sola ve sağa hareket ettirmek için okları kullanın. Puan kazanacak ve', True, (0, 0, 0))
how_to_play_text3 = font.render('kaybedeceksiniz. Doğruluğunuzu test etmek için "Test" düğmesine tıklayın. Hızlandırı-', True, (0, 0, 0))
how_to_play_text4 = font.render('cılarınızı kullanmak için boşluk tuşuna basın.', True, (0, 0, 0))
pause_button = ImgBasedButton((5, 60), resource_path("assets/pause.png"), screen)
pause_button.scale(5 / 128)
main_menu_composter2 = pygame.image.load(resource_path("assets/composter.png"))
main_menu_composter = pygame.transform.scale(main_menu_composter2, (400, 400))
main_menu_composter_rect = main_menu_composter.get_rect(center=(width // 2, height // 3))
composter = Composter([360, 700], screen)
high_scores_button = Button((200, 450), screen, font, text="Yüksek Skorlar", outline_width = 2, hitbox = 'ellipse', width = 160)
exit_button = ImgBasedButton((5, 0), resource_path("assets/arrow.png"), screen)
speed_purchase = Button((300, 400), screen, font, 10, 10, 10, 10, "rect", 125, 25, "400 Coins")
composter.scale(25 / 512)
exit_button.scale(5 / 128)
counter = Counter()
timer = Timer()
items = []

# Run update script if it exists
update_script = os.path.join(script_dir, "extra-scripts", "update.py")
if os.path.isfile(update_script):
    subprocess.run([sys.executable, update_script])

while run:
    for event in pygame.event.get():
        if event.type == 256:
            save()
            sys.exit()
    screen.fill((255, 255, 255))
    if in_main_menu:
        test_button.draw()
        play_button.draw()
        marketplace_button.draw()
        screen.blit(main_menu_composter, main_menu_composter_rect)
        how_to_play_button.draw()
        high_scores_button.draw()
        update_button.draw()
        pygame.display.update()
        if marketplace_button.is_clicked():
            in_loop = True
            while in_loop:
                screen.fill((255, 255, 255))
                for event in pygame.event.get():
                    if event.type == 256:
                        save()
                        sys.exit()
                if exit_button.is_clicked():
                    in_loop = False
                exit_button.draw()
                coin_text = coin_text_font.render(str(money), True, (0, 0, 0))
                coin_rect = coin_text.get_rect()
                point_text = coin_text_font.render(str(points_2), True, (0, 0, 0))
                point_rect = point_text.get_rect()
                speed_text = coin_text_font.render(str(speed_boosts_left), True, (0, 0, 0))
                speed_rect = speed_text.get_rect()
                screen.blit(coin_text, (700, 25))
                coin_rect.topleft = (700, 25)
                screen.blit(coin_img, coin_rect.topright)
                point_rect.topleft = (700, 75)
                screen.blit(point_text, (700, 75))
                screen.blit(point_img, point_rect.topright)
                screen.blit(speed_text, (700, 125))
                speed_rect.topleft = (700, 125)
                screen.blit(speed_img, speed_rect.topright)
                screen.blit(speed_img, (300, 300))
                speed_purchase.draw()
                if speed_purchase.is_clicked():
                    if money >= 400:
                        money -= 400
                        speed_boosts_left += 1
                        while speed_purchase.is_clicked():
                            for event in pygame.event.get():
                                if event.type == 256:
                                    save()
                                    sys.exit()
                pygame.display.update()
        if high_scores_button.is_clicked():
            WFC = True
            h_s_text = font.render(f"Yüksek Skor: {fixed_max(scores)}", True, (0, 0, 0))
            h_p_text = font.render(f"Yüksek Yüzde: {fixed_max(percentages)}", True, (0, 0, 0))
            while WFC:
                for event in pygame.event.get():
                    if event.type == 256:
                        save()
                        sys.exit()

                screen.fill((255, 120, 0))
                screen.blit(h_s_text, (350, 400))
                screen.blit(h_p_text, (350, 350))

                exit_button.draw()
                if exit_button.is_clicked():
                    WFC = False
                    in_main_menu = True

                pygame.display.update()
        if how_to_play_button.is_clicked():
            in_main_menu = False
            screen.fill((255, 255, 255))
            screen.blit(how_to_play_text1, (0, 70, 200, 800))
            screen.blit(how_to_play_text2, (0, 95, 200, 800))
            screen.blit(how_to_play_text3, (0, 120, 200, 800))
            screen.blit(how_to_play_text4, (0, 145, 200, 800))
            exit_button.draw()
            pygame.display.update()
            while not exit_button.is_clicked():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        save()
                        sys.exit()
            in_main_menu = True
        if play_button.is_clicked():
            game = True
            points = 0
            ticks = 0
            start = pygame.time.get_ticks()
            while game:
                ticks += 1
                for event in pygame.event.get():
                    if event.type == 256:
                        save()
                        sys.exit()
                    if event.type == POINT_GET:
                        points += event.point
                        if points < 0:
                            points = 0
                screen.fill((255, 255, 255))
                keys = pygame.key.get_pressed()
                boost_factor = 2 if speed_boost_activated else 1
                if keys[pygame.K_RIGHT]:
                    composter.pos[0] += boost_factor
                if keys[pygame.K_LEFT]:
                    composter.pos[0] -= boost_factor
                if keys[pygame.K_SPACE]:
                    if not speed_boost_activated:
                        speed_boost_activated = True
                        speed_boosts_left -= 1
                if composter.pos[0] < 5:
                    composter.pos[0] = 5
                elif composter.pos[0] + composter.width > 795:
                    composter.pos[0] = 795 - composter.width
                composter.draw()
                pause_button.draw()
                if pause_button.is_clicked():
                    pause(True)
                if ticks == 400:
                    items.append(Item())
                    ticks = 0
                for item in items:
                    if not item.scale == 3 / 40:
                        item.scale(3/40)
                    if item.type == "assets/coin.png":
                        money += 1
                    item.pos[1] += 1
                    if item.pos[1] > 750:
                        del items[items.index(item)]
                    if item.has_overlap():
                        del items[items.index(item)]
                        pygame.event.post(pygame.event.Event(POINT_GET, {"point" : point_dict[item.type]}))
                    item.draw()
                counter.render_point(points, (50, 30))
                if 60 - ((pygame.time.get_ticks() - start) // 1000) == 0:
                    money += int((5 * points) / 2)
                    speed_boost_activated = False
                    points_2 += points
                    in_main_menu = True
                    scores.append(points)
                    high_score = str(max(scores))
                    high_score_text = font.render(f"Yüksek Skor: {high_score}", True, (0, 0, 0))
                    start2 = pygame.time.get_ticks()
                    waiting = True
                    score = font.render(f"Skor: {points}", True, (0, 0, 0))
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == 256:
                                save()
                                sys.exit()
                        screen.fill((64, 224, 208))
                        screen.blit(score, (400, 400))
                        screen.blit(high_score_text, (400, 450))
                        if (pygame.time.get_ticks() - start2) // 1000 == 10:
                            game = False
                            break
                        pygame.display.update()
                    waiting = False
                    break
                timer.render_time(60 - ((pygame.time.get_ticks() - start) // 1000), (500, 30))
                pygame.display.update()
        if test_button.is_clicked():
            game = True
            total_items = 0
            correct_items_caught = 0
            ticks = 0
            start = pygame.time.get_ticks()
            while game:
                ticks += 1
                for event in pygame.event.get():
                    if event.type == 256:
                        save()
                        sys.exit()
                screen.fill((255, 255, 255))
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:
                    composter.pos[0] += 1
                if keys[pygame.K_LEFT]:
                    composter.pos[0] -= 1
                if composter.pos[0] < 5:
                    composter.pos[0] = 5
                elif composter.pos[0] + composter.width > 795:
                    composter.pos[0] = 795 - composter.width
                composter.draw()
                pause_button.draw()
                if pause_button.is_clicked():
                    pause(True)
                if ticks == 400:
                    item = Item()
                    items_existed.append(item)
                    items.append(item)
                    total_items += 1
                    ticks = 0
                for item in items:
                    if not item.scale == 3 / 40:
                        item.scale(3/40)
                    item.pos[1] += 1
                    if item.pos[1] > 750:
                        del items[items.index(item)]
                    if item.has_overlap():
                        items[items.index(item)].caught = True
                        del items[items.index(item)]
                    item.draw()
                if 60 - ((pygame.time.get_ticks() - start) // 1000) == 0:
                    in_main_menu = True
                    for item in items_existed:
                        if item.caught:
                            if item.good:
                                correct_items_caught += 1
                        else:
                            if not item.good:
                                correct_items_caught += 1
                    score = (100 * correct_items_caught) // total_items
                    percentages.append(score)
                    max_per = max(percentages)
                    max_per_text = font.render(f"Yüksek Yüzde: {max_per}", True, (0, 0, 0))
                    start2 = pygame.time.get_ticks()
                    waiting = True
                    score_text = font.render(f"Yüzde: {score}", True, (0, 0, 0))
                    items_existed = []
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == 256:
                                save()
                                sys.exit()
                        screen.fill((64, 224, 208))
                        screen.blit(score_text, (400, 400))
                        screen.blit(max_per_text, (400, 450))
                        if (pygame.time.get_ticks() - start2) // 1000 == 10:
                            game = False
                            break
                        pygame.display.update()
                    waiting = False
                    break
                timer.render_time(60 - ((pygame.time.get_ticks() - start) // 1000), (500, 30))
                pygame.display.update()
        if update_button.is_clicked():
            update_script = os.path.join(script_dir, "extra-scripts", "update.py")
            if os.path.isfile(update_script):
                subprocess.run([sys.executable, update_script])
        test_button.draw()
        play_button.draw()
        how_to_play_button.draw()
        update_button.draw()
    if run:
        pygame.display.update()