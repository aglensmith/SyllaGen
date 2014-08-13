import os

from datetime import date, timedelta, datetime
import syllabus
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

#Add Non-alternating schedule feature


class Handler(webapp2.RequestHandler):
	
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
		
	def render(self, template, *args, **kw):
		self.write(self.render_str(template, **kw))
		
	def render_date_form(self, error):
		self.render("form_html.html")
				
	def getdates(self):
		
		#alter this function to return a dictionary instead of a list
		begin_date = str(self.request.get('begin_date'))
		end_date = str(self.request.get('end_date'))
		holiday1 = str(self.request.get('holiday1'))
		holiday2 = str(self.request.get('holiday2'))
		holiday3 = str(self.request.get('holiday3'))
		holiday_begin = str(self.request.get('holiday_begin'))
		holiday_end = str(self.request.get('holiday_end'))
		
		dates = []
		dates.append(begin_date)
		dates.append(end_date)
		
		for i in [holiday1, holiday2, holiday3, holiday_begin, holiday_end]:
			if i:
				dates.append(i)
		
		return dates
	
	def error_check(self):	
		"""checks if dates entered raise an error; returns true or false"""
		Syltest = syllabus.Syllabus()
		datestrs = self.getdates()

		valid = ' '
		no_error = True
		in_range = True
		error = ' '
		
		try:
			for i in datestrs:
				datetime.strptime(i, '%Y-%m-%d')
		except (ValueError, TypeError, OverflowError) as e:
			no_error = False
			error = e
		
		return no_error, error
				
	def in_range(self):
		"""checks that dates are valid; returns true or false"""
		#Possibly get rid of getdates() function -- just do request.get when necessary.
		datestrs = self.getdates()
		begin_date = datetime.strptime(datestrs[0], '%Y-%m-%d')
		end_date = datetime.strptime(datestrs[1], '%Y-%m-%d')
		
		
		#make function for this so that both begin_date/end_date & holiday_begin/holiday_end
		#can use it.
		if datetime.toordinal(begin_date) > datetime.toordinal(end_date):
			in_range = False
			error = 'Error: begin date should come before end date'
		elif datetime.toordinal(end_date) - datetime.toordinal(begin_date) > 100:
			in_range = False
			error = 'Error: begin date & end date too far apart'
		else:
			in_range = True
			error = ''
			
		#for extended holiday
		
		holiday_begin = self.request.get('holiday_begin')
		holiday_end = self.request.get('holiday_end')
		
		if (holiday_begin and holiday_end) and in_range == True:
			holiday_begin = datetime.strptime(holiday_begin, '%Y-%m-%d')
			holiday_end = datetime.strptime(holiday_end, '%Y-%m-%d')
			if datetime.toordinal(holiday_begin) > datetime.toordinal(holiday_end):
				in_range = False
				error = 'begin_date > end_date'
			elif datetime.toordinal(holiday_end) - datetime.toordinal(holiday_begin) > 100:
				in_range = False
				error = 'Error: Holiday length too long'
			else:
				in_range = True
				error = ''
		
				
		return in_range, error
	
	def valid_dates(self):
		
		no_error, error = self.error_check()
		in_range, message = self.in_range()
		error_message = error + message
		
		if in_range and no_error:
		
			Syl = self.make_syl()
			Syl.update()
		if self.no_errors() and self.in_range():
			return True
		else:
			return False
				
	def make_syl(self):
		"""gets the date strings from the html form, instatiates a syllabus object and return its"""
		Syl = syllabus.Syllabus()
		Syl.begin_date = Syl.makedate(str(self.request.get('begin_date')))
		Syl.end_date = Syl.makedate(str(self.request.get('end_date')))
		Syl.add_holiday(str(self.request.get('holiday1')), 
		str(self.request.get('holiday2')), str(self.request.get('holiday3')))
		
		if self.request.get('holiday_begin') and self.request.get('holiday_end'):
			Syl.add_exthol(str(self.request.get('holiday_begin')), str(self.request.get('holiday_end')))
		if self.request.get('holiday_begin2') and self.request.get('holiday_end2'):
			Syl.add_exthol(str(self.request.get('holiday_begin2')), str(self.request.get('holiday_end2')))
		return Syl
      
class MainPage(Handler):
	
	def get(self):
		self.render('form_html.html')
		
	def post(self):
		#working on adding error handling and validation

		begin_date = self.request.get('begin_date')
		end_date = self.request.get('end_date')
		holiday1 = self.request.get('holiday1')
		holiday2 = self.request.get('holiday2')
		holiday3 = self.request.get('holiday3')
		holiday_begin = self.request.get('holiday_begin')
		holiday_end = self.request.get('holiday_end')
		holiday_begin2 = self.request.get('holiday_begin2')
		holiday_end2 = self.request.get('holiday_end2')
		schedule = self.request.get('schedule')
		no_error, error = self.error_check()
		in_range = True

		if no_error == True:
			in_range, error = self.in_range()

		if in_range == True and no_error == True:
		
			Syl = self.make_syl()
			Syl.update()
			
			selecta = ''
			selectb = ''
			selectc = ''
			
			format1 = ''
			format2 = ''
			format3 = ''
			
			format = self.request.get('format')
			
			if format == 'sidebyside.html':
				format1 = 'selected'
				if schedule == 'a':
					syllabus = Syl.a
					selecta = 'selected'
				if schedule == 'b':
					syllabus = Syl.b
					selectb = 'selected'
				elif schedule != 'a' and 'b':
					syllabus = [Syl.makestr(i) for i in Syl.term_days]
					selectc = 'selected'
					format = 'table.html'
			if format == 'table.html':
				format2 = 'selected'
				if schedule == 'a':
					syllabus = [Syl.makestr(i) for i in Syl.adays]
					selecta = 'selected'
				if schedule == 'b':
					syllabus = [Syl.makestr(i) for i in Syl.bdays]
					selectb = 'selected'
				elif schedule != 'a' and 'b':
					syllabus = [Syl.makestr(i) for i in Syl.term_days]
					selectc = 'selected'
			if format == 'plaintext.html':
				format3 = 'selected'
				if schedule == 'a':
					syllabus = [Syl.makestr(i) for i in Syl.adays]
					selecta = 'selected'
				if schedule == 'b':
					syllabus = [Syl.makestr(i) for i in Syl.bdays]
					selectb = 'selected'
				elif schedule != 'a' and 'b':
					syllabus = [Syl.makestr(i) for i in Syl.term_days]
					selectc = 'selected'
				
			self.render('form_html.html', begin_date=begin_date, end_date=end_date, 
			holiday1=holiday1,holiday2=holiday2, holiday3=holiday3, 
			holiday_begin=holiday_begin, holiday_end=holiday_end,
            holiday_begin2 = holiday_begin2 , holiday_end2=holiday_end2, selecta=selecta, 
			selectb=selectb, selectc=selectc, format1=format1, format2=format2, format3=format3)
			
			self.render(format, syllabus=syllabus, schedule=schedule)
		else:
			self.render('form_html.html', error_message=error, begin_date=begin_date, end_date=end_date, 
			holiday1=holiday1,holiday2=holiday2, holiday3=holiday3, 
			holiday_begin=holiday_begin, holiday_end=holiday_end)
							

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
