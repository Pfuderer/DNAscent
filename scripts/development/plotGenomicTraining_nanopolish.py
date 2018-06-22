import sys
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from scipy import stats

totalReads = 10000

#--------------------------------------------------------------------------------------------------------------------------------------
def displayProgress(current, total):

	barWidth = 70
	progress = float(current)/float(total)

	if progress <= 1.0:
		sys.stdout.write('[')
		pos = int(barWidth*progress)
		for i in range(barWidth):
			if i < pos:
				sys.stdout.write('=')
			elif i == pos:
				sys.stdout.write('>')
			else:
				sys.stdout.write(' ')
		sys.stdout.write('] '+str(int(progress*100))+' %\r')
		sys.stdout.flush()
#--------------------------------------------------------------------------------------------------------------------------------------


#eventalign output
sixmer2eventsBrdU = {}
f = open(sys.argv[1],'r')
currentRead = ''
readCounter = 0
for line in f:

	splitLine = line.rstrip().split('\t')

	#ignore the header line
	if splitLine[0] == 'contig':
		continue

	readIndex = splitLine[3]
	if readIndex != currentRead:
		currentRead = readIndex
		readCounter += 1
		displayProgress(readCounter, totalReads)

	if readCounter == totalReads:
		break

	eventTime = float(splitLine[8])
	if eventTime < 0.002:
		continue

	sixmer = splitLine[9]
	if sixmer not in sixmer2eventsBrdU:
		sixmer2eventsBrdU[sixmer] = []
	else:
		sixmer2eventsBrdU[sixmer].append( float(splitLine[6]) )
f.close()

#pore model
model = {}
f = open(sys.argv[2],'r')
for line in f:

	if line[0] == '#' or line[0] == 'k':
		continue
	
	splitLine = line.rstrip().split('\t')
	model[splitLine[0]] = [	float(splitLine[1]), float(splitLine[2]) ]
f.close()

#mixture model
mixture = {}
f = open(sys.argv[3],'r')
for line in f:

	if line[0] == '6':
		continue
	
	splitLine = line.rstrip().split('\t')
	mixture[splitLine[0]] = [ float(splitLine[4]), float(splitLine[5]), float(splitLine[7]), float(splitLine[8]), float(splitLine[10]), float(splitLine[11]) ]
f.close()

for i, key in enumerate(sixmer2eventsBrdU):

	if key == 'NNNNNN':
		continue
	
	#if key in mixture:
	if len( sixmer2eventsBrdU[key] ) > 100:
		x = np.linspace( np.mean(sixmer2eventsBrdU[key])-15, np.mean(sixmer2eventsBrdU[key])+15, 1000 )
		plt.figure(i)

		#density
		densityBrdU = stats.kde.gaussian_kde( sixmer2eventsBrdU[key] )
		plt.plot(x, densityBrdU(x), label='BrdU Density')
		
		#pore model
		yModel = mlab.normpdf( x, model[key][0], model[key][1] )
		plt.plot(x, yModel, label='6mer Pore Model')

		#trimodal
		if key in mixture:
			yMix = mlab.normpdf( x, mixture[key][0], mixture[key][1] )
			plt.plot( x, yMix, label='Fit Distribution (1)')
			yMix = mlab.normpdf( x, mixture[key][2], mixture[key][3] )
			plt.plot( x, yMix, label='Fit Distribution (2)')
			yMix = mlab.normpdf( x, mixture[key][4], mixture[key][5] )
			plt.plot( x, yMix, label='Fit Distribution (3)')

		#plotting stuff
		plt.xlabel('pA')
		plt.ylabel('Count')
		plt.title( key + '  N=' + str(len(sixmer2eventsBrdU[key])) )
		plt.legend(loc='upper right')
		plt.savefig( key + '.png' )
		plt.close()
