import PIL
import Tkinter
import random
import Image, ImageTk
from Tkinter import * 
from sys import argv

cargar = argv[1] #argumento para cargar imagen 
int = 1 #intencidad
pol = 1 #polarizacion 

def function(imagen): #creamos ventana 
  imagen_carga = Image.open(imagen)
	root = Tkinter.Tk()
	root.title("Sal y Pimienta")
	ima_res = sal_pim(imagen_carga)
	tkimage=ImageTk.PhotoImage(imagen_carga)
	imagen_carga.save("sal_pim.png")
	Tkinter.Label(root, image=tkimage).pack()
	root.mainloop()

def sal_pim(imagen = cargar): #sal y pimienta 
	pixeles = imagen.load()
	x,y = imagen.size
	n = x * y
	n = int*(n/100)
	i = 0
	if imagen.mode == "RGB":
		while i != n:
			a,b = random.randint(0, x-1), random.randint(0, y-1)
			det = random.randint(0,1)
			if det == 1:
				s = random.randint(255-pol, 255) 
				pixeles[a,b] = (s, s, s)
			else:
				p = random.randint(0, pol)
				pixeles[a,b] = (p, p, p)
			i += 1
	
	if imagen.mode == "L":
		while i!= n:
			a,b = random.randint(0, x - 1), random.randint(0, y - 1)
			det = random.randint(0, 1)
			if det == 1:
				s = random.randint(255-pol, 255)
				pixeles[a,b] = s
			else: 
				p = random.randint(0, pol)
				pixeles[a,b] = p
			i += 1
	return pixeles
	
def main():
	function(cargar)
	
main()
