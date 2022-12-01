import os
import cfg
import dxf
import numpy as np

def edge(layer, x, y, length, width):

  w, g = 10, 5

  x1, y1 = x + g, y + g
  x2, y2 = x - g + length, y - g + width

  dxf.rects(layer, x1, y1, x1 + w, y1 + w)
  dxf.rects(layer, x1, y2, x1 + w, y2 - w)
  dxf.rects(layer, x2, y1, x2 - w, y1 + w)
  dxf.rects(layer, x2, y2, x2 - w, y2 - w)

def metal(layer, x, y, length, width):
  
  g, l, w = 5, 100, 10

  data = [layer]

  data.append([x + g, y + w * 0.5])
  data.append([x + g + l * 0.5, y + width * 0.5])
  data.append([x + length - g - l * 0.5, y + width * 0.5])
  data.append([x + length - g, y + w * 0.5])
  data.append([x + length - g, y - w * 0.5])
  data.append([x + length - g - l * 0.5, y - width * 0.5])
  data.append([x + g + l * 0.5, y - width * 0.5])
  data.append([x + g, y - w * 0.5])

  cfg.data.append(data)

  return x + length, y
  
def arange(start, stop, step):

  return np.arange(start, stop + step * 0.5, step)

def move(idev, x, xp, length):

  ltip = (length - xp + x) * 0.5

  xtip, _ = dxf.move(idev, x, 0, xp, 0, ltip, 0, 0)

  return xtip, ltip

def removes(folder):

  if os.path.isdir(folder):
    
    files = os.listdir(folder)
    
    for fp in files:
      if os.path.exists(folder + fp): os.remove(folder + fp)
    
    os.rmdir(folder)

def saveas(filename):

  fp = dxf.start(filename)
  dxf.conversion(fp)
  dxf.close(fp)

  removes('__pycache__/')