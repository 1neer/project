import pygame
import sys

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
        self.speed = 20

    def reset_speed(self):
        self.speed = 10

def main():
    pygame.init()

    # 화면 설정
    width, height = 1500, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("비트 캐쳐!")

    clock = pygame.time.Clock()

    image_load = Catcher("catcher.png")

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
        #스페이스바 누르면 속도가 빨라짐. 함수정보는 Catcher 클래스에있음
        if keys[pygame.K_SPACE]:
            image_load.power_move()
        #스페이스바 뗄 시 속도가 원래대로 돌아옴
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                image_load.reset_speed()


        # 화면 업데이트
        screen.fill((0, 0, 0))  # 배경은 검은색으로
        screen.blit(image_load.image, (image_load.x, image_load.y))

        pygame.display.flip()
        clock.tick(60)  # 초당 60프레임으로 설정

if __name__ == "__main__":
    main()






