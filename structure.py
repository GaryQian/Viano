from notes import noteDict
from mido import Message, MidiFile, MidiTrack, MetaMessage
import mido as mido
from random import randint, random
import sys
import numpy as np

util = dict()
util['tempobpm'] = 120
util['tpb'] = 1024
util['complexity'] = 50
util['segments'] = 3
util['basenotes'] = [noteDict['c5'], noteDict['d5'], noteDict['e5'], noteDict['f5'], noteDict['g5'], noteDict['a5'], noteDict['b5']]

class Seg:
	notes = list()
	velocity = 0
	id = 0
	def __init__(self):
		self.notes = list()
	def transpose(self, n):
		for note in self.notes:
			num = note.note + 12 * n
			if num > 127:
				num = 127
			if num < 0:
				num = 0
			note.note = num
		
class Song:
	segs  = list()
	basssegs = list()
	tpb   = 480
	baseunit = 16.0
	def __init__(self):
		self.segs = list()

class Note:
	note     = 60
	chords   = list()
	length   = 480
	velocity = 100
	time     = 0
	endtime  = 480
	def __init__(self, note, length, velocity, time):
		self.note = note
		self.length = length
		self.velocity = velocity
		self.time = time
		self.endtime = time + length
		self.chords = list()
		
def formImg(tempo, tpb, notes):
	ar = np.zeros((6,4,1))
	y = None
	temp = None
	for i, n in enumerate(notes):
		if i < 6 and n is not None:
			temp = [[n.note * 100], [tempo / tpb * n.length], [n.velocity * 10], [mido.tempo2bpm(tempo) * 10]]
			ar[i,:,:] = temp
		else:
			y = n
	#print ar
	return [ar, y]