from mido import Message, MidiFile, MidiTrack, MetaMessage
import mido as mido
from random import randint, random
import sys
import numpy as np
from collections import deque
import copy
import cPickle
from multiprocessing import Pool

from notes import noteDict
from structure import util, Seg, Song, Note, formImg
from read import read
from write import writeSong

def evalFile(filename):
	song = read(filename)
	data = list()
	tempo = 500000
	bassq = deque([None, None, None, None, None, None], maxlen=7)
	trebleq = deque([None, None, None, None, None, None], maxlen=7)
	lasttime = 0
	lastnote = True #true if last note was treble
	for seg in song.segs:
		for i, note in enumerate(seg.notes):
			if note.note >= noteDict['c4']:
				trebleq.append(note)
				temp = copy.copy(note)
				temp.note = temp.note - 24
				bassq.append(temp)
				lastnote = True
			else:
				bassq.append(note)
				temp = copy.copy(note)
				temp.note = temp.note + 24
				trebelq.append(temp)
				lastnote = False
			lasttime = note.time
			break
		for i, note in enumerate(seg.notes):
			if note.note == 999:
				tempo = note.velocity
			elif note.time == lasttime:
				if lastnote and note.note > trebleq[-1].note:
					trebleq[-1] = note
				elif not lastnote and note.note < bassq[-1].note:
					bassq.append(note)
			elif note.note >= trebleq[-1].note - 14 and note.note > noteDict['c4']:
				trebleq.append(note)
				#trebleq.popleft()
				lastnote = True
				data.append(formImg(tempo, song.tbp, trebleq))
			else:
				bassq.append(note)
				#bassq.popleft()
				lastnote = False
				data.append(formImg(tempo, song.tpb, bassq))
	return data
	

import os

rootdir = 'C:\hophacks\midi'
filename = ''

data = list()
counter = 0
for subdir, dirs, files in os.walk(rootdir):
	#pool = Pool(processes=4)
	#files = list()
	for i, file in enumerate(files):
		
		if i % 20 == 0:
			#cPickle.dump(data, open( "rawdata.dat", "wb" ))
			print 'WritingData past ' + filename
		filename = os.path.join(subdir, file)
		print filename
		for res in evalFile(filename):
			data.append(res)
		#files.append(filename)
		#if counter % 4 == 0:
		#	results = [pool.apply_async(evalFile, [files[j]]) for j in range(4)]
		#	answers = [res.get(timeout=6) for res in results]
		#	wait(6)
		#	for res in answers:
		#		for obj in res:
		#			data.append(obj)
cPickle.dump(np.array(data), open( "rawdatadouble.dat", "wb" ))
cPickle.dump(np.array(data[0:50000]), open( "rawdatadoublesmall.dat", "wb" ))
				