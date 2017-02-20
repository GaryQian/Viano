from mido import Message, MidiFile, MidiTrack, MetaMessage
import mido as mido
import random as randomClass
from random import randint, uniform as random
import sys
from collections import deque
import heapq
import numpy as np
import time as timeClass
import copy

import cPickle
from os import path
from os import listdir
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.models import load_model
from keras.utils import np_utils
from keras import backend as K


from notes import noteDict
from structure import util, Seg, Song, Note, formImg
from read import read
from write import writeSong




keys = dict()
#MAJOR
keys[0] = [0, 2, 4, 5, 7, 9, 11] #C
keys[1] = [7, 9, 11, 0, 2, 4, 6] #G
keys[2] = [2, 4, 6, 7, 9, 11, 1] #D
keys[3] = [9, 11, 1, 2 ,4, 6, 8] #A
keys[4] = [4, 6 ,8, 9, 11, 1, 3] #E
keys[5] = [11, 1, 3, 4, 6, 8, 10] #B
keys[6] = [6, 8, 10, 11, 1, 3, 5] #F#

keys[7] = [5, 7, 9, 10, 0, 2, 4] #F
keys[8] = [10, 0, 2, 3, 5, 7, 9] #Bb
keys[9] = [3, 5, 7, 8, 10, 0, 2] #Eb
keys[10] = [8, 10, 0, 1, 3, 5, 7] #Ab
keys[11] = [1, 3, 5, 6, 8, 10, 0] #Db
keys[12] = [6, 8, 10, 11, 1, 3, 5] #Gb

#MINOR
keys[13] = [9, 11, 0, 2, 4, 5, 7] #A
keys[14] = [4, 6, 7, 9, 11, 0, 2] #E
keys[15] = [11, 1, 2, 4, 6, 7, 9] #B
keys[16] = [6, 8, 9, 11, 1, 2, 4] #F#
keys[17] = [1, 3, 4, 6, 8, 9, 11] #C#
keys[18] = [8, 10, 11, 1, 3, 4, 6] #G#
keys[19] = [3, 5, 6, 8, 10, 11, 1] #D#

keys[20] = [2, 4, 5, 7, 9, 10, 0] #D
keys[21] = [7, 9, 10, 0, 2, 3, 5] #G
keys[22] = [0, 2, 3, 5, 7, 8, 10] #C

keyCount = 22

features = dict()
features[-5] = [2, 1, 2, 1]
features[-4] = [1, 2, 1, 2]
features[-3] = [1, 1]
features[-2] = [2, 2, 2, 2]
features[-1] = [2, 2]
features[0] = [4, 4]
features[1] = [4, 4, 4, 4]
features[2] = [4]
features[3] = [8]
features[4] = [2, 2, 2, 2]
features[5] = [4, 2, 2]
features[6] = [4, 4, 2, 2]
features[7] = [2, 2, 4]
features[8] = [3, 1]
features[9] = [3, 1, 3, 1]
features[10] = [6, 2]
features[11] = [1.33333, 1.33333, 1.33333]
features[12] = [2.666666, 2.666666, 2.666666]
features[13] = [1, 1, 2]
features[14] = [2, 1, 1]
features[15] = [1, 3, 1]
features[16] = [.5, .5, 3]
featuresMax = 16
featuresMin = -5

def btt(song, n): #"Beats to time"
	return n / song.baseunit * mido.tempo2bpm(song.tempo) / 60 * song.tpb
	
def choice(seq):
    total_prob = sum(item[1] for item in seq)
    chosen = random(0, total_prob)
    cumulative = 0
    for item, probality in seq:
        cumulative += probality
        if cumulative > chosen:
            return item
			
def nextInKey(key, i, dir, mod=4, counter=0):
	k = keys[key]
	oc = i / 12
	i = i % 12
	if i in k:
		index = k.index(i)
		val = 30
		if counter % mod == 0:
			dir = -dir
		if dir > 0:
			if index == 6:
				val = k[0] + oc * 12 + 12
			else:
				val = k[index+1] + oc * 12
		else:
			if index == 0:
				val = k[6] + oc * 12 - 12
			else:
				val = k[index-1] + oc * 12
		while val < 20:
			val = val + 12
		return val
	else:
		closest = k[0]
		for j in range(len(k)):
			if abs(i - k[j]) < abs(i - closest):
				closest = k[j]
		return nextInKey(key, closest + oc * 12, dir)
			
			
