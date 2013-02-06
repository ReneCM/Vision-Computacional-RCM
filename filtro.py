import PIL 
import Tkinter
from Tkinter import * 
import Image, ImageTk
from sys import argv
import numpy

cargar = argv[1]

def function(imagen):
  imagen_carga = Image.open(imagen)
	root = Tkinter.Tk()
	root.title("Conversion")
	ima_res = filtro(imagen_carga)
	tkimage=ImageTk.PhotoImage(imagen_carga)
	imagen_carga.save("iron_filtro.png")
	Tkinter.Label(root, image=tkimage).pack()
	root.mainloop()

def filtro(imagen = cargar):
	pixeles = imagen.load()
	list = [-1,0,1]
	x,y = imagen.size
	matriz = numpy.empty((x,y))
	for i in range(x):
		for j in range(y):
			prom = vecinos(i,j,list,matriz)
			pixeles[i,j] = (prom,prom,prom)
	return pixeles

def vecinos(i,j,list,matriz):
	prom = 0 
	ind = 0
	for x in list:
		for y in list:
			a = i+x
			b = j+y
			try:
				if matriz[a,b]:
					prom += matriz[a,b]
					ind += 1
			except IndexError:
				pass
	try:
		prom = int(prom/ind)
		return prom
	except ZeroDivisionError:
		return 0
		
def greyscale(imagen = cargar):
	pixeles = imagen.load()
	x,y = imagen.size
	for i in range(x):
		for j in range(y):
			(r,g,b) = pixeles[i,j]
			escale = (r+g+b)/3
			pixeles[i,j] = (escale,escale,escale)
			matriz[i,j] = int(escala)
	return pixeles, matriz
	
def main():
	function(cargar)

main()
