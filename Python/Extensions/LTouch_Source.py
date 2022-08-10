### Version 3.0
import math
import numpy

class Source:
		
	# this dictionary maps the L-Touch component's parameters
	# to the osc sub address for the L-ISA Controller parameters
	param_dict = {
		"Pan" : "p",
		"Width" : "w",
		"Distance" : "d",
		"Elevation" : "e"
	}

	presets_dict = {}

	def __init__(self, ownerComp, udpOp):
		
		print("LTOUCH extension created")

		self._pan_min = tdu.Dependency(-36.03)
		self._pan_max = tdu.Dependency(36.03)
		self._pan_range = tdu.Dependency(72.06)
		self.Presets = {"preset count":0}
		
		self.ownerComp = ownerComp
		self.Id = self.ownerComp.par.Id

		self.udpOp = udpOp
		self._ip = self.ownerComp.par.Ip
		self._recv_port = self.ownerComp.par.Recv
		self._dev_id = self.ownerComp.par.Deviceid
		self.par_presets = {}

		self.index = 'NaN'
		self.Name = tdu.Dependency(self.ownerComp.name)

		self.OSC_Sender = op("OSC_Output/oscout1")

########- PAN/WIDTH/DISTANCE/ELEVATION 
		# 
		# pwde attributes for polar/L-ISA Controller native
		# set to tdu Dependency using default par vals
		self._pan = tdu.Dependency(0.5)
		self._width = tdu.Dependency(0.0)
		self._distance = tdu.Dependency(0.5)
		self._elevation = tdu.Dependency(0.0)

		# Cartesian coordinates
		self._tx = tdu.Dependency(0.0)
		self._ty = tdu.Dependency(0.45)
		self._tz = tdu.Dependency(0.0)

#####-------------------------------------------------------#
	# 				POSITIONAL PROPERTIES 					#

	# one reason for doing this is to automatically calculate
	# between polar and cartesian coordinates

	#--------#
	# PAN #
	@property
	def Pan(self):
		# calling .Pan as an attribute
		# will return the private _pan 
		return self._pan

	@Pan.setter
	def Pan(self, p_val):

		# trying to set .Pan attribute
		# will run this function
		# first updating the value of _pan
		self._pan.val = p_val

		# then calculating cartesian coordinates
		# and assigning them to _tx and _ty
		# Note:
		# distance * math.sin(pan) is not appropriate
		# for calculating the pan/distance values for L-ISA
		# this is just a placeholder

		# further, this calculation should be in a separate function
		# that setter can call, since both pan and distance need to do this
		pan_ranged = self._reRange(0, 1, self._pan_min, self._pan_max, self._pan)

		tx = self._distance * math.sin(math.radians(pan_ranged))
		ty = self._distance * math.cos(math.radians(pan_ranged))
		#print(tx)
		self._tx.val = tx
		self._ty.val = ty 
		
	#-------------------#
	# DISTANCE #

	@property
	def Distance(self):
		return self._distance

	@Distance.setter
	def Distance(self, d_val):
		#print("Distance")
		self._distance.val = d_val 

		pan_ranged = self._reRange(0, 1, self._pan_min, self._pan_max, self._pan)
		tx = self._distance * math.sin(math.radians(pan_ranged))
		ty = self._distance * math.cos(math.radians(pan_ranged))

		self._tx.val = tx 
		self._ty.val = ty

	#-------------------#
	# ELEVATION #

	@property
	def Elevation(self):
		return self._elevation

	@Elevation.setter
	def Elevation(self, e_val):
		self._elevation.val = e_val
	
	#------------------------#
	# WIDTH #

	@property
	def Width(self):
		return self._width
	
	@Width.setter 
	def Width(self, w_val):
		self._width.val = w_val
	#------------------------#
	# TX #
	@property
	def Tx(self):
		return self._tx
	
	@Tx.setter
	def Tx(self, x_val):
		self._tx.val = x_val

		x = self._tx.val#self._reRange(0, 1, -1, 1, self._tx.val)
		y = self._ty.val#self._reRange(0, 1, -1, 1, self._ty.val)
		pan, distance = self._cart_to_polar(x, y)

		#print(pan, distance)
		# pan = math.atan(self._tx/self._ty)
		# distance = math.sqrt(math.pow(self._tx, 2) + math.pow(self._ty, 2))
		self._distance.val = distance
		self._pan.val = pan 
		 

	#-------------------------------#
	# TY #
	@property
	def Ty(self):
		return self._ty

	@Ty.setter
	def Ty(self, y_val):
		self._ty.val = y_val

		x = self._tx.val#self._reRange(0, 1, -1, 1, self._tx.val)
		y = self._ty.val#self._reRange(0, 1, -1, 1, self._ty.val)
		pan, distance = self._cart_to_polar(x, y)

		# pan = math.atan(self._tx/self._ty)
		# distance = math.sqrt(math.pow(self._tx, 2) + math.pow(self._ty, 2))

		self._pan.val = pan 
		self._distance.val = distance 

	#--------------------------------#
	# TZ coming soon

