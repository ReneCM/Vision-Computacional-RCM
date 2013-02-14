import Tkinter
import random
import Image, ImageTk
from sys import argv

cargar = argv[1]

polaridad = 1
intensidad = 1

#Ventana
def funcion(imagen):
	imagen_carga = Image.open(imagen)
	root = Tkinter.Tk()
	root.title("Sal y pimienta")
	imagen_carga = salpim(imagen_carga, 0.5, 0)
	tkimage = ImageTk.PhotoImage(imagen_carga)
	imagen_carga.save("sp1.png")
	Tkinter.Label(root, image = tkimage).pack()
	root.mainloop()
	
#Aplicamos sal y pimienta
def salpim(imagen, intensidad, polaridad):
	pixeles = imagen.load()
	x,y = imagen.size
	total = x * y
	total = int(intensidad*(total/100))
	i = 0
	print total
	while i!= total:
		a, b = random.randint(0, x - 1), random.randint(0, y - 1)
		vec = random.randint(0,1)
		if vec == 1:
			s = random.randint(255 - polaridad, 255)
			pixeles[a,b] = (s,s,s)
		else:
			p = random.randint(0, polaridad)
			pixeles[a,b] = (p,p,p)
		i += 1
	return imagen

def main():
	funcion(cargar)

main()
