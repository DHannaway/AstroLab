import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from tkinter import *
from cdict import *
from astropy.io import fits
import shutil

#Delete the old 'images' folder, and create a new one
if os.path.exists('images'):
	shutil.rmtree('images')
if not os.path.exists('images'):
	os.makedirs('images')

#Path to the executable file:
codepath='C:\\Users\\Dan\\Documents\\GitHub\\Python\\'
filename='CMacIonize.exe --params test_dustsimulation.param --dusty-radiative-transfer --threads 8'

cdict1=[]
for i in range(0,len(cmap1)):
	arr=[]
	for j in range(0,len(cmap1[i])):
		arr.append(cmap1[i][j]/255.)
	cdict1.append(arr)
cm = mpl.colors.ListedColormap(cdict1)

fitsfile = fits.open('NGC891_V_data.fits')
fitsdata = fitsfile[0].data
nfactor=np.nansum(fitsdata)

datalist=[]
for i in range(355,555):
	arr=[]
	for j in range(250,650):
		arr.append(fitsdata[i][j])
	datalist.append(arr)
dataplot=np.array(datalist)
tdata=np.transpose(dataplot)
nloop=1

def simulation():
	global nloop

	B_T=w1.get()
	h_stars=w2.get()
	r_stars=w3.get()
	h_ISM=w4.get()
	r_ISM=w5.get()
	n_0=w6.get()

	nphotons=600000

	#Replace the old .param file with a new one with the entered values
	with open('test_dustsimulation_original.param') as g:
		lines=list(g)

	h=open('test_dustsimulation.param','w')
	for i in range(0,len(lines)):
		if i==12:
			h.write('  B_over_T: '+str(B_T)+'\n')
		elif i==13:
			h.write( '  h_stars: '+str(h_stars)+' kpc\n' )
		elif i==14:
			h.write('  r_stars: '+str(r_stars)+' kpc\n'  )
		elif i==16:
			h.write('  h_ISM: '+str(h_ISM)+' kpc\n'  )
		elif i==18:
			h.write('  r_ISM: '+str(r_ISM)+' kpc\n'  )
		elif i==17:
			h.write('  n_0: '+str(n_0)+' cm^-3\n' )
		elif i==28:
			h.write('number of photons: '+str(nphotons)+'\n'  )
		else:
			h.write(lines[i])
	h.close()

	#Input this new file into the testDustSimulation program and compile
	os.system(codepath+filename)  

	#Input the created binary file, and plot as an image 
	# Compare this image with the FITS data
	image = np.fromfile("test_dustsimulation_output.dat", dtype = np.float64)
	image = image.reshape((200, 200))

	image2=[]
	for i in range(0,len(image)):
		arr=[]
		for j in range(50,150):
			arr.append(image[i][j]*0.75*sum(sum(tdata)))
		image2.append(arr)
	image2 = np.kron(image2,np.ones((2,2)))


	fig, ax = plt.subplots(2) 
	ax[0].matshow(dataplot, cmap=cm)
	ax[1].matshow(np.transpose(image2), cmap=cm)

	plt.text(420,50,"B_T ="+str(B_T)+'\n'+"h_stars ="+str(h_stars)+" kpc"+'\n'+"r_stars ="+str(r_stars)+" kpc"+'\n'+"h_ISM ="+str(h_ISM)+" kpc"+'\n'+"r_ISM ="+str(r_ISM)+" kpc"+'\n'+"n0 ="+str(n_0)+" cm^-3",color='k')
#	tick_locs_x = [0,200,400]
#	tick_locs_y = [0,200,400]

#	xtick_lbls = ['-12.1kpc','0','12.1kpc']
#	ytick_lbls = ['-6kpc','0','6kpc']

#	plt.xticks(tick_locs_x, xtick_lbls,rotation=0,fontsize=10)
#	plt.yticks(tick_locs_y, ytick_lbls,rotation=0,fontsize=10)

	linearray=[152,200,248]
	N=len(linearray)
	color=iter(plt.cm.rainbow(np.linspace(0,1,N)))
	for i in range(0,len(linearray)):
		c=next(color)
		ax[0].axvline(linearray[i],c=c)
		ax[1].axvline(linearray[i],c=c)

	plt.savefig('images/image'+str(nloop))
	plt.show()
	plt.close()

	def normplot(func,n):
	#	return (func[n]/max(func[n]))-(min(func[n])/max(func[n]))
	#	return (func[n]/(func[n][100]))-(min(func[n])/(func[n][100]))
		return func[n]-min(func[n])
	def difplot(func1,func2,n):
		return (func1[n]-min(func1[n]))-(func2[n]-min(func2[n]))
	color=iter(plt.cm.rainbow(np.linspace(0,1,N)))

	fig,ax=plt.subplots(len(linearray),sharey=False)
	for i in range (0,len(linearray)):
		ax[i].plot(normplot(image2,linearray[i]),linestyle='--',label='model',c='k')
		ax[i].plot(normplot(tdata,linearray[i]),label='data',c=next(color))
		ax[i].set_title("Intensity offset plot for x = "+str(linearray[i]))
		ax[i].legend(loc='upper left')
	plt.tight_layout()
	plt.savefig('images/offset'+str(nloop))
	plt.show()
	plt.close()
	color=iter(plt.cm.rainbow(np.linspace(0,1,N)))

	fig,ax=plt.subplots(len(linearray),sharey=True)
	for i in range (0,len(linearray)):
		ax[i].plot(difplot(tdata,image2,linearray[i]),linestyle='--',label='residual',c=next(color))
		ax[i].set_title("Intensity offset plot for x = "+str(linearray[i]))
		ax[i].legend(loc='upper left')
	plt.tight_layout()
	plt.savefig('images/difference'+str(nloop))
	plt.show()
	plt.close()
	nloop=nloop+1
master = Tk()
w1 = Scale(master, from_=0.0, to=0.99,resolution=0.01, orient=HORIZONTAL,length=500,label="B/T")
w1.pack()
w2 = Scale(master, from_=0.0, to=2.0,resolution=0.01, orient=HORIZONTAL,length=500,label="h_stars [kpc]")
w2.pack()
w3 = Scale(master, from_=0.0, to=7.0,resolution=0.01, orient=HORIZONTAL,length=500,label="r_stars [kpc]")
w3.pack()
w4 = Scale(master, from_=0.0, to=2.0,resolution=0.01, orient=HORIZONTAL,length=500,label="h_ISM [kpc]")
w4.pack()
w5 = Scale(master, from_=0.0, to=7.0,resolution=0.01, orient=HORIZONTAL,length=500,label="r_ISM [kpc]")
w5.pack()
w6 = Scale(master, from_=0.0, to=3.0,resolution=0.01, orient=HORIZONTAL,length=500,label="n_0 [cm^-3]")
w6.pack()
Button(master, text='Simulate', command=simulation
).pack()

mainloop()

