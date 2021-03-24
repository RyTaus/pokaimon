from pprint import pprint
import time
import keyboard

import retro

import environment

e = environment.E("./PokemonBlue.gb")
print(e.buttons)
print(dir(e))
while True:
  time.sleep(1.0 / 59.7275)
  ram = e.step(keyboard.is_pressed("q"))
  # print(ram.size)
  # print(ram[0xFF80 - 0xA000:0xFFB4 - 0xA000])
  print(ram[0xFF8A - 0xC000])
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