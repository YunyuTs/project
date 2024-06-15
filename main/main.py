import pygame
from game import game_play
from choose_character import choose_color
from finish import finish
from open_anime import start_page

#設定標題
pygame.display.set_caption("Poko")

#音樂
pygame.mixer.init()

def main():
    repeat = 5
    go_on = -1
    while repeat: #1:重複 2:回首頁 3:P1 win 4:P2 win
        if repeat == 2 or repeat == 5:
            start = start_page()
            if start == 0:
                break
            choice = choose_color()
            repeat = 1
            continue
        elif repeat > 2:
            pygame.mixer.music.load("src/sound/victory_sound.mp3")
            pygame.mixer.music.play()
            go_on = finish(4 - repeat, choice[0])
            pygame.mixer.music.stop()

        if go_on == 1:
            repeat = 2
            go_on = -1
        elif go_on == 2:
            repeat = 1
            go_on = -1
        elif go_on == 0:
            break

        while repeat == 1:
            repeat = game_play(choice)
        


if __name__ == "__main__":
    main()