import cfg
import txt
import numpy as np

def start(filename):

  fp = open(cfg.work + filename + '.dxf', 'w')

  fp.write('0\nSECTION\n')
  fp.write('2\nHEADER\n')
  fp.write('0\nENDSEC\n')
  fp.write('0\nSECTION\n')
  fp.write('2\nTABLES\n')
  fp.write('0\nENDSEC\n')
  fp.write('0\nSECTION\n')
  fp.write('2\nENTITIES\n')

  return fp

def polyline(fp, layer):

  fp.write('0\nPOLYLINE\n')
  fp.write('8\n' + layer + '\n')
  fp.write('66\n1\n')
  fp.write('10\n0\n')
  fp.write('20\n0\n')
  fp.write('70\n1\n')
  
def vertex(fp, layer, x, y):

  xstr = str(round(x, 6))
  ystr = str(round(y, 6))

  if xstr[-2:] == '.0': xstr = xstr[:-2]
  if ystr[-2:] == '.0': ystr = ystr[:-2]

  fp.write('0\nVERTEX\n8\n' + layer + '\n')
  fp.write('10\n' + xstr + '\n')
  fp.write('20\n' + ystr + '\n')
  
def seqend(fp, layer):

  fp.write('0\nSEQEND\n')
  fp.write('8\n' + layer + '\n')

def close(fp):

  fp.write('0\nENDSEC\n')
  fp.write('0\nEOF\n')

  fp.close()

def conversion(fp):

  for device in cfg.data:

    layer = device[0]

    if layer in cfg.layer:
      polyline(fp, layer)
      for [x, y] in device[1:]: vertex(fp, layer, x, y)                    
      seqend(fp, layer)

    else: print('There is NO layer ----', layer, '----')

  cfg.data.clear()

def rxt(angle):
  
  arg = angle * np.pi / 180

  rcos = np.cos(arg)
  rsin = np.sin(arg)

  return np.array([[rcos, -rsin], [rsin, rcos]])
  
def rotate(xp, yp, angle):

  [xp, yp] = rxt(angle) @ np.array([xp, yp])

  return xp, yp

def move(idev, x, y, xp, yp, dx, dy, angle):

  for data in cfg.data[idev:len(cfg.data)]:
    xy = np.array(data[1:]).transpose()
    
    if angle != 0:
      xy = rxt(angle) @ xy
      s = rxt(angle) @ [[x], [y]]
      t = rxt(angle) @ [[xp], [yp]]
    else:
      s = [[x], [y]]
      t = [[xp], [yp]]
    
    px = x - s[0][0] + dx
    py = y - s[1][0] + dy
    
    xy = xy.transpose() + [px, py]
    
    data[1:] = xy.tolist()
  
  return t[0][0] + px, t[1][0] + py

def circle(layer, x, y, radius, start, stop, n):

  t = np.linspace(start, stop, n) * np.pi / 180

  xp = x + radius * np.cos(t)
  yp = y + radius * np.sin(t)

  data = np.array([xp, yp]).transpose()
  cfg.data.append([layer] + data.tolist() + [[x, y]])

  return x, y

def rects(layer, x1, y1, x2, y2):

  data = [layer]

  data.append([x1, y1])
  data.append([x2, y1])
  data.append([x2, y2])
  data.append([x1, y2])

  cfg.data.append(data)

  return x2, y2

def crect(layer, x, y, length, width):

  l = length * 0.5
  w = width * 0.5

  data = [layer]

  data.append([x - l, y - w])
  data.append([x + l, y - w])
  data.append([x + l, y + w])
  data.append([x - l, y + w])

  cfg.data.append(data)

  return x + length, y

def srect(layer, x, y, length, width):

  w = width * 0.5

  data = [layer]

  data.append([x, y - w])
  data.append([x + length, y - w])
  data.append([x + length, y + w])
  data.append([x, y + w])

  cfg.data.append(data)

  return x + length, y

def taper(layer, x, y, length, wstart, wstop):

  data = [layer]

  data.append([x, y - wstart * 0.5])
  data.append([x + length, y - wstop * 0.5])
  data.append([x + length, y + wstop * 0.5])
  data.append([x, y + wstart * 0.5])

  cfg.data.append(data)

  return x + length, y

def sline(layer, x, y, length):

  srect(layer, x, y, length, cfg.wg)
  
  return x + length, y

def tline(layer, x, y, length):

  w = cfg.wg * 0.5

  crect(layer, x - w, y, x + w, y + length)

  return x, y + length

def tilts(layer, x, y, length, width, angle):

  w = width * 0.5

  xp = np.array([0, length, length, 0])
  yp = np.array([w, w, -w, -w])

  xp, yp = rotate(xp, yp, angle)
  xp, yp = xp + x, yp + y

  data = np.array([xp, yp]).transpose()
  cfg.data.append([layer] + data.tolist())

  return (xp[1] + xp[2]) * 0.5, (yp[1] + yp[2]) * 0.5

def texts(layer, x, y, title, scale, align):

  l = 0
  for c in title: l += txt.size[c] if c in txt.size else 50
  l = (l + 25 * (len(title) - 1)) * scale

  x -= txt.xalign[align[0]] * l
  y -= txt.yalign[align[1]] * scale * 100
  
  for c in title:
    if c in txt.size:
      xp = x + txt.x[c] * scale
      yp = y + txt.y[c] * scale
      data = np.array([xp, yp]).transpose()
      cfg.data.append([layer] + data.tolist())
      x += (txt.size[c] + 25) * scale
    else: x += 50 * scale

  return l, scale * 100