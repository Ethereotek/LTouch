# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value

# This will map the name of the parameter to its attribute in the extension
# i.e. {"par_name":"attr_name"}

par_map = {"Pan":"Pan",
			"Distance":"Distance",
			"Tx":"Tx",
			"Ty":"Ty",
			"Panrange1":"Panmin",
			"Panrange2":"Panmax"}

def onValueChange(par, prev):

		# set target_par to name of attr corresponding to changed par
	target_par = par_map.get(par.name)

		#
	if me.parent().par[par.name].enable == True:
		setattr(me.parent(), target_par, par.eval())
		print("attribute {} set".format(par.name))

		#print(target_par)




# # Called at end of frame with complete list of individual parameter changes.
# # The changes are a list of named tuples, where each tuple is (Par, previous value)
# def onValuesChanged(changes):
# 	for c in changes:
# 		# use par.eval() to get current value
# 		par = c.par
# 		prev = c.prev
# 	return

# def onPulse(par):
# 	return

# def onExpressionChange(par, val, prev):
# 	return

# def onExportChange(par, val, prev):
# 	return

# def onEnableChange(par, val, prev):
# 	return

# def onModeChange(par, val, prev):
# 	return
# 	