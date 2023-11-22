import pygame
import sys
import random
import math

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
        self.speed = 50

    def reset_speed(self):
        self.speed = 10

class Ball:
    def __init__(self, x):
        self.radius = 40
        self.color = (255, 255, 255)
        self.x = x
        self.y = 0
        self.speed = 10

    def move(self):
        self.y += self.speed

    def create_ball(self, main_screen):
        pygame.draw.circle(main_screen, self.color, (self.x, self.y), self.radius)

#스프라이트를 이용해 공이 플레이어에 닿았을 때 사라지며 이펙트가 나타나게 함.
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

def check_collision(catcher, balls, effect_group):
    catcher_rect = pygame.Rect(catcher.x, catcher.y, catcher.rect.width, catcher.rect.height)
    for ball in balls:
        ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, 2 * ball.radius, 2 * ball.radius)
        if catcher_rect.colliderect(ball_rect):
            #이펙트를 공을 10개 소환 (공이 10개가 생성되고 퍼져나가는 이펙트 생성)
            for _ in range(10):
                effect = Effect(ball_rect.center)
                effect_group.add(effect)
            balls.remove(ball)
        elif ball.y > 800:  # 화면 아래로 벗어난 경우
            balls.remove(ball)

def main():
    pygame.init()

    # 화면 설정
    width, height = 1500, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("비트 캐쳐!")

    clock = pygame.time.Clock()

    image_load = Catcher("catcher.png")

    # 공이 떨어지고 딜레이를 주기 위한 변수
    timer = 0

    # 몇 번째 공이 떨어져야 하는지에 대한 변수
    balls = []
    #이펙트 그룹 생성
    effect_group = pygame.sprite.Group()

    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 키 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            image_load.move_left()
        if keys[pygame.K_RIGHT]:
            image_load.move_right()
        # 스페이스바 누르면 속도가 빨라짐. 함수정보는 Catcher 클래스에 있음
        if keys[pygame.K_SPACE]:
            image_load.power_move()
        # 스페이스바 뗄 시 속도가 원래대로 돌아옴
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                image_load.reset_speed()
        
        position = random.randint(80, 1420)

        # 화면 업데이트
        screen.fill((0, 0, 0))  # 배경은 검은색으로
        screen.blit(image_load.image, (image_load.x, image_load.y))

        # 3초마다 원을 생성
        if timer % 180 == 0:
            balls.append(Ball(position))

        # 실시간으로 공의 갯수를 세고 공의 갯수만큼 공이 떨어지도록 만듬
        if len(balls) > 0:
            for i in balls:
                i.create_ball(screen)
                i.move()

        # 충돌 확인
        check_collision(image_load, balls, effect_group)

        #이펙트를 화면에 나타내고 업데이트 함
        effect_group.draw(screen)
        effect_group.update()

        pygame.display.flip()
        clock.tick(60)  # 초당 60프레임으로 설정
        timer += 1

if __name__ == "__main__":
    main()




