from mido import Message, MidiFile, MidiTrack, MetaMessage
import mido as mido

from notes import noteDict
from structure import util, Seg, Song, Note



def read(filename):
	song = Song()
	song.segs.append(Seg())
	mid = None
	if '.mid' not in filename:
		mid = MidiFile(filename + '.mid')
	else:
		mid = MidiFile(filename)
	song.tpb = mid.ticks_per_beat
	for i, track in enumerate(mid.tracks):
		if i != 1:
			for m in mid:
				#print m
				if m.type == 'set_tempo':
					song.tempo = m.tempo
		else:
			activeNotes = list()
			activeNotesData = dict()
			time = 0
			tempNote = None
			for m in mid:
				#print m
				if m.type == 'set_tempo':
					song.tempo = m.tempo
					song.segs[0].notes.append(Note(999, 0, m.tempo, time))
					#print m.tempo
				#print mid.length
				time = time + m.time * song.tpb * mido.tempo2bpm(song.tempo) / 60
				#print time
				if m.type == 'note_on':
					if m.note in activeNotes and activeNotesData[m.note] != None:
						tempNote = activeNotesData[m.note]
						song.segs[0].notes.append(Note(m.note, time - tempNote[1], tempNote[0].velocity, tempNote[1]))
					activeNotes.append(m.note)
					activeNotesData[m.note] = (m, time)
				elif m.type == 'note_off':
					if m.note in activeNotes and activeNotesData[m.note] != None:
						tempNote = activeNotesData[m.note]
						song.segs[0].notes.append(Note(m.note, time - tempNote[1], tempNote[0].velocity, tempNote[1]))
						#print time - tempNote[1]
						activeNotes.remove(m.note)
						activeNotesData[m.note] = None
	#song.tempo = int(song.tempo * 1)
	return song
			