import os

from datetime import date, timedelta, datetime
import webapp2
import jinja2

#joins this file with the template.html file
template_dir = os.path.join(os.path.dirname(__file__), 'templates')

#instatiates jinja environment, uses filesystem loader using template_dir variable
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def generate_ext_holiday(holiday_begin, holiday_end):
	
	ext_holiday = []
	for i in range(datetime.toordinal(holiday_begin), datetime.toordinal(holiday_end)):
		ext_holiday.append(datetime.fromordinal(i))
		return ext_holiday
	
def strptime(date_string):
	date_object = datetime.strptime(date_string, '%Y-%m-%d')
	return date_object
	
def weeknum(dateobject):
	dateobject = dateobject
	week_number = dateobject.strftime('%W')
	return str(week_number)
	
def weeknumlist(dates):
	dates = dates
	weeks_list = []
	
	for i in dates:
		if weeknum(i) not in weeks_list:
			weeks_list.append(str(weeknum(i)))
	return weeks_list

def weekdict(black_dates, gold_dates):
	
	black_dates = black_dates
	gold_dates = gold_dates
		
	black_dict ={}
	for i in range(len(black_dates)):	
		week_number = weeknum(black_dates[i])
		if week_number not in black_dict:
			black_dict[week_number] = []
		black_dict[week_number].append(black_dates[i].strftime("%A, %m/%d"))
		
	gold_dict ={}
	for i in range(len(gold_dates)):	
		week_number = weeknum(gold_dates[i])
		if week_number not in gold_dict:
			gold_dict[week_number] = []
		gold_dict[week_number].append(gold_dates[i].strftime("%A, %m/%d"))
		
	return black_dict, gold_dict

def generate_syllabi(dates_from_user):
	
	begin_date = dates_from_user[0]
	end_date = dates_from_user[1]
	holiday_list = dates_from_user[2]
	ext_holiday = dates_from_user[3]
	
	if ext_holiday:
		ext_holiday = generate_ext_holiday(ext_holiday[0], ext_holiday[1])
	
	for i in ext_holiday:
		holiday_list.append(i)
	
	# holiday_list.append(datetime(2014, 9, 1))
	
	x = 0
	delta = timedelta(days=x)
	next_date = begin_date + delta
	syl_list = []
	
	while next_date != end_date:
		delta = timedelta(days=x)
		next_date = begin_date + delta
		
		if (date.weekday(next_date) < 5) and (next_date not in holiday_list):
			syl_list.append(next_date)
		x +=1
		

	black_syl = []
	gold_syl = []


	for i in syl_list[::2]:
		black_syl.append(i)

	for i in syl_list[1::2]:
		gold_syl.append(i)
		
	return black_syl, gold_syl	

class Handler(webapp2.RequestHandler):
	
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	#takes a filename and extra parameters, uses get_template function to get template.html,
	#then uses render() to render the .html with the given parameters
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
		
	#sends the rendered string to the browser with the given template.html file and parameters
	def render(self, template, *args, **kw):
		self.write(self.render_str(template, **kw))
		
	def render_date_form(self, error):
		self.render("form_html.html")
		
	def valid_dates(self, date_string_list):	
		
		begin_string = date_string_list[0]
		end_string = date_string_list[1]
		
		valid = ' '
		no_error = True
		in_range = True
		error = ' '
		
		try:
			date_objects = self.convert_dates(date_string_list)
		except ValueError:
			no_error = False
			error = 'ValueError'
		except TypeError:
			no_error = False
			error = 'TypeError'
		except OverflowError:
			no_error = False
			error = 'OverflowError'
			
		if no_error == True:
			
			begin_date = strptime(begin_string)
			end_date = strptime(end_string)
			
			if datetime.toordinal(begin_date) > datetime.toordinal(end_date):
				in_range = False
				error = 'begin_date > end_date'
			elif datetime.toordinal(end_date) - datetime.toordinal(begin_date) > 100:
				in_range = False
				error = 'end date - begin date > 100 days'
				
		
		if (no_error == True) and (in_range == True):
			return True, error
		else:
			return False, error
							
	def get_date_strings(self):
		date_string_list = []
		holiday_list = []
		ext_holiday_list = []
		begin_date = self.request.get('begin_date')
		end_date = self.request.get('end_date')
		
		holiday1 = self.request.get('holiday1')
		holiday2 = self.request.get('holiday2')
		holiday3 = self.request.get('holiday3')
		
		holiday_begin = self.request.get('holiday_begin')
		holiday_end = self.request.get('holiday_end')
		
		if holiday1:
			holiday_list.append(holiday1)
		if holiday2:
			holiday_list.append(holiday2)
		if holiday3:
			holiday_list.append(holiday3)
		if holiday_begin:
			ext_holiday_list.append(holiday_begin)
		if holiday_end:
			ext_holiday_list.append(holiday_end)
			
		date_string_list.append(begin_date)
		date_string_list.append(end_date)
		date_string_list.append(holiday_list)
		date_string_list.append(ext_holiday_list)
		
		return date_string_list
	
	def convert_dates(self, date_string_list):
		
		begin_date = date_string_list[0]
		end_date = date_string_list[1]
		
		holiday_list = []
		for i in date_string_list[2]:
			i = datetime.strptime(i, '%Y-%m-%d')
			holiday_list.append(i)
		
		ext_holiday = []
		for i in date_string_list[3]:
			i = datetime.strptime(i, '%Y-%m-%d')
			ext_holiday.append(i)
			
		begin_date = datetime.strptime(begin_date, '%Y-%m-%d')
		end_date = datetime.strptime(end_date, '%Y-%m-%d')
		
		dates = []
		dates.append(begin_date)
		dates.append(end_date)
		dates.append(holiday_list)
		dates.append(ext_holiday)
		return dates
			
class MainPage(Handler):
	
	def get(self):
		self.render('form_html.html')
		
	def post(self):
		
		date_strings_list = self.get_date_strings()
			
		all_dates_valid, error = self.valid_dates(date_strings_list)
		
		if all_dates_valid == True:
			
			date_objects = self.convert_dates(date_strings_list)
		
			black_dates, gold_dates = generate_syllabi(date_objects)
			
			black_week_list = weeknumlist(black_dates)
			gold_week_list = weeknumlist(gold_dates)
			
			black_syl, gold_syl = weekdict(black_dates, gold_dates)
			
			self.render('form_html.html')
			self.render('syllabus_html.html', 
						black_syl=black_syl, 
						gold_syl=gold_syl,
						black_week_list=black_week_list,
						gold_week_list=gold_week_list)		
		
		error_message = 'Invalid dates: %s.' % error
		if all_dates_valid == False:
				self.render('form_html.html', error_message=error_message)
				date_strings_list = self.get_date_strings()
				all_dates_valid = self.valid_dates(date_strings_list)
						
class SyllabusHandler(Handler):

	def post(self):
		
		date_strings = self.get_date_strings()	
		dates = self.convert_dates(date_strings)
		black_dates, gold_dates = generate_syllabi(dates)
		
		black_week_list = weeknumlist(black_dates)
		gold_week_list = weeknumlist(gold_dates)
		
		black_syl, gold_syl = weekdict(black_dates, gold_dates)
		
		self.render('syllabus_html.html', 
					black_syl=black_syl, 
					gold_syl=gold_syl,
					black_week_list=black_week_list,
					gold_week_list=gold_week_list)
		
app = webapp2.WSGIApplication([('/', MainPage), ('/syllabus', SyllabusHandler)], debug=True)
