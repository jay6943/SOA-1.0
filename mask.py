import cfg
import dxf
import dev
import soa
import amp
import lds
import key

if __name__ == '__main__':

  x1, y1 = 3700, 3000
  x2, y2 = x1, 12745

  for layer in ['active','active-0.6','active-1.0']:
    x2, _ = lds.chips(layer, x1, y1)
    for _ in range(3): x2, _ = soa.chips(layer, x2, y1)
    x2, _ = lds.chips(layer, x2, y1)

    x2, _ = lds.chips(layer, x1, y2)
    x2, _ = soa.chips(layer, x2, y2)
    x2, _ = amp.chips(layer, x2, y2)
    x2, _ = soa.chips(layer, x2, y2)
    x2, _ = lds.chips(layer, x2, y2)

  dxf.rects('block', 1000, 1000, 30000, 22000)

  key.chips(0, 0)

  dxf.circle('wafer', 0, 0, cfg.size, 0, 90, 91)
  dxf.circle('wafer', cfg.size, 0, cfg.size, 90, 180, 91)

  dev.saveas('SOA V0.1')