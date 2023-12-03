import pygame
import sys
import random
import math
import time
class SongSelection:
    def __init__(self, screen, song_data, selected_song_index):
        self.screen = screen
        self.font = pygame.font.Font("1.ttf", 36)
        self.song_data = song_data
        self.index = selected_song_index  # 현재 선택된 곡의 인덱스
        self.start_button = pygame.Rect(600, 400, 200, 50)
        self.start_text = self.font.render("Start", True, (0, 0, 0))
        self.update_texts()

    def update_texts(self):
        song = self.song_data[self.index]
        print(song)
        composer_text = self.font.render("작곡가:" + song["composer"], True, (255, 255, 255))
        bpm_text = self.font.render("BPM:" + str(song["bpm"]), True, (255, 255, 255))
        difficulty_text = self.font.render("난이도:" + str(song["difficulty"]), True, (255, 255, 255))
        background_image = pygame.image.load(song["bg"]).convert_alpha()
        background_image = pygame.transform.scale(background_image, (400, 200))

        self.texts = [composer_text, bpm_text, difficulty_text]
        self.background_image = background_image

    def draw(self):
        for i, text in enumerate(self.texts):
            self.screen.blit(text, (1000, 150 + i * 50))
        self.screen.blit(self.background_image, (1000, 300))

        # Draw Start Button
        pygame.draw.rect(self.screen, (0, 255, 0), self.start_button)
        self.screen.blit(self.start_text, (650, 415))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.start_button.collidepoint(x, y):
                return True
        return False

class Catcher:
    def __init__(self, imagefile):
        self.image = pygame.image.load(imagefile)
        self.image = pygame.transform.scale(self.image, (200, 100))
        self.rect = self.image.get_rect()
        self.x = 375
        self.y = 700
        self.speed = 10

    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0

    def move_right(self):
        self.x += self.speed
        if self.x > 1300:
            self.x = 1300
    
    def power_move(self):
        self.speed = 30

    def reset_speed(self):
        self.speed = 10

class Ball:
    def __init__(self, x):
        self.radius = 40
        self.color = (255, 255, 255)
        self.x = x
        self.y = -100
        self.speed = 10
        #노트가 타이밍 1초전에 생성됨
        self.note_time = time.time() + 1

    def move(self, Time):
        #self.y += self.speed
        self.time = Time
        self.y = 600 + (self.time - self.note_time) * 600
    def create_ball(self, main_screen):
        pygame.draw.circle(main_screen, self.color, (self.x, self.y), self.radius)

class Effect(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (5, 5), 5)
        self.rect = self.image.get_rect(center=position)
        self.speed = random.uniform(5, 10)
        self.angle = random.uniform(0, 2 * 3.14)
    
    #이펙트의 위치를 업데이트 하는 함수
    def update(self):
        self.rect.x += self.speed * 2 * 3.14 * 0.01 * 15000 * 0.001 * math.cos(self.angle)
        self.rect.y += self.speed * 2 * 3.14 * 0.01 * 15000 * 0.001 * math.sin(self.angle)
        self.speed -= 0.3
        if self.speed <= 0:
            self.kill()

def check_collision(catcher, balls, effect_group, sound):
    catcher_rect = pygame.Rect(catcher.x, catcher.y, catcher.rect.width, catcher.rect.height)
    for ball in balls:
        ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, 2 * ball.radius, 2 * ball.radius)
        if catcher_rect.colliderect(ball_rect):
            #이펙트를 공을 10개 소환 (공이 10개가 생성되고 퍼져나가는 이펙트 생성)
            for _ in range(10):
                effect = Effect(ball_rect.center)
                effect_group.add(effect)
            sound.play()
            balls.remove(ball)
        elif ball.y > 800:  # 화면 아래로 벗어난 경우
            balls.remove(ball)

