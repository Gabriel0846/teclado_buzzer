import pygame
import time
import numpy as np

# Inicializa o mixer e a janela do pygame
pygame.init()
pygame.mixer.init()

# Mapeia as teclas do teclado do computador para frequências das notas
key_to_frequency = {
    pygame.K_a: 261.63,  # C4
    pygame.K_s: 293.66,  # D4
    pygame.K_d: 329.63,  # E4
    pygame.K_f: 349.23,  # F4
    pygame.K_g: 392.00,  # G4
    pygame.K_h: 440.00,  # A4
    pygame.K_j: 493.88,  # B4
    pygame.K_k: 523.25,  # C5
}

# Função para tocar uma nota
def generate_tone(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(frequency * t * 2 * np.pi)
    return (tone * (2**15 - 1) / np.max(np.abs(tone))).astype(np.int16)

def play_tone(frequency, duration, sustain):
    sample_rate = 44100
    if sustain:
        duration = 10  # Extende a duração para 10 segundos ou até o pedal ser liberado
    tone = generate_tone(frequency, duration)
    sound = pygame.sndarray.make_sound(tone)
    sound.play(-1)
    return sound

# Cria uma janela do pygame
screen = pygame.display.set_mode((300, 200))
pygame.display.set_caption("Teclado Musical")

# Loop principal
running = True
sustain = False
playing_sounds = {}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sustain = True
            elif event.key in key_to_frequency and event.key not in playing_sounds:
                frequency = key_to_frequency[event.key]
                sound = play_tone(frequency, 0.5, sustain)
                playing_sounds[event.key] = sound
            elif event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                sustain = False
                for sound in playing_sounds.values():
                    sound.fadeout(500)
                playing_sounds.clear()
            elif event.key in playing_sounds:
                sound = playing_sounds[event.key]
                if not sustain:
                    sound.fadeout(500)  # Fade out in 500ms
                    del playing_sounds[event.key]

pygame.quit()