def pickNote(dissonance, complexity, scaliness, key, result, prevNote, prevPrevNote, isBass):
	l = []
	
	if isBass:
		scaliness = scaliness * 1.5
		if scaliness > 100:
			scaliness = 100
		dissonance = dissonance * .5
		complexity = complexity * .5
		
	
	for i,p in enumerate(result):
		heapq.heappush(l, (1.0-p, i))
	pool = dict()
	for i in range(4):
		val = heapq.heappop(l)
		#print val
		if val[1] > 10 and val[1] > 0.4:
			pool[val[1]] = 1 + 1.5 * dissonance / 100
	prevOctave = prevNote / 12
	#prevent overly high playing
	if prevOctave > 7 and randint(0,100) < 20:
		prevOctave = prevOctave - 1
	if isBass and prevOctave > 5 and randint(0,100) < 50:
		prevOctave = prevOctave - 1
	#prevent overly low playing
	if (prevOctave <= 3 or (isBass and prevOctave <= 3))and randint(0,100) < 40:
		prevOctave = prevOctave + 1
	onKey = prevNote % 12 in keys[key]
	if (onKey):
		arpeggioEven = (keys[key].index(prevNote % 12) % 2 == 0)
	for i,k in enumerate(keys[key]):
		n = k + prevOctave * 12 
		pool[n] = 1 + (scaliness / 100 * (.10 * (24 - abs(prevNote - n))) ** 2)#Descending!
		if scaliness > 30 and prevNote < prevPrevNote and n < prevNote:
			pool[n] = pool[n] * 1.5
		elif scaliness > 30 and prevNote > prevPrevNote and n > prevNote:
			pool[n] = pool[n] * 1.5
		if complexity > 30 and onKey and ((i % 2 == 0 and arpeggioEven) or (i % 2 == 0 and not arpeggioEven)):
			pool[n] = pool[n] * 1.5
	
	#increase weights of closest scale notes
	n = nextInKey(key, prevNote, 1)
	if n in pool:
		pool[n] = pool[n] * 1.5
	else:
		pool[n] = 1.5
	n = nextInKey(key, prevNote, -1)
	if n in pool:
		pool[n] = pool[n] * 1.5
	else:
		pool[n] = 1.5
	
	if randint(0,100) <= dissonance:
		n = randint(int(prevNote - 14 * dissonance / 100), int(prevNote + 14 * dissonance / 100))
		if n in pool:
			pool[n] = pool[n] + 1 * dissonance / 100
		else:
			pool[n] = 2 * dissonance / 100
	
		
		
	selectedNotes = pool.keys()
	selection = list()
	for k in selectedNotes:
		selection.append((k, pool[k]))
	#print selection
	picked = choice(selection)
	if picked / 12 >= 7:
		picked = picked - 12
	#print picked
	return picked

	from random import uniform
		
	
