
from mido import Message, MidiFile, MidiTrack, MetaMessage
import mido as mido
import heapq
import copy

from notes import noteDict
from structure import util, Seg, Song, Note


def writeSong(song, filename):
	mid = MidiFile()
	track = MidiTrack()
	mid.tracks.append(track)
	#track.append(MetaMessage('set_tempo', tempo=song.tempo))
	track.append(Message('program_change', program=1, time=0))
	time = 0
	
	segtime = 0
	for seg in song.segs:
		h = []
		segtime = 0
		for note in seg.notes:
			heapq.heappush(h, (note.time, note, 'on'))
			heapq.heappush(h, (note.endtime, note, 'off'))
			for n in note.chords:
				temp = copy.copy(note)
				temp.note = n
				heapq.heappush(h, (note.time, temp, 'on'))
				heapq.heappush(h, (note.endtime, temp, 'off'))
			segtime = note.endtime
		time = time + segtime
		prevtime = 0
		while len(h) > 0:
			n = heapq.heappop(h)
			if n[1].note == 999:
				track.append(MetaMessage('set_tempo', tempo=n[1].velocity, time=0))
			else:
				track.append(Message('note_' + n[2], note=n[1].note, velocity=n[1].velocity, time=int(n[0] - prevtime)))
			prevtime = n[0]
	trebleTime = time
	time = 0
	for seg in song.basssegs:
		segtime = 0
		h = []
		for note in seg.notes:
			#print note.time
			heapq.heappush(h, (note.time, note, 'on'))
			heapq.heappush(h, (note.endtime, note, 'off'))
			for n in note.chords:
				temp = copy.copy(note)
				temp.note = n
				heapq.heappush(h, (note.time, temp, 'on'))
				heapq.heappush(h, (note.endtime, temp, 'off'))
			segtime = note.endtime
			if segtime + time > trebleTime:
				break
		time = time + segtime
		prevtime = 0
		while len(h) > 0:
			n = heapq.heappop(h)
			if n[1].note == 999:
				track.append(MetaMessage('set_tempo', tempo=n[1].velocity, time=0))
			else:
				#print 'writing!' + str(n[1].velocity)
				track.append(Message('note_' + n[2], note=n[1].note, velocity=n[1].velocity, time=int(n[0] - prevtime)))
			prevtime = n[0]
	mid.ticks_per_beat = song.tpb
	if '.mid' in filename:
		mid.save(filename)
	else:
		mid.save(filename + '.mid')
		