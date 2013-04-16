#!/usr/bin/python

import sys
import Image
import ImageDraw
import math
import random
from collections import defaultdict

def funcion():
  root = Tkinter.Tk()
	root.title("Elipses")
	root.mainloop()

def convolucion(im, g):
  w, h = im.size
  pix = im.load()
  salida = Image.new("RGB", (w, h))
  out = salida.load()
  for i in xrange(1, w-2):
    for j in xrange(1, h-1):
      suma1, suma2, suma3 = 0, 0, 0
      for n in xrange(i-1, i+2):
        for m in xrange(j-1, j+2):
            if n >= 0 and m >= 0 and n < w and m < h:
              suma1 += g[n - (i - 1)][ m - (j - 1)] * pix[n, m][0]
              suma2 += g[n - (i - 1)][ m - (j - 1)] * pix[n, m][1]
              suma3 += g[n - (i - 1)][ m - (j - 1)] * pix[n, m][2]
      out[i, j] = suma1, suma2, suma3
  return salida
 
def bfs(im, origen, color):
  pix = im.load()
  w, h = im.size
  q = []
  coords = []
  q.append(origen)
  original = pix[origen]
  n = 0
  while len(q) > 0:
    (x, y) = q.pop(0)
    actual = pix[x, y]
    if actual == original or actual == color:
      for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
          i, j = (x + dx, y + dy)
          if i >= 0 and i < w and j >= 0 and j < h:
            contenido = pix[i, j]
            if contenido == original:
              pix[i, j] = color
              coords.append((i, j))
              n += 1
              q.append((i, j))
  im.save("sali.png")
  return n, coords
 
def distancia((x1, y1), (x2, y2)):
  return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
 
def encontrar(im, elipse, Gx, Gy):
  list = {}
  pix = im.load()
  for point in elipse:
    r, g, b = Gx[point]
    gx = (r+g+b)/3
    r, g, b = Gy[point]
    gy = (r+g+b)/3
    if (gx, gy) not in list:
      list[(gx, gy)] = []
      list[(gx, gy)].append(point)
    else:
      list[(gx, gy)].append(point)
  acumulator = defaultdict(int)
  for key in list:
    curr = list[key]
    N = len(curr)
    for i in range(N):
      x1, y1 = curr[i]
      x2, y2 = curr[N - i - 1]
      m1, m2 = (x1 +x2)/2, (y1 + y2)/2
      if pix[m1, m2] != (255, 255, 255):
        acumulator[m1, m2] += 1
  frec = sorted(acumulator.items(), key=lambda x: x[1], reverse = True)
  return frec[0][0]
 
def puntos(p, line):
  for coords in line:
    if p == coords:
      return True
  return False
 
def fix_axis(center, (p1, p2)):
  xc, yc = center
  if distancia((p1[0], 0), (p2[0], 0)) > distancia((0, p1[1]), (0, p2[1])):
    out1 = (p1[0], yc)
    out2 = (p2[0], yc)
    axis = 'x'
  else:
    out1 = (xc, p1[1])
    out2 = (xc, p2[1])
    axis = 'y'
  return (out1, out2), axis
  
def get_bounding_box(x, y):
  ymax, ymin = 0, 10000
  xmax, xmin = 0, 10000
  for points in x:
    if points[0] > xmax:
      xmax = points[0]
    if points[0] < xmin:
      xmin = points[0]
    if points[1] > ymax:
      ymax = points[1]
    if points[1] < ymin:
      ymin = points[1]
  for points in y:
    if points[0] > xmax:
      xmax = points[0]
    if points[0] < xmin:
      xmin = points[0]
    if points[1] > ymax:
      ymax = points[1]
    if points[1] < ymin:
      ymin = points[1]
  return (xmin, ymin, xmax, ymax)
 
def ejes(im, list, center):
  w, h = im.size
  distances = defaultdict(int)
  for key in list:
    curr = list[key]
    N = len(curr)
    for i in range(N):
      x1, y1 = curr[i]
      x2, y2 = curr[N - i - 1]
      temp = Image.new('RGB', (w, h))
      draw = ImageDraw.Draw(temp)
      draw.line(((x1, y1), (x2, y2)), (255, 255, 255))
      _, line = bfs(temp, (x1, y1), (255, 0, 0))    
      if puntos(center, line):
        distances[(x1, y1), (x2, y2)] = distancia((x1, y1), (x2, y2))       
  frec = sorted(distances.items(), key=lambda x: x[1], reverse = True)
  coords, axis = fix_axis(center, frec[0][0])
  if axis == 'x':
    x = coords
    y, _ = fix_axis(center, frec[len(frec) - 1][0])
  else:
    y = coords
    x, _ = fix_axis(center, frec[len(frec) - 1][0])
  bounding_box = get_bounding_box(x, y)
  return x, y, bounding_box
 
def color():
  return (random.randint(200, 255), random.randint(63, 132), random.randint(0, 71))
 
def validar(elipse, temp):
  pix = temp.load()
  w, h = temp.size
  end = False
  for i in range(w):
    if end: break
    for j in range(h):
      if pix[i, j] is not (0, 0, 0):
        _, coords = bfs(temp, (i, j), (255, 0, 0))
        end = True
        break
  c = 0
  for point in coords:
    for p in elipse:
      if p == point:
        c += 1
  total = len(elipse)
  porcentaje = (c / float(total) ) * 100.0
  if porcentaje < 80.0:
    return True
  else:
    return False 

"""
def deteccion(im, bordes, (gradx, grady)):
  w, h = im.size
  elipses = []
  tmp = bordes.copy()
  out = tmp.load()
  salida = im.copy()
  for i in range(w):
    for j in range(h):
      if out[i, j] == (255, 255, 255):
        n, coords = bfs(tmp, (i, j), (255, 0, 0))
        elipses.append(coords)
  Gx = gradx.load()
  Gy = grady.load()
  draw = ImageDraw.Draw(salida)
  pix = salida.load()
  i = 1
  diagonal = distancia((0, 0), (w-1, h-1))
  for elipse in elipses:
    M, list = encontrar(bordes, elipse, Gx, Gy)
    x, y, bb = ejes(im, list, M)
    temp = Image.new('RGB', (w, h))
    temp_draw = ImageDraw.Draw(temp)
    temp_draw.ellipse(bb, outline = (255, 255, 255))
    if validar(elipse, temp):
      dist1 = distancia(x[0], x[1])
      dist2 = distancia(y[0], y[1])
      draw.ellipse(bb, outline = color())
      pix[M] = (0, 0, 255)
      i += 1
"""
	  
def main():
	function()

im = Image.open(sys.argv[1]).convert('RGB')

sobelx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
sobely = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

ambas = [[1, 3, 3,], [-3, -2, 3], [-3, -3, 1]]

gradx = convolucion(im, sobelx)
grady = convolucion(im, sobely)

"""
#bordes = convolucion(im, ambas)
#deteccion(im, bordes, (gradx, grady))
"""