#####-------------------------------------------------------#
#	Coordinate system property
	# DEPRECATED 01/05/2022
	# @property
	# def Coordinate_System(self):
	# 	return self._coordinate_system
	# @Coordinate_System.setter
	# def Coordinate_System(self, cs_val):
	# 	self._coordinate_system.val = cs_val
	# 	if cs_val == 0:
	# 		self.ownerComp.par.Pan.enable = True
	# 		self.ownerComp.par.Distance.enable = True

	# 		self.ownerComp.par.Tx.enable = False
	# 		self.ownerComp.par.Ty.enable = False
	# 		self.ownerComp.par.Tz.enable = False

	# 	elif cs_val == 1:
	# 		self.ownerComp.par.Pan.enable = False
	# 		self.ownerComp.par.Distance.enable = False

	# 		self.ownerComp.par.Tx.enable = True
	# 		self.ownerComp.par.Ty.enable = True
	# 		self.ownerComp.par.Tz.enable = True

	@property
	def Panmin(self):
		return self._pan_min

	@Panmin.setter
	def Panmin(self, min_val):
		self._pan_min.val = min_val
		self._pan_range.val = self._pan_max.val - self._pan_min.val

	@property
	def Panmax(self):
		return self._pan_max

	@Panmax.setter
	def Panmax(self, max_val):
		
		self._pan_max.val = max_val
		self._pan_range.val = self._pan_max.val - self._pan_min.val

	@property
	def Panrange(self):
		return self._pan_range

	def Rotate(self, p, angle):

		self.p = p 
		self.angle = angle

		rot_mat = numpy.array([[math.cos(self.angle), -math.sin(self.angle)],
								[math.sin(self.angle), math.cos(self.angle)]])
		Rp = numpy.matmul(p, rot_mat)

		return Rp

	def _reRange(self, old_min, old_max, new_min, new_max, val):
		self.old_min = old_min
		self.old_max = old_max
		self.new_min = new_min
		self.new_max = new_max
		self.val = val 

		old_range = (self.old_max - self.old_min)
		new_range = (self.new_max - self.new_min)
		new_val = (((self.val - self.old_min) * new_range) / old_range) + self.new_min

		return new_val

	def ReRange(self, old_min, old_max, new_min, new_max, val):
		self.old_min = old_min
		self.old_max = old_max
		self.new_min = new_min
		self.new_max = new_max
		self.val = val 

		old_range = (self.old_max - self.old_min)
		new_range = (self.new_max - self.new_min)
		new_val = (((self.val - self.old_min) * new_range) / old_range) + self.new_min

		return new_val

	def _cart_to_polar(self, x, y):

		self.x = x
		self.y = y 

		# First step is to rotate coordinate plane 90 degrees
			# use numpy array to create [x,y] vector
		p = numpy.array([self.x, self.y])
			# matrix will rotate 90deg counterclockwise
		rotation_matrix = numpy.array([[0, -1], [1, 0]])
			# multiply vec p by rotation matrix
		r = numpy.matmul(p, rotation_matrix)

		# find the radius using pyth theorem, then angle using cos.
		# angle is in radians
		radius = math.sqrt(math.pow(r[0], 2) + math.pow(r[1], 2))

		angle = math.atan2(r[1],r[0])

		# DEPRECATED 01/13/2022
		# multiply angle times (x / |x|)
		# this tells us which direction we're going in
		# simultaneously flipping x axis (which now looks like y)
		# try statement in case x is 0, i.e. cannot divide by zero
		# NOTE: this returns angle in radians
		# try:
		# 	angle *= self.x/math.fabs(self.x)
		# except ZeroDivisionError:
		# 	angle = 0

		angle *= -1

		rad_min = math.radians(self._pan_min.val)
		rad_max = math.radians(self._pan_max.val)
		scale_to_circle = self._reRange(rad_min, rad_max, -math.pi, math.pi, angle)
		norm_angle = self._reRange(-math.pi, math.pi, 0, 1, scale_to_circle)

		distance = self.ReRange(0, 1, -0.3, 1, radius) #math.pow(radius, 2)
		if distance < 0:
			elevation = math.fabs(distance)
			self._elevation.val = math.fabs(self.ReRange(0, -0.3, 0, 1, elevation))
			distance = 0


		return norm_angle, distance
