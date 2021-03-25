from pprint import pprint

import queue

import retro
import gym
import time
import pyaudio
from threading import Thread
import numpy as np
import gc
from gym.envs.classic_control.rendering import SimpleImageViewer

class E(gym.Env):

  def _audio_runner(self, data):
    audio_stream = self.audio.open(
      format=pyaudio.paInt8, channels=2, rate=32768, output=True)
    audio_stream.write(data)
    audio_stream.stop_stream()
    audio_stream.close()


  def _get_padded_audio(self, frame_count):
    # Get as much from the buffer as possible.
    idx = 0
    out = np.empty([frame_count, 2], dtype=np.uint8)
    print('======')
    print(frame_count)
    print(self.audio_queue.qsize())
    while True:
      if idx == frame_count - 1:
        break
      try:
        a = self.audio_queue.get_nowait()
        # out[idx] = a
        out[idx] = [200, 200]
        idx += 1
      except queue.Empty:
        break
    
    return out
    # return silence

  def _on_audio_ready(self, in_data, frame_count, time_info, status):
    # return
    return self._get_padded_audio(frame_count), pyaudio.paContinue

  def __init__(self, rom_path):
    self.audio = pyaudio.PyAudio()
    self.audio_queue = queue.Queue()
    # thread = Thread(target=self._audio_runner)
    # thread.run()

    # self.audio_stream.start_stream()

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
    self.em.set_button_mask(action)
    self.em.step()
    self.data.update_ram()
    # for a in self.em.get_audio():
    #   self.audio_queue.put_nowait(a)
    # Thread(target=self._audio_runner, args=[self.em.get_audio()]).run()
    # self.audio_queue.put_nowait(self.em.get_audio())
    # print("added more audio")
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
