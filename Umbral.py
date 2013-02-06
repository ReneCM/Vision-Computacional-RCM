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
	ima_res = umbral(imagen_carga)
	tkimage=ImageTk.PhotoImage(imagen_carga)
	imagen_carga.save("iron_umbral.png")
	Tkinter.Label(root, image=tkimage).pack()
	root.mainloop()
	
def umbral(imagen = cargar):
	pixeles = imagen.load()
	x,y = imagen.size
	for i in range(x):
		for j in range(y):
			(r,g,b) = pixeles[i,j]
			gris = (r+g+b)/3
			if gris < 127 : 
				pixeles[i,j]=(0,0,0)
			else:
				pixeles[i,j]=(255,255,255)
	return pixeles
	
def main():
	function(cargar)

main()
