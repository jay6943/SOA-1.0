import cfg
import dxf
import dev
import numpy as np

ysize = 500
angle = np.cos(cfg.tilt * np.pi / 180)
slope = np.tan(cfg.tilt * np.pi / 180)

def srect(layer, x, y, length, width):

  w = width * 0.5
  dx = width * slope * 0.5

  data = [layer]

  data.append([x - dx, y - w])
  data.append([x - dx + length, y - w])
  data.append([x + dx + length, y + w])
  data.append([x + dx, y + w])

  cfg.data.append(data)

  return x + length, y

def chip(layer, x, y, length):

  wg, ltip, ltaper, lexpand = 1, 40, 200, 50

  if layer == 'active': wt = 0.8
  if layer == 'active-0.6': wt = 0.6
  if layer == 'active-1.0': wt = 1

  ytilt = (length + ltip) / angle * slope
  lchip = (length + ltip) / angle - (ltip + ltaper + lexpand) * 2

  idev = len(cfg.data)

  x1, y1 = x - ltip * 0.5 / angle, y - (ytilt - ysize) * 0.5
  x2, y2 = dxf.srect(layer, x1, y1, ltip, wt)
  x3, y3 = dxf.taper(layer, x2, y2, ltaper, wt, wg)
  x4, y4 = dxf.taper(layer, x3, y3, lexpand, wg, cfg.wg)
  x5, y5 = dxf.srect(layer, x4, y4, lchip, cfg.wg)
  x6, y6 = dxf.taper(layer, x5, y5, lexpand, cfg.wg, wg)
  x7, y7 = dxf.taper(layer, x6, y6, ltaper, wg, wt)
  x8, y8 = dxf.srect(layer, x7, y7, ltip, wt)
  
  dxf.srect('p-open', x1 + 5, y1, x8 - x1 - 10, 6)
  dxf.srect('ingaas', x1, y1, x8 - x1, 10)
  dev.metal('metal', x, y4, length, 300)
  dev.metal('plate', x, y1, length, 300)
  
  dxf.move(idev, x1, y1, x8, y8, 0, 0, cfg.tilt)

  dev.edge('metal', x, y, length, ysize)

  return x + length, y + ysize

def chips(layer, x, y):

  for i in range(4):
    length = 500 + 500 * i

    for j in range(15):
      x1, y1 = x, y + j * ysize
      x2, y2 = chip(layer, x1, y1, length)

      s = str(length) + '-' + str(j+1)
      dxf.texts('metal', x1 + length * 0.5, y1 + 10, s, 0.5, 'cb')

    x = x2

  return x2, y2

if __name__ == '__main__':

  chips('active', 0, 0)

  dev.saveas('soa')