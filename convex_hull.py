import Tkinter
import random
import Image, ImageTk, ImageDraw
from sys import argv

cargar = argv[1]

def funcion(imagen):
  imagen_carga = Image.open(imagen)
	imagen, hulls = convex_hull(imagen_carga)
	draw = ImageDraw.Draw(imagen_carga)
	for i in hulls: 
		for j in i:
			draw.line(j, fill=255)
	print hulls
	root = Tkinter.Tk()
	root.title("Convex Hull")
	tkimage = ImageTk.PhotoImage(imagen_carga)
	w, h = imagen_carga.size
	canvas = Tkinter.Canvas(root, width = w, height = h)
	imagen_carga.save("conv2.png")
	Tkinter.Label(canvas, image = tkimage).pack()
	canvas.pack()
	root.mainloop()
	
def bfs(imagen, origen, color):
	pixeles = imagen.load()
	x, y = imagen.size
	cola = []
	coordenadas  = []
	cola.append(origen)
	original = pixeles[origen]
	n = 0
	while len(cola) > 0:
		(a, b) = cola.pop(0)
		actual = pixeles[a, b]
		if actual == original or actual == color:
			for dx in [-1, 0, 1]:
				for dy in [-1, 0, 1]:
					i, j = (a + dx, b + dy)
					if i >= 0 and i < x and j >= 0 and j < y:
						contenido = pixeles[i, j]
						if contenido == original:
							pixeles[i, j] = color
							coordenadas.append((i, j))
							n += 1
							cola.append((i, j))
	return n, coordenadas

#def turn(p1, p2, p3):
#	t = cmp(0, (p2[0] - p1[0])*(p3[1] - p1[1]) - (p3[0] - p1[0])*(p2[1] - p1[1]))
#	if t == -1: 
#		return 'LEFT'	
 
def jarvis(S):
	punto_hull = [min(S)]
	i = 0
	while True:
		fin_punto = S[0]
		for j in range(len(S) - 1):
			if fin_punto == punto_hull[i] or turn(S[j], punto_hull[i], fin_punto) == 'LEFT':
				fin_punto = S[j]
		i += 1
		punto_hull.append(fin_punto)
		if fin_punto == punto_hull[0]:
			break
	return punto_hull
        
def convex_hull(imagen):
	x, y = imagen.size
	pixeles = imagen.load()
	hulls = []
	for i in range(x):
		for j in range(y):
			if pixeles[i, j] == (255, 255, 255):
				n, coordenadas = bfs(imagen, (i, j), (255, 0, 0))
				hulls.append(jarvis(coordenadas))
#	for punto_hull in hulls:
#		for points in punto_hull:
#			pixeles[points] = (0, 255, 0)
#	return pixeles, hulls
	
def main():
	funcion(cargar)
	
main()
