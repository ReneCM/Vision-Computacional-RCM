import Tkinter
import Image, ImageTk
import time
import math
from sys import argv

cargar = argv[1]
matriz = argv[2:11]

escala = 'escala.jpg'
convo = 'convo.jpg'

def funcion(imagen):
  #imagen = raw_input("Extencion de imagen: ")
	im = Image.open(imagen).convert("RGB")
	ancho,altura = im.size
	pixel = im.load()
	root = Tkinter.Tk()
	root.title("Deteccion Lineas")
	tkimage = ImageTk.PhotoImage(im)
	#im.save("imagen)
	im = grayscale(im)
	convo,gx,gy,mxy = convolucion(im)
	lineas(convo,mxy,gx,gy)
	Tkinter.Label(root, image = tkimage).pack()
	root.mainloop()
	return
	#return ancho,altura,pixels,im
	
def grayscale(im):
	pixel = im.load()
	ancho,altura = im.size
	print im.mode
	for i in range(ancho):
		for j in range(altura):
			(r,g,b) = pixel[i,j]
			gris = (r+g+b)/3
			pixel[i,j] = (gris,gris,gris)
	im.save(escala)
	return im
 	
def convolucion(im):
	tiempoi = time.time()
	ancho,altura = im.size
	pixel = im.load() 
	matrix = [[-1,-1,-1],[2,2,2],[-1,-1,-1]]
	matriy = [[-1,2,-1],[-1,2,-1],[-1,2,-1]]
	nueva = Image.new("RGB", (ancho, altura))
	pixels = nueva.load()
	gx = []
	gy = []
	mxy = []
	for i in range(altura):
		gx.append([])
		gy.append([])
		mxy.append([])
		for j in range(ancho):
			sumax = 0
			sumay = 0
			cont = 0
			if j > 0 and i > 0 and  i < altura -1 and j <ancho -1:             
				for x in range(len(matrix[0])):
					for y in range(len(matrix[0])):
						try:
							sumax += matrix[x][y] * pixels[j+y-1,i+x-1][1]
							sumay += matriy[x][y] * pixels[j+y-1,i+x-1][1]		
						except:
							pass
			r = int(math.sqrt(sumax**2+sumay**2)) 
			gx[i].append(sumax)
			gy[i].append(sumay)
			mxy[i].append(r)
			if r <= 0:
				r = 0
			if r > 255:
				r = 255	
			pixels[j, i] = (r,r,r)	
	nueva.save(convo)
	tiempof = time.time()
        print "Tiempo: ",tiempof-tiempoi,"segundos"
	return convo,gx,gy,mxy
	
def lineas(convo,mxy,gx,gy):
	print "entrando"
	tiempoi = time.time()
	CERO = 0.0001 
	magnitud = []  
	angulos = [] 
	rhos = [] 
	ancho,altura = im.size
	pixel = im.load() 
	angulo = 0.0
	#greyscale()
	print "inicio de rho: "
	for x in range(altura):
		rhos.append([])
		angulos.append([])
		magnitud.append([])
		for y in range(ancho):
			if x > 0 and y > 0 and  x < altura -1 and y < ancho -1:
				hor = gx[x][y]
				ver = gy[x][y]
				mag = mxy[x][y]
				if fabs(hor) > 0.0:
					angulo = atan(ver/hor)
				else:
					if fabs(hor) + fabs(ver) <= 0.0:
						angulo = None
					elif fabs(ver - hor) < CERO: 
						angulo = atan(1.0)
					elif hor * ver > 0.0:
						angulo = pi 
					else:
						angulo = 0.0	
				if angulo is not None:
 					while angulo < CERO:
						angulo += pi
					while angulo > pi:
						angulo -= pi
					cosa = float('%0.2f'%angulo)
					rho = fabs( y * cos(angulo) + x * sin(angulo))
					magnitud[x].append(mag)                                    
					angulos[x].append(cosa)
					rhos[x].append(float('%0.2f'%rho)) 
				if angulo == None:
					magnitud[x].append(mag)
                                        angulos[x].append(angulo)
                                        rhos[x].append(None)		
	grupos = dict()
	cont = 0
	for x in range(altura):
		for y in range(ancho):
			if x > 0 and y > 0 and  x < altura -1 and y < ancho -1:
				try:
					if rhos[x][y] != None:
						dato = ((rhos[x][y]),(angulos[x][y]))
					if dato in grupos:
						grupos[dato] += 1 
					else:
						grupos[dato] = 1
				except:
					pass
	print "frecuencias"			
	frec = frecuentes(grupos, int(ceil(len(grupos) * 50))) 
	for x in range(altura):
		for y in range(ancho):
			if x > 0 and x< altura-1 and y > 0 and y < ancho-1:
				try:
					if pixels2[y,x][1] == 255:
						rho, ang = rhos[x][y],angulos[x][y]
						if (rho, ang) in frec:
							if ang == 0.79:
								pixel[y,x] = (255,0,0)
							if ang == 3.14 or ang == 0:
								pixel[y,x] = (0,0,255)
							if 1.50 < ang and ang < 1.60 :
								pixel[y,x] = (0,255,0)
				except:
					pass
	im.save("ba.png")						 
	tiempof = time.time()
	print "Tiempo: ",tiempof-tiempoi
	return 
	
def main():
	imagen = raw_input("Dame la imagen: ")
	funcion(imagen)
	#lineas(convo,mxy,gx,gy):
	
im = Image.open(cargar)
matriz = [int(i) for i in matriz]

main()
