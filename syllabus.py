from datetime import date, timedelta, datetime

class Syllabus(object):
	
	def __init__(self):
		self.begin_date = ''
		self.end_date = ''
		self.holidays = []
		self.exthol = []
		
	#updates the object attrs (used when holidays are added/removed)
	def update(self):
	
		self.term_days = self.gentrm()
		self.adays = self.altsched('a')
		self.bdays = self.altsched('b')
		self.a = self.week_list(self.adays)
		self.b = self.week_list(self.bdays)
	
	#converts date string into datetime object
	def makedate(self, arg):
		if isinstance(arg, str) and len(arg) > 0:
			return datetime.strptime(arg, '%Y-%m-%d')
		if isinstance(arg, int):
			return datetime.fromordinal(arg)
		if type(arg) == type([]):
			return [self.makedate(i) for i in arg]
	
	#converts a range of dates into a list of datetime objects
	def rangeofdates(self, begin, end):
		x = range(datetime.toordinal(begin), datetime.toordinal(end) + 1)
		return [self.makedate(i) for i in x]
	
	#coverts a datetime object to a string
	def makestr(self, date):
		return date.strftime("%A, %m/%d")

	#adds holidays to holiday list
	def add_holiday(self, *args): 
		[self.holidays.append(self.makedate(i)) for i in args]
		self.update()
		
	#adds extended holiday date range to holidays list
	def add_exthol(self, begin, end):
		for i in self.rangeofdates(self.makedate(begin), self.makedate(end)):
			self.holidays.append(i)
		self.update()
		
	def remove_holiday(self):
		return

	def print_holidays(self):
		for i in self.holidays:
			print self.makestr(i)
	
	#returns the week number
	def weeknum(self, dateobject):
		return dateobject.strftime('%W')

	#Return ALL class days from begin_date to end_date
	def gentrm(self):
		all_days = self.rangeofdates(self.begin_date, self.end_date)
		class_days = []
		for day in all_days:
			if date.weekday(day) < 5 and day not in self.holidays:
				class_days.append(day)
				
		return class_days
	
	#Returns alternating days for a schedule or b schedule
	def altsched(self, alt):
		term_days = self.gentrm()
		
		if alt == 'a':
			return term_days[::2]
		if alt == 'b':
			return term_days[1::2]
	
	#Return a list of lists of a or b day days grouped into weeks		
	def week_list(self, schedule):
	
		syl = []
		for day in schedule:
			if self.weeknum(day) != self.weeknum(schedule[schedule.index(day)-1]):
				syl.append(self.grpwk(day, schedule))
		return syl
	
	#Return a list of days from from either a or b days whos week number equals the given week number
	def groupweek(self, week, a_or_b_day):
		return [self.makestr(day) for day in a_or_b_day if int(self.weeknum(day)) == week]
		
	def grpwk(self, day, schedule):
		return [self.makestr(i) for i in schedule if self.weeknum(i) == self.weeknum(day)] 
 
	def prls(self, ls):
		for i in ls:
			print i
			
			
class Table(Syllabus):
	
	#updates the object attrs (used when holidays are added/removed)
	def update(self):
		
		self.term_days = self.gentrm()
		self.adays = self.altsched('a')
		self.bdays = self.altsched('b')
		self.a = self.adays
		self.b = self.adays
