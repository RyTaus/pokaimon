from pprint import pprint

import queue

import retro
import gym
import time
import simpleaudio as sa
import pyaudio
from threading import Thread
import numpy as np
import gc
from gym.envs.classic_control.rendering import SimpleImageViewer

class E(gym.Env):
  def __init__(self, rom_path):

    self.data = retro.data.GameData()
    self.viewer = SimpleImageViewer()

    gc.collect()
    self.system = retro.get_romfile_system(rom_path)
    self.em = retro.RetroEmulator(rom_path)
    self.em.configure_data(self.data)

    core = retro.get_system_info(self.system)
    self.buttons = core['buttons']

    self.step_number = 0

    

  def step(self, action):
    self.step_number += 1
    # This should return the current RAM
    # return self.em.r
    self.em.set_button_mask(np.array([1, 0, 1, 1, 0, 0, 0, 0, action], dtype=np.uint8))
    self.em.step()
    self.data.update_ram()
    return self._get_ram()

  def reset(self):
    pass

  def render(self):
    # Also play audio
    # img = self._get_screen() if self.img is None else self.img # cached?
    img = self._get_screen()
    self.viewer.imshow(img)
    

  def close(self):
    pass

  def seed(self, seed=None):
    pass

  def _get_ram(self):
    blocks = []
    for offset in sorted(self.data.memory.blocks):
        arr = np.frombuffer(self.data.memory.blocks[offset], dtype=np.uint8)
        blocks.append(arr)
    return np.concatenate(blocks)

  def _get_screen(self, player=0):
    img = self.em.get_screen()
    x, y, w, h = self.data.crop_info(player)
    if not w or x + w > img.shape[1]:
        w = img.shape[1]
    else:
        w += x
    if not h or y + h > img.shape[0]:
        h = img.shape[0]
    else:
        h += y
    if x == 0 and y == 0 and w == img.shape[1] and h == img.shape[0]:
        return img
    return img[y:h, x:w]
