import PIL
import Tkinter
from Tkinter import *
import Image, ImageTk
from sys import argv

cargar = argv[1]

def function(imagen):
  imagen_carga = Image.open(imagen)
	root = Tkinter.Tk()
	root.title("Conversion")
	ima_res = greyscale(imagen_carga)
	tkimage=ImageTk.PhotoImage(imagen_carga)
	imagen_carga.save("iron_gris.png")
	Tkinter.Label(root, image=tkimage).pack()
	root.mainloop()
	
def greyscale(imagen = cargar):
	pixeles = imagen.load()
	x,y = imagen.size
	for i in range(x):
		for j in range(y):
			(r,g,b) = pixeles[i,j]
			gris = (r+g+b)/3
			pixeles[i,j]=(gris,gris,gris)
	return pixeles
	
def main():
	function(cargar)

main()
