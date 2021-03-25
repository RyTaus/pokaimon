from pprint import pprint
import time
import keyboard

import numpy as np

# import retro

import environment

def get_input():
  return np.array([
    keyboard.is_pressed("o"),
    False,
    keyboard.is_pressed("n"),
    keyboard.is_pressed("m"),
    keyboard.is_pressed("w"),
    keyboard.is_pressed("s"),
    keyboard.is_pressed("a"),
    keyboard.is_pressed("d"),
    keyboard.is_pressed("p")
  ], dtype=np.uint8)


e = environment.E("./PokemonBlue.gb")
print(e.buttons)
print(dir(e))
while True:
  time.sleep(1.0 / 59.7275)
  ram = e.step(get_input())
  # print(ram)
  print(ram[0xCC26 - 0xA000 + 0x0011])
  # print(ram[0xFF8A - 0xC000])
  # print(keyboard.is_pressed("q"))
  e.render()


# env = retro.make(game='BalloonKid-GameBoy')
# obs = env.reset()
# while True:
#     obs, rew, done, info = env.step(env.action_space.sample())
#     env.render()
#     if done:
#         obs = env.reset()
# env.close()

#80 + 1B 28 bytes off