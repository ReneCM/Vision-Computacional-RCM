import Tkinter
import random
import Image, ImageTk
from sys import argv
import time

cargar = argv[1]

#Ventana
def funcion(imagen):
  imagen_carga = Image.open(imagen)	
	root = Tkinter.Tk()
	root.title("Quitar Sal y pimienta")
	imagen_carga = sin_salpim(imagen_carga)
	tkimage = ImageTk.PhotoImage(imagen_carga)
	imagen_carga.save("sin_sp1.png")
	Tkinter.Label(root, image = tkimage).pack()
	root.mainloop()

#Quitamos sal y pimienta	
def sin_salpim(imagen):
	pixeles = imagen.load()
	x, y = imagen.size
	for i in range(x):
		for j in range(y):
			rgb = pixeles[i,j]
			#time.sleep(1)
			#print rgb
			if rgb == (255, 255, 255) or rgb == (0, 0, 0):
				suma1, suma2, suma3 = 0, 0, 0
				#print rgb
				for n in [-1, 0, 1]:
					for m in [-1, 0, 1]:
						if n+i > 0 and n+i < x and m+j > 0 and m+j < y:
							#print m+i, n+j	
							if n == 0 and m == 0:
								pass
							else:
								suma1 += pixeles[n+i, m+j][0]
								suma2 += pixeles[n+i, m+j][1]
								suma3 += pixeles[n+i, m+j][2]	
				promedio1, promedio2, promedio3 = suma1/8, suma2/8, suma3/8
				print suma1, suma2, suma3
				pixeles[i, j] = promedio1, promedio2, promedio3
	return imagen
	
def main():
	funcion(cargar)

main()
