import PIL 
import Tkinter
from Tkinter import *
import Image, ImageTk
from sys import argv

image = sys.argv[1]
matriz = sys.argv[2:11]

def function():
  convolusion()
	root = Tkinter.Tk()
	root.title("Convolusion")
	tkimage = ImageTk.PhotoImage(ima_res)
	ima_res.save("det_bord.png")
	Tkinter.Label(root, image = tkimage).pack()
	root.mainloop()

def grayscale():
	pixel = imagen.load()
	x,y = imagen.size
	for i in range(x):
		for j in range(y):
			(r,g,b) = pixel[i,j]
			gris =(r+g+b)/3
			pixel[i,j] = (gris, gris, gris)

def convolusion(): # Vecinos
	grayscale()
	pixeles = ima_res.load()
	pixel = imagen.load()
	x,y = imagen.size
	for i in range(x):
		for j in range(y):
			color = 0
			(r,g,b) = pixel[i,j]
			color += int(r * matriz[4])
			#Norte
			if i - 1 <= 0:
				None
			else: 
				r_norte, g_norte, b_norte = pixel[(i-1),j]
				color += (r_norte * matriz[1])
				#Noroeste
				if i - 1 <= 0 or j - 1 <=0:
					None
				else:
					r_noroeste, g_noroeste, b_noroeste = pixel[(i-1),(j-1)]
					color += (r_noroeste * matriz[0])
				#Noreste
				if i - 1 <= x or j + 1 <= y:
					None
				else:
					r_noreste, g_noreste, b_noreste = pixel[(i-1), (j+1)]
					color += (r_noreste * matriz[2])
			#Sur
			if i + 1 >= x:
				None 
			else: 
				r_sur, g_sur, b_sur = pixel[(i + 1), j]
				color += (r_sur * matriz[7])
				#Suroeste
				if i + 1 < x or j - 1 < y:
					None
				else: 
					r_suroeste, g_suroeste, b_suroeste = pixel[(i+1),(j-1)]
					color += (r_suroeste * matriz[6])
				#Sureste
				if i + 1 <= x or j + 1 <= y:
					None
				else: 
					r_sureste, g_sureste, b_sureste = pixel[(i+1),(j+1)]
					color += (r_sureste * matriz[8])
			#Oeste
			if j - 1 <= 0:
					None
			else:
				r_oeste, g_oeste, b_oeste = pixel[i,(j-1)]
				color += (r_oeste * matriz[3])
			#Este
			if j + 1 >= y:
				None
			else: 
				r_este, g_este, b_este = pixel[i,(j+1)]
				color += (r_este * matriz[5])
			pixeles[i, j] = (color, color, color)
				
def main():
	function()

imagen = Image.open(image)
ima_res = Image.open(image)
matriz = [int(i) for i in matriz]

main()	
