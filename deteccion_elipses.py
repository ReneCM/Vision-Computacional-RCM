#!/usr/bin/python

import sys
import Image
import ImageDraw
import math
import random
import Image, ImageTk
import Tkinter
from collections import defaultdict

def function():
  root = Tkinter.Tk()
	root.title("Elipses")
	tkimage = ImageTk.PhotoImage(imagen)
	Tkinter.Label(root, image = tkimage).pack()
	root.mainloop() 
 
def convolucion(imagen, g):
	w, h = imagen.size
	pix = imagen.load()
	salida_im = Image.new("RGB", (w, h))
	out = salida_im.load()
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
	salida_im.save("sal1.png")
	return salida_im
 
def bfs(imagen, origen, color):
	pix = imagen.load()
	w, h = imagen.size
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
	imagen.save("sal2.png")
	return n, coords
 
def distancia((x1, y1), (x2, y2)):
	return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
 
def encontrar(imagen, elipse, Gx, Gy):
	list = {}
	pix = imagen.load()
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
	return frec[0][0], list
 
def puntos(p, line):
	for coords in line:
		if p == coords:
			return True
	return False
 
def fijar_ejes(center, (p1, p2)):
	xc, yc = center
	if distancia((p1[0], 0), (p2[0], 0)) > distancia((0, p1[1]), (0, p2[1])):
		out1 = (p1[0], yc)
		out2 = (p2[0], yc)
		axis = "x"
	else:
		out1 = (xc, p1[1])
		out2 = (xc, p2[1])
		axis = "y"
	return (out1, out2), axis
  
def cuadrado(x, y):
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
 
def ejes(imagen, list, center):
	w, h = imagen.size
	diagonal = distancia((0, 0), (w-1, h-1))
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
	coords, axis = fijar_ejes(center, frec[0][0])
	if axis == "x":
		x = coords
		y, _ = fijar_ejes(center, frec[len(frec) - 1][0])
	else:
		y = coords
		x, _ = fijar_ejes(center, frec[len(frec) - 1][0])
	dist1 = distancia(x[0], x[1])
	dist2 = distancia(y[0], y[1])
	bou = cuadrado(x, y)
	return x, y, bou
		
def deteccion(imagen, bordes, (gradx, grady)):
	w, h = imagen.size
	elipses = []
	tmp = bordes.copy()
	out = tmp.load()
	salida_im = imagen.copy()
	for i in range(w):
		for j in range(h):
			if out[i, j] == (255, 255, 255):
				_, coords = bfs(tmp, (i, j), (255, 0, 0))
				elipses.append(coords)
	Gx = gradx.load()
	Gy = grady.load()
	draw = ImageDraw.Draw(salida_im)
	pix = salida_im.load()
	i = 1
	total = w*h
	for elipse in elipses:
		M, list = encontrar(bordes, elipse, Gx, Gy)
		x, y, b = ejes(imagen, list, M)
		area, coords = bfs(salida_im, M, (255, 0, 0))
		print "Figura encontrada: %s"%i
		print "Total de Area: %0.2f%%"%((area/float(total))*100.0)
		draw.text(M, "%s"%i, fill = (0, 0, 0))
		pix[M] = (0, 0, 255)
		i += 1
	salida_im.save("sal3.png")

sobelx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
sobely = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
	
ambas = [[1, 3, 3,], [-3, -2, 3], [-3, -3, 1]]
	
	
def main():
	function()
	
	imagen = Image.open(sys.argv[1]).convert("RGB")
	
	gradx = convolucion(imagen, sobelx)
	grady = convolucion(imagen, sobely)
	
	bordes = convolucion(imagen, ambas)
	deteccion(imagen, bordes, (gradx, grady))
	
main()
