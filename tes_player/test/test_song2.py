import pygame

# 初始化 Pygame 和 Mixer
pygame.init()
pygame.mixer.init()

# 加載音樂文件
pygame.mixer.music.load('src/sound/state0.wav')

# 開始播放音樂
pygame.mixer.music.play()

# 等待音樂播放一段時間
pygame.time.delay(100)

# 檢查音樂是否正在播放
while pygame.mixer.music.get_busy():
    print("音樂正在播放...")
    pygame.time.Clock().tick(10)

print("音樂播放完畢")