####
	def SavePreset(self, name):

		self.name = name
		# if "name" does not already exist in Presets dictionary (self.Presets) then:
		# add new preset to dictionary
		# increase the "preset count", i.e. number of presets in dict
		def write_to_dict(preset_name):
			self.Presets[self.name] = [
				self._pan.val,
				self._width.val,
				self._distance.val,
				self._elevation.val]

			self.Presets["preset count"] += 1 
		
		if not self.Presets.get(self.name):
			write_to_dict(self.name)
			# 08/10/2022 put this in write_to_dict() func
			# self.Presets[self.name] = [
			# 	self._pan.val,
			# 	self._width.val,
			# 	self._distance.val,
			# 	self._elevation.val]

			# self.Presets["preset count"] += 1

		else:
			
			message_text = "Preset \"{}\" already exists. Do you wish to overwrite this preset?".format(self.name)
			message_box = ui.messageBox("Warning", message_text, buttons=["Yes", "No"])

			if message_box == 0:
				write_to_dict(self.name)
			elif message_box == 1:
				pass
			

	def RecallPreset(self, name):
		self.name = name 

		try:
			pars = self.Presets.get(self.name)
			self._pan.val = pars[0]
			self._width.val = pars[1]
			self._distance.val = pars[2]
			self._elevation.val = pars[3]
		except TypeError:
			ui.messageBox("Error", "Preset \"{}\" does not exist".format(self.name), buttons=["Okay"])

	
### CUSTOM TOGGLE PARAMETER FUNCTIONS	


### CUSTOM PULSE PARAMETER FUNCTIONS
	def PushAllData(self):
		# Runs series of functions that send all data
		# that can be controlled via OSC
		self.PushFlags()
		self.PushPars()

	def PushPars(self):
		# Updates all soundscape parameters using current values
		
		src_id = self.Id 	# also self.ownerComp.par.Id
		self.OSC_Sender.sendOSC(
			"/ext/src/{}/p".format(src_id), [self._pan.val],
			"/ext/src/{}/w".format(src_id), [self._width.val],
			"/ext/src/{}/d".format(src_id), [self._distance.val],
			"/ext/src/{}/e".format(src_id), [self._elevation.val],
			"/ext/src/{}/s".format(src_id), [self.ownerComp.par.Auxsend.eval()],
			asBundle = True
			)

	def PushFlags(self):
		# Updates all control flags using current parameter selections
		panflag = self.ownerComp.par.Panflag 
		widthflag = self.ownerComp.par.Widthflag 
		distflag = self.ownerComp.par.Distanceflag
		elevflag = self.ownerComp.par.Elevationflag
		sendflag = self.ownerComp.par.Sendflag 

		src_id = self.Id 	# also self.ownerComp.par.Id
		self.OSC_Sender.sendOSC(
			"/ext/flag/src/{}/p".format(src_id), [panflag],
			"/ext/flag/src/{}/w".format(src_id), [widthflag],
			"/ext/flag/src/{}/d".format(src_id), [distflag],
			"/ext/flag/src/{}/e".format(src_id), [elevflag],
			"/ext/flag/src/{}/s".format(src_id), [sendflag],
			asBundle = True
			)

	def RegisterDevice(self):
		# Registers device for L-ISA to send OSC to

		ID = self._dev_id.eval()		# device ID (not source)
		IP = self._ip.eval()			# host IP address
		PORT = self._recv_port.eval()	# host receiving port

		# Register the device; give it the name L-TOUCH
		# Set L-ISA to receive OSC from
		# Set L-ISA to send OSC to
		# Set Parameter format to L-ISA

		self.OSC_Sender.sendOSC(
				"/ext/device/{}/register".format(ID),[IP, PORT],
				"/ext/device/{}/name".format(ID),["L-TOUCH"],
				"/ext/device/{}/receive".format(ID),[1],
				"/ext/device/{}/send".format(ID),[1],
				"/ext/device/{}/format".format(ID),["lisa"],
				asBundle = True
					)
		

	def Plug_Ping(self, port, machine, device, track_name, active, track_no, sender_op):
		self.port = port#.val
		self.machine = machine
		self.device = device
		self.track_name = track_name
		self.active = active
		self.track_no = track_no
		self.sender_op = sender_op

		#print(type(self.port))

		self.vals = [self.port, self.machine, self.device, self.track_name, self.active, self.track_no]

		self.sender_op.sendOSC('/plug/ping', self.vals, asBundle = True)


# 	def OSC_Ping(self, port, IP, sender_op, comments = None):
# 		self.port = port
# 		self.IP = IP
# 		self.sender_op = sender_op
# 		self.comments = comments

# 		self.message = "/ext/ping"

# 		self.sender_op.sendOSC(self.message, [self.IP, 9000])
