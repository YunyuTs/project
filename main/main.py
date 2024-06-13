from game import game_play
from choose_character import choose_color

def main():
    repeat = 1
    while repeat: #1:重複 2:回首頁 3:P1 win 4:P2 win
        choice = choose_color()
        if repeat == 2:
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