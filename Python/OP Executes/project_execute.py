# me - this DAT
# frame - the current frame
# state - True if the timeline is paused

import json
import TDJSON

def storePars():
	# this function is called on *saving* the project

	# make a json string and dump pars into it
	# all of these pars get values from extension attributes

	print("storing Soundscape pars...")

	Soundscape = json.dumps({
		"Panmin" : me.parent().Panmin.val,
		"Panmax" : me.parent().Panmax.val, 
		"Pan" : me.parent().Pan.val, 
		"Width" : me.parent().Width.val,
		"Distance" : me.parent().Distance.val,
		"Elevation" : me.parent().Elevation.val,
		"Cartesian" : me.parent().par.Cartesian.eval(),
		"Tx" : me.parent().Tx.val,
		"Ty" : me.parent().Ty.val
	})

	# string is stored in parent's storage dictionary
	me.parent().store("Soundscape",Soundscape)

	print("Soundscape pars stored!")


def fetchPars():
	# this function is called on *loading* the project

	# pars are fetched from parent's storage dictionary
	Soundscape = json.loads(me.parent().fetch("Soundscape"))

	# for each key:val pair, set the corresponding parameter
	for key, val in Soundscape.items():
		try:
			setattr(me.parent(), key, val)
		except AttributeError:
			# not entirely sure what this exception is about...
			me.parent().par.Cartesian = val


def onStart():
	fetchPars()

def onCreate():
	return

def onExit():
	return #sfp.storePars()

def onFrameStart(frame):
	return

def onFrameEnd(frame):
	return

def onPlayStateChange(state):
	return

def onDeviceChange():
	return

def onProjectPreSave():
	return

def onProjectPostSave():
	storePars()
