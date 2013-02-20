import Tkinter
import random
import Image, ImageTk
from sys import argv

cargar = argv[1]

def funcion(imagen):
  imagen_carga = Image.open(imagen)
	root = Tkinter.Tk()
	root.title("Deteccion de Formas")
	#imagen_carga = bfs(imagen_carga, posi, color)
	tkimage = ImageTk.PhotoImage(imagen_carga)
	imagen_carga.save("detectado2.png")
	Tkinter.Label(root, image = tkimage).pack()
	root.mainloop()
	
def bfs(imagen):
	pixeles = imagen.load()
	x, y = imagen.size
	cola = []
	cola.append(posi)
	pos = pixeles[posi]
	while len(cola) > 0:
		(i,j) = cola.pop(0)
		posicion = pixeles[i,j]
		if posicion == pos or posicion == color:
			for rangox in [-1, 0, 1]:
				for rangoy in [-1, 0, 1]:
					a,b = (i + rangox, j + rangoy)
					if a >= 0 and a < x and b >= 0 and b < y:
						total = pixeles[a,b]
						if total == pos:
							pixeles[a,b] = color
							cola.append((a,b))

def main():
	funcion(cargar)

main()
