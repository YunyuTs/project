import pygame
from game import game_play
from pc import pc_game
from pc_hard import pc_hard
from choose_character import choose_color
from finish import finish
from open_anime import start_page
from face_pve import face_pve

#設定標題
pygame.display.set_caption("Tag you're it!")

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
            if start == 1:
                choice = choose_color()
            else:
                choice = face_pve()
            repeat = 1
            continue
        elif repeat > 2:
            pygame.mixer.music.load("src/sound/victory_sound.mp3")
            pygame.mixer.music.play()
            if start == 1:
                go_on = finish(4 - repeat, choice[0], 0)
            else:
                go_on = finish(4 - repeat, choice[0], 1)
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
            if start == 1:
                repeat = game_play(choice)
            elif start == 2:
                repeat = pc_game(choice)
            elif start == 3:
                repeat = pc_hard(choice)
        


if __name__ == "__main__":
    main()