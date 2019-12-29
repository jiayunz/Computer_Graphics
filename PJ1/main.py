import pyaudio
import wave
import numpy as np
import pygame
import math
import librosa
import sys

nframes = 1024
bar_width = 5
window_width = 512
window_height = 300
step = max(1, int(math.ceil(nframes * 2 / (window_width / bar_width))))

colors = [
    (145, 18, 133),
    (166, 18, 140),
    (196, 28, 147),
    (229, 74, 166),
    (248, 143, 186),
    (253, 187, 201),
    (253, 221, 222),
    (253, 187, 201),
    (248, 143, 186),
    (229, 74, 166),
    (196, 28, 147),
    (166, 18, 140),
    (145, 18, 133),
    (83, 18, 112)
]

def play_music(argv):
    if not len(argv):
        music_file = "swan_lake.wav"
    else:
        music_file = argv[0]

    p = pyaudio.PyAudio()
    with wave.open(music_file, 'rb') as wf:
        # 打开音乐并播放
        stream = p.open(
            format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )
        # 读取音频数据
        data = wf.readframes(nframes)
        pygame.init()
        pygame.display.set_caption('music visualization')
        screen = pygame.display.set_mode((window_width, window_height), 0, 32)

        # 获取节奏点
        y, sr = librosa.load(music_file)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

        iter = 0
        # 当音乐还未结束
        while data != '':
            stream.write(data)
            # 继续读取音频数据
            data = wf.readframes(nframes)
            # 傅里叶变换，将一个信号变换到频域
            data_fft = np.real(np.fft.fft(np.fromstring(data, dtype=np.int16)))
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            for n in range(0, data_fft.size, step):
                bar_height = min(abs(int(data_fft[n] * 1e-4)), 0.4 * window_height)
                # 根据节奏点增大bar_height，达到可视化节奏效果
                if iter in beat_frames:
                    bar_height = min(bar_height + 5, 0.4 * window_height)
                pygame.draw.rect(screen, colors[int(n / data_fft.size * len(colors) - iter / 2) % len(colors)], pygame.Rect((bar_width * n / step, window_height / 2), (bar_width / 2, bar_height)))
                pygame.draw.rect(screen, colors[int(n / data_fft.size * len(colors) - iter / 2) % len(colors)], pygame.Rect((bar_width * n / step, window_height / 2), (bar_width / 2, -bar_height)))

            pygame.display.update()
            iter += 1

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == '__main__':
    play_music(sys.argv[1:])