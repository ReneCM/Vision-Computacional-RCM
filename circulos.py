import Tkinter
import math
import sys
import os
import random
from PIL import Image, ImageDraw, ImageFont

def funcion():
  root = Tkinter.Tk()
  root.title("Circulos")
  root.mainloop()

def convolucion(im, g):
  w, h = im.size
  pixeles = im.load()
  salida = Image.new("RGB", (w, h))
  sal = salida.load()
  for i in xrange(1, w):
    for j in xrange(h-1):
      suma1, suma2, suma3 = 0, 0, 0
      for n in xrange(i-1, i+2):
        for m in xrange(j-1, j+2):
            if n >= 0 and m >= 0 and n < w and m < h:
              suma1 += g[n - (i - 1)][ m - (j - 1)] * pixeles[n, m][0]
              suma2 += g[n - (i - 1)][ m - (j - 1)] * pixeles[n, m][1]
              suma3 += g[n - (i - 1)][ m - (j - 1)] * pixeles[n, m][2]
      sal[i, j] = suma1, suma2, suma3
  salida.save("bordes1.png")
  return salida

maskx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
masky = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

def distance(p1, p2):
  x1, y1 = p1
  x2, y2 = p2
  return math.sqrt( math.pow((x2 - x1) , 2) +  math.pow((y2 - y1) , 2))

def pintar(im, coords, radius):
  umbral = 4
  global actual
  bordes = Image.open('bordes1.png')
  grad = bordes.load()
  w, h = im.size
  pixeles = im.load()
  draw = ImageDraw.Draw(im)
  D = distance((0, 0), (w, h))
  
  for x, y in coords:
    rg = 255
    v1, v2, v3, v4 = False, False, False, False
    for k in range(-umbral, umbral):
      curr_radius = radius + k
      if x + curr_radius < w and x + curr_radius > 0 and x - curr_radius < w and  x - curr_radius > 0:
        if grad[x + curr_radius, y] != (0, 0, 0):
          v1 = True
        if grad[x - curr_radius, y] != (0, 0, 0):
          v2 = True
      if y + curr_radius < h and y + curr_radius > 0 and y - curr_radius < h and  y - curr_radius > 0:
        if grad[x, y + curr_radius] != (0, 0, 0):
          v3 = True
        if grad[x, y - curr_radius] != (0, 0, 0):
          v4 = True

        if v1 and v2 and v3 and v4:
          pixeles[x, y] = (0, 255, 0)
          draw.text((x, y), '%s'%(actual+1), (0,0,0))
          d = 2.0 * radius
          print "Deteccion: (%s, %s)"%(x, y)
          print "ID: %s Radio: %s Diametro: %.01f %%"%(actual+1, radius, (d/D)*100.0)
          actual += 1
          draw.ellipse((x-radius, y-radius, x+radius, y+radius), outline = (rg, rg, 0))
          break
  im.save("deteccion1.png")

def zeros(n, m):
  matrix = []
  for i in range(n):
    tmp = []
    for j in range(m):
      tmp.append(0)
    matrix.append(tmp)
  return matrix

def group_votes(frec, (w, h)):
  dim = max(w, h)
  for padding in range (1, int(round(dim*0.1))):
    c = True
    while c:
      c = False
      for i in range(w):
        for j in range(h):
          v = frec[i][j]
          if v > 0:
            for n in range(-padding, padding):
              for m in range(-padding, padding):
                if not (n == 0 and m == 0):
                  if i + m >= 0 and i + m < w and j + n >= 0 and j + n < h:
                    v2 = frec[i + m][j + n]
                    if v2 > 0:
                      if v - padding >= v2:
                        frec[i][j] = v + v2 
                        frec[i + m][j + n] = 0
                        c = True
  return frec
  
def encontrar(im, radius, gradx, grady):
  w, h = im.size
  Gx = gradx.load()
  Gy = grady.load()
  frec = zeros(w, h)
  pixeles = im.load()
  
  for i in range(w):
    for j in range(h):
      if Gy[i, j] != (0, 0, 0) or Gx[i, j] != (0, 0, 0):
        r, g, b = Gx[i, j]
        gx = (r+g+b)/3
        r, g, b = Gy[i, j]
        gy = (r+g+b)/3
        g = math.sqrt(gx ** 2 + gy ** 2)
        if abs(g) > 0:
          theta = math.atan2(gy , gx)
          xc = int(round(i - radius * math.cos(theta+math.radians(90.0))))
          yc = int(round(j - radius * math.sin(theta+math.radians(90.0))))
          if xc >= 0 and xc < w and yc >= 0 and yc < h:
            frec[xc][yc] += 1
  		
  frec = group_votes(frec, (w, h))
  max_ = 0
  suma = 0.0
  
  for x in xrange(w):
    for y in xrange(h):
      v = frec[x][y]
      suma += v
      if v > max_:
        max_ = v
  promedio = suma / (w * h)
  umbral = (max_ + promedio) / 2.0
  coords = []
  for x in xrange(w):
    for y in xrange(h):
      v = frec[x][y]
      if v > umbral:
        coords.append((x, y))
  return coords

def deteccion(im, radius, gradx, grady):
  convolucion(im, ambos)
  coords = encontrar(im, radius, gradx, grady)
  pintar(im, coords, radius)

def main():
  function()
  
actual = 0
im = Image.open(sys.argv[1]).convert('RGB')
ambos = [[0, 2, 2], [-2, 0, 2], [-2, -2, 0]]
gradx = convolucion(im, maskx)
grady = convolucion(im, masky)
for i in [14, 20, 25]:
  deteccion(im, i, gradx, grady)	