def play(b, l, t, p):
    pygame.init()

    #화면 설정
    width, height = 1500, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("비트 캐쳐!")

    clock = pygame.time.Clock()

    image_load = Catcher("catcher.png")

    timer = 0
    # 몇 번째 공이 떨어져야 하는지에 대한 변수
    balls = []
    #노트 패턴을 저장하는 배열
    note_position = []
    #비트 저장
    note_bit = []
    #이펙트 그룹 생성
    effect_group = pygame.sprite.Group()

    #여기서부터는 노트정보를 저장한 텍스트파일을 불러와서 배열로 저장하는 부분
    f = open(p, "r")
    data = f.read().splitlines()
    note_data = []
    
    for note in data:
        note_data.append(note.split(','))

    for sublist in note_data:
        note_bit.append(sublist[0])
        note_position.append(sublist[1:])
    
    f.close()

    #노트가 나올 순서 변수
    note_turn = 0

    #비트가 바뀌는 순서 변수
    note_bit_turn = 0
    
    #bpm
    bpm = b

    #곡이 시작한 시간 저장
    start_time = time.time()

    #곡 플레이
    music_phoenix = pygame.mixer.Sound(t)
    music_phoenix.play()
    
    #효과음 저장
    clap = pygame.mixer.Sound("drum-hitclap.ogg")
    
    #곡이 시작되고 음이 나오기 전까지 공백, 측정은 오데시티라는 프로그램 활용
    a = l
    
    #곡이 끝나는 타이밍 재기위한 변수
    second = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            image_load.move_left()
        if keys[pygame.K_RIGHT]:
            image_load.move_right()
        if keys[pygame.K_SPACE]:
            image_load.power_move()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                image_load.reset_speed()

        position = 0
        if note_position[note_bit_turn][note_turn] == '1':
            position = 125
        elif note_position[note_bit_turn][note_turn] == '2':
            position = 375
        elif note_position[note_bit_turn][note_turn] == '3':
            position = 625
        elif note_position[note_bit_turn][note_turn] == '4':
            position = 875
        elif note_position[note_bit_turn][note_turn] == '5':
            position = 1125
        elif note_position[note_bit_turn][note_turn] == '6':
            position = 1375

        screen.fill((0, 0, 0))
        screen.blit(image_load.image, (image_load.x, image_load.y))

        beats_per_measure = int(note_bit[note_bit_turn])
        carculate_beat = beats_per_measure / 4
        spb = 60 / (carculate_beat * bpm)

        time_interval = spb
        elapsed_time = time.time() - start_time
        beats_per_bar = int(note_bit[note_bit_turn])
        spb_bar = 60 * beats_per_bar * spb
        note_Time = time.time()

        if elapsed_time >= time_interval - a:
            if note_position[note_bit_turn][note_turn] != '0':
                balls.append(Ball(position))
            note_turn += 1
            if note_turn >= len(note_position[note_bit_turn]):
                note_turn = 0
                note_bit_turn += 1
            start_time = time.time()
            a = 0

        if len(balls) > 0:
            for i in balls:
                i.create_ball(screen)
                i.move(note_Time)

        check_collision(image_load, balls, effect_group, clap)

        effect_group.draw(screen)
        effect_group.update()

        pygame.display.flip()
        clock.tick(60)
        timer += 1
        if timer % 60 == 0:
            second += 1
        print(second)

        if second >= 88:
            music_phoenix.fadeout(3000)
        if second >= 92:
            pygame.quit()


def main():
    pygame.init()
    width, height = 1500, 800
    pygame.display.set_caption("비트 캐쳐!")
    clock = pygame.time.Clock()

    font = pygame.font.Font("1.ttf",60)
    song_data = [
        {"title": "Phoenix", "composer": "Netrum & Halvorsen", "bpm": 165, "difficulty": 2, "bg": "Phoenix.jpg", "late" : 0.381, "pattern" : "note.txt"},
        {"title": "enchanted love", "composer": "linear ring", "bpm": 95, "difficulty": 3, "bg": "enchanted love.png"},
        # 추가 곡 정보를 필요한 만큼 추가
    ]
    
    while True:
        screen = pygame.display.set_mode((width, height))
        song_name_texts = [font.render(f"곡: {song['title']}", True, (255, 255, 255)) for song in song_data]
        song_name_rects = [text.get_rect(center=(300, 100 + i * 140)) for i, text in enumerate(song_name_texts)]
        for i in range(0, len(song_name_texts)):
            screen.blit(song_name_texts[i], song_name_rects[i])
    
        pygame.display.flip()

        song_selection = None
        waiting_for_click = True
        print("a")
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for i, rect in enumerate(song_name_rects):
                        if rect.collidepoint(x, y):
                            selected_song = i
                            waiting_for_click = False

        if selected_song is not None:
            song_selection = SongSelection(screen, song_data, selected_song)
            song_selection.draw()
    
            pygame.display.flip()

            start_button_clicked = False
            selected_song_button = False
            while not start_button_clicked and not selected_song_button:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos
                        for i, rect in enumerate(song_name_rects):
                            if rect.collidepoint(x, y):
                                selected_song_button = True
                    start_button_clicked = song_selection.handle_event(event)

            pygame.display.flip()
            clock.tick(60)
        if start_button_clicked == True:
            break
    song = song_selection.song_data[song_selection.index]
    bpm = song["bpm"]
    late = song["late"]
    title = song["title"] + ".mp3"
    pattern = song["pattern"]
    bg = song["bg"]
    print(str(bpm) + str(late) + title + pattern + bg)             
    play(bpm, late, title, pattern)

if __name__ == "__main__":
    main()