def scales(octaveOffset, key, trebleTime, scaliness, complexity, velocity, dissonance, song, speed):
	time = 0
	notes = list()
	numTargets = randint(3,4)
	targets = list()
	targets.append(keys[key][0] + (4+octaveOffset) * 12)
	if numTargets == 3:
		if randint(0,1) == 0:
			targets.append(keys[key][randint(2,4)] + (5+octaveOffset) * 12)
			targets.append(keys[key][6] + 3 * 12)
		else:
			targets = list()
			targets.append(keys[key][0] + (5+octaveOffset) * 12)
			targets.append(keys[key][randint(2,4)] + (4+octaveOffset) * 12)
			targets.append(keys[key][6] + 3 * 12)
	if numTargets == 4:
		targets.append(keys[key][randint(2,3)] + (5+octaveOffset) * 12)
		targets.append(keys[key][randint(3,5)] + (3+octaveOffset) * 12)
		targets.append(keys[key][6] + (4+octaveOffset) * 12)
	i = targets[0]
	notelength = 2
	if randint(0,100) < complexity and (speed > 135 or speed < 120):
		notelength = 1
	elif randint(0,150) < speed:
		notelength = 4
	note = Note(i, btt(song, notelength), 60 + velocity, time)
	time = time + note.length
	notes.append(note)
	j = 0
	incMode = randint(0,1)
	frills = False
	frillMod = 4
	if randint(0,50) < complexity:
		frills = True
		frillMod = randint(4,6)
	count = 0
	while time < trebleTime:
		targ = targets[j%numTargets]
		#print 'targ ' + str(targ) + ' ' + str(i)
		while i != targ:
			if time > trebleTime:
				break
			
			note = Note(i, btt(song, notelength), 60 + velocity, time)
			if (randint(0,100) < 8 * (dissonance / 100)):
				note = Note(i, btt(song, notelength * 2), 60 + velocity, time)
			time = time + note.length
			notes.append(note)
			#print note.note
			if incMode == 0:
				if not frills:
					if targ < i:
						i = nextInKey(key, i, -1)
					else:
						i = nextInKey(key, i, 1)
				else:
					if targ < i:
						i = nextInKey(key, i, -1, frillMod, count)
					else:
						i = nextInKey(key, i, 1, frillMod, count)
			else:
				if targ < i:
					i = i - 1
				else:
					i = i + 1
			count = count + 1
		j = j + 1
	return notes
	
