from mido import Message, MidiFile, MidiTrack, MetaMessage
import mido as mido
from random import randint, random
import sys

from notes import noteDict
from structure import util, Seg, Song, Note
from read import read
from write import writeSong
#from gen import generate

#mid = MidiFile()
#track = MidiTrack()
#mid.tracks.append(track)
#
#track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(100)))
#track.append(Message('program_change', program=1, time=0))
#for n in util['basenotes']:
#	
#	track.append(Message('note_on', note=n, velocity=20, time=0))
#
#	track.append(Message('note_off', note=n, velocity=1, time=500))


#track.append(Message('note_on', note=60, velocity=127, time=0))
#
#track.append(Message('note_off', note=60, velocity=127, time=800))

#tempt = track.copy()
#for m in tempt:
#	track.append(m)
#print mid.ticks_per_beat

#song = read('midi/Chopin/chpn_op7_2')
song = read('This Game')
#for seg in song.segs:
#	for note in seg.notes:
#		print str(noteDict[note.note]) + ' ' + str(note.velocity) + ' ' + str(note.time)
#print song.tempo
writeSong(song, 'CopyThisGame')

#generate(complexity=100)