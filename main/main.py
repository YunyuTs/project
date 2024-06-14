import pygame
from game import game_play
from choose_character import choose_color
from finish import finish

#設定標題
pygame.display.set_caption("Poko")

def main():
    repeat = 5
    while repeat: #1:重複 2:回首頁 3:P1 win 4:P2 win
        if repeat == 2 or repeat == 5:
            choice = choose_color()
            repeat = 1
            continue
        elif repeat == 3:
            if finish(1) == 0:
                repeat = 1
            elif finish(1) == 1:
                repeat = 2
            else:
                break
        elif repeat == 4:
            if finish(0) == 0:
                repeat = 1
            elif finish(0) == 1:
                repeat = 2
            else:
                break
        while repeat == 1:
            repeat = game_play(choice)
        


if __name__ == "__main__":
    main()