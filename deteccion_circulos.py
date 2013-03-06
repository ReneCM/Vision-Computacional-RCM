import Tkinter
import sys
import time
import random
import math
from PIL import Image, ImageTk, ImageDraw
 
def function():
  deteccion(sys.argv[1])
  root = Tkinter.Tk()
	root.title("Circulos")
	tkimage = ImageTk.PhotoImage(salida)
	Tkinter.Label(root, image = tkimage).pack()
	root.mainloop()
 
def convolucion(image, mascara):
	im = Image.open(escala)
	ancho,altura = im.size
	pic = image.load()
	mask = mascara
	nuevai = Image.new("RGB", (ancho, altura))
	npixels = nuevai.load()
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
			npixels[j, i] = (r,r,r)
	return gx,gy,mxy
 
def circulos(picx, picy, image,bias = 10):
    frequency = dict()
    matriz = dict()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            (Rx, Gx, Bx) = picx[i,j]
            (Ry, Gy, By) = picy[i,j]
            gx = float(Rx+Gx+Bx)/3
            gy = float(Ry+Gy+By)/3
            gradiente = math.sqrt(math.pow(gx, 2) + math.pow(gy, 2))
            if gradiente < -1*bias or gradiente > bias:
                cos_theta = (gx/gradiente)
                sin_theta = (gy/gradiente)
                theta = math.atan2(gy, gx)
                r = 60
                centro = (int( i - r * math.cos(theta+math.radians(90.0))), int( j - r * math.sin(theta+math.radians(90.0))))
                centro = ((centro[0]/salto)*salto, (centro[1]/salto)*salto)
                matriz[i,j] = centro
                if not centro in frequency:
                    frequency[centro] = 1
                else:
                    frequency[centro] += 1
            else:
                matriz[i, j] = None
    return matriz, frequency
 
def lineas(image, frequency, matriz):
    pic = image.load()
    draw = ImageDraw.Draw(image)
    counter = 1
    colors = dict()
    for i in frequency.keys():
        colors[i] = (0,255,0)
        r = 2
        draw.ellipse((i[0]-r, i[1]-r, i[0]+r, i[1]+r), fill=(0, 0, 255))
        print 'C'+str(counter)
        counter += 1
 
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if matriz[i, j] in frequency:
                try:
                    pic[i,j] = colors[matriz[i, j]]
                except:
                    pass
    return image
 
sobelx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
sobely = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
 
def deteccion(image_name, salida="deteccion_circulos2.png"):
    imagex = convolucion(image_name, sobelx)
    imagey = convolucion(image_name, sobely)
    image = Image.open(image_name)
    salto = 30
    matriz, frequency = circulos(imagex, imagey, image, salto = salto)
    for i in frequency.keys():
        if frequency[i] < salto*8:
            frequency.pop(i)
        else:
            print frequency[i], i
    lineas(image, frequency, matriz)
    image.save(salida)
 
def main():
    function()
 
main(
