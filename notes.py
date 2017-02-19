
noteDict = dict()
octave = 0
for i in range(128):
	octave = i / 12
	num = i % 12
	if num == 0:
		noteDict['c' + str(octave)] = i
		noteDict[i] = 'c' + str(octave)
	elif num == 1:
		noteDict['c#' + str(octave)] = i
		noteDict['db' + str(octave)] = i
		noteDict[i] = 'c#' + str(octave)
	elif num == 2:
		noteDict['d' + str(octave)] = i
		noteDict[i] = 'd' + str(octave)
	elif num == 3:
		noteDict['d#' + str(octave)] = i
		noteDict['eb' + str(octave)] = i
		noteDict[i] = 'd#' + str(octave)
	elif num == 4:
		noteDict['e' + str(octave)] = i
		noteDict[i] = 'e' + str(octave)
	elif num == 5:
		noteDict['f' + str(octave)] = i
		noteDict[i] = 'f' + str(octave)
	elif num == 6:
		noteDict['f#' + str(octave)] = i
		noteDict['gb' + str(octave)] = i
		noteDict[i] = 'f#' + str(octave)
	elif num == 7:
		noteDict['g' + str(octave)] = i
		noteDict[i] = 'g' + str(octave)
	elif num == 8:
		noteDict['g#' + str(octave)] = i
		noteDict['ab' + str(octave)] = i
		noteDict[i] = 'g#' + str(octave)
	elif num == 9:
		noteDict['a' + str(octave)] = i
		noteDict[i] = 'a' + str(octave)
	elif num == 10:
		noteDict['a#' + str(octave)] = i
		noteDict['bb' + str(octave)] = i
		noteDict[i] = 'a#' + str(octave)
	elif num == 11:
		noteDict['b' + str(octave)] = i
		noteDict[i] = 'b' + str(octave)