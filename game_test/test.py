from game import game_play

repeat = 1
while repeat:
    repeat = 0
    repeat = game_play()
    if repeat == 3:
        print("P1 win")
    elif repeat == 4:
        print("P2 win")
    if repeat > 1:
        break