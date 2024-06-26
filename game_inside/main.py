import pygame
from game import game_play
from choose_character import choose_color

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
            print("P1 win")
            break
        elif repeat == 4:
            print("P2 win")
            break
        while repeat == 1:
            repeat = game_play(choice)
        


if __name__ == "__main__":
    main()