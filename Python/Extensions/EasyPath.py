class EasyPath():
	EaseFunctions = {
	"LinearInterpolation":0,
	"QuadraticEaseIn":1,
	"QuadraticEaseOut":2,
	"QuadraticEaseInOut":3,
	"CubicEaseIn":4,
	"CubicEaseOut":5,
	"CubicEaseInOut":6,
	"QuarticEaseIn":7,
	"QuarticEaseOut":8,
	"QuarticEaseInOut":9,
	"QuinticEaseIn":10,
	"QuinticEaseOut":11,
	"QuinticEaseInOut":12,
	"SineEaseIn":13,
	"SineEaseOut":14,
	"SineEaseInOut":15,
	"CircularEaseIn":16,
	"CircularEaseOut":17,
	"CircularEaseInOut":18,
	"ExponentialEaseIn":19,
	"ExponentialEaseOut":20,
	"ExponentialEaseInOut":21,
	"ElasticEaseIn":22,
	"ElasticEaseOut":23,
	"ElasticEaseInOut":24,
	"BackEaseIn":25,
	"BackEaseOut":26,
	"BackEaseInOut":27,
	"BounceEaseIn":28,
	"BounceEaseOut":29,
	"BounceEaseInOut":30
}

	def __init__(self, easerComp):
		self.easerComp = easerComp

		self.timer = easerComp.op("timer1")

		self._start = tdu.Dependency(0) 
		self._stop = tdu.Dependency(1) 
		self._duration = tdu.Dependency(10)


	@property
	def Start(self):
		return self._start
	@Start.setter
	def Start(self, start_val):
		self._start.val = start_val

	@property
	def Stop(self):
		return self._stop
	@Stop.setter
	def Stop(self, stop_val):
		self._stop.val = stop_val

	@property
	def Duration(self):
		return self._duration
	@Duration.setter
	def Duration(self, dur_val):
		self._duration.val = dur_val

	def PlayPath(self, func = "Linear", start = 0, stop = 1, duration = 10):
		self.func = self.EaseFunctions.get(func)
		if start == "r":
			self._start.val = me.parent().Pan
			self._stop.val = self._start.val + stop
		else:
			self._start.val = start 
			self._stop.val = stop
			
		self._duration.val = duration 

		self.timer.par.initialize.pulse()

		self.easerComp.par.Function = self.func

		self.timer.par.start.pulse()
	
	
	