def generate(complexity=None, segments=None, dissonance=None, scaliness=None, speed= None, key=None, filename='Samples/NewSong'):
	print "Generating song!"
	if complexity is None:
		complexity = random(10, 100)
	if segments is None:
		segments = randint(3, 6)
	if dissonance is None:
		dissonance = random(0, 50)
	if scaliness is None:
		scaliness = random(20, 100)
	if key is None:
		if randint(0, 100) > dissonance:
			key = randint(0, (keyCount / 2))
		else:
			key = randint(0, keyCount)
	if speed is None:
		speed = random(40, 150)
		
	
	randomClass.seed(timeClass.clock)
	
	model = load_model('model1.dat')
	
	song = Song()
	song.tpb = 480
	song.tempo = mido.bpm2tempo(speed)
	
	segmentStore = list()
	basssegmentStore = list()
	tempoSeg = Seg()
	tempoSeg.notes.append(Note(999, 0, song.tempo, 0))
	song.segs.append(tempoSeg)
	if speed < 90 or speed > 135:
		song.baseunit = 8.0
	for i in range(segments):
		seg = Seg()
		seg.id = i
		seg.velocity = randint(-25, 25)
		#generate feature components Treble
		components = list()
		for i in range(int(random(1.0 + (100 - complexity) / 100 * 3,6 - (100 - complexity) / 100 * 3))):
			components.append(features[int(random(featuresMin + ((100 - complexity) / 100 * featuresMin * -.5) + 0.1, featuresMax - ((100 - complexity) / 100 * featuresMax * .5) - .01))])
		progression = list()
		for i in range(randint(4,8)):
			progression.append(components[randint(0,len(components) - 1)])
			
		noteCache = dict()
		time = 0
		prevPrevNote = 60
		q = deque(maxlen=6)
		note = Note(keys[key][int(random(0, 2))] + int(random(4,5) * 12), btt(song, progression[0][0]), 100 + seg.velocity, time)
		time = time + note.length
		seg.notes.append(note)
		q.append(note)
		noteCache[str(progression[0])] = list()
		noteCache[str(progression[0])].append(note)
		#print note.note
		for c,comp in enumerate(progression):
			if str(comp) not in noteCache:
				noteCache[str(comp)] = list()
			for i,t in enumerate(comp):
				if i == 0 and c == 0:
					continue
				if len(noteCache[str(comp)]) < len(comp):
					img = np.zeros((1, 6, 4, 1))
					img[:] = formImg(song.tempo, song.tpb, q)[0]
					result = model.predict_proba(img, verbose=0)
					#print result
					n = pickNote(dissonance, complexity, scaliness, key, result[0], note.note, prevPrevNote, True)
					prevPrevNote = note.note
					note = Note(n, btt(song, t), 80 + seg.velocity, time)
					if randint(0,100) < complexity / 2 and note.note > 10:
						note.chords.append(note.note - 4)
						if randint(0,100) < 50:
							note.chords.append(note.note - 7)
					q.append(note)
					noteCache[str(comp)].append(note)
					time = time + note.length
					seg.notes.append(note)
					#print 'vel:' + str(note.velocity)
				else:
					note = copy.copy(noteCache[str(comp)][i])
					note.time = time
					#print 'rep' + str(note.note)
					q.append(note)
					time = time + note.length
					seg.notes.append(note)
		trebleTime = time
		#generate scales instead of bass line
		if randint(0,80) < scaliness:
			notes = scales(0, key, trebleTime, scaliness, complexity, seg.velocity, dissonance, song, speed)
			for n in notes:
				seg.notes.append(n);
		else:
			components = list()
			for i in range(randint(2,3)):
				components.append(features[int(random(-2,6))])
			progression = list()
			for i in range(randint(5,10)):
				progression.append(components[randint(0,len(components) - 1)])
				
			noteCache = dict()
			time = 0
			q = deque(maxlen=6)
			note = Note(keys[key][int(random(0, 2))] + int(random(3,4) * 12), btt(song, progression[0][0]), 60 + seg.velocity, time)
			time = time + note.length
			seg.notes.append(note)
			q.append(note)
			noteCache[str(progression[0])] = list()
			noteCache[str(progression[0])].append(note)
			#print note.note
			for c,comp in enumerate(progression):
				if str(comp) not in noteCache:
					noteCache[str(comp)] = list()
				for i,t in enumerate(comp):
					if i == 0 and c == 0:
						continue
					if time > trebleTime:
						break
					if len(noteCache[str(comp)]) < len(comp):
						img = np.zeros((1, 6, 4, 1))
						img[:] = formImg(song.tempo, song.tpb, q)[0]
						result = model.predict_proba(img, verbose=0)
						#print result
						n = pickNote(dissonance, complexity, scaliness, key, result[0], note.note, prevPrevNote, False)
						prevPrevNote = note.note
						note = Note(n, btt(song, t), 50 + seg.velocity, time)
						if randint(0,100) < complexity / 2 and note.note > 10:
							note.chords.append(note.note - 4)
							if randint(0,100) < 50:
								note.chords.append(note.note - 7)
						q.append(note)
						noteCache[str(comp)].append(note)
						time = time + note.length
						seg.notes.append(note)
						
					else:
						note = copy.copy(noteCache[str(comp)][i])
						note.time = time
						#print 'rep' + str(note.note)
						q.append(note)
						time = time + note.length
						seg.notes.append(note)
		segmentStore.append(seg)
	#populate segments in song
	for i in range(segments):
		song.segs.append(copy.copy(segmentStore[i]))
	for i in range(randint(100,150)):
		song.segs.append(copy.copy(segmentStore[randint(0,len(segmentStore) - 1)]))
		
	#transpose!
	transSeg = randint(0,segments-1)
	seen = False
	for seg in song.segs:
		if not seen and seg.id == transSeg:
			seen = True
		elif seen and seg.id == transSeg:
			seg.transpose(1)
			seen = False
		#seg.transpose(1)
	#for i in range(segments / 2):
	#	song.basssegs.append(copy.copy(basssegmentStore[i]))
	#for i in range(randint(10,10)):
	#	song.basssegs.append(copy.copy(basssegmentStore[randint(0,len(basssegmentStore) - 1)]))
	print '\n\tSong Parameters:'
	print 'Complexity: \t' + str(complexity) + ' \nSegments: \t' + str(segments) + ' \nDissonance: \t' + str(dissonance) + ' \nScaliness: \t' + str(scaliness) + ' \nSpeed: \t\t' + str(speed) + ' \nKey: \t\t' + str(key)
	writeSong(song, filename)
	
for i in range(15,30):
	generate(filename='Samples/BatchSample' + str(i))
#generate(complexity=50, dissonance=0, scaliness=100, speed=70)	
		