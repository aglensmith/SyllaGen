import webapp2
from datetime import date, timedelta, datetime
from main import *
import unittest

class Handler(Handler):
	pass

class TestSylGen(unittest.TestCase):
		
	def get_date_strings(self):
		
		date_string_list = []
		holiday_list = []
		ext_holiday_list = []
		
		begin_date = '2014-8-25'
		end_date = '2014-10-03'
		
		holiday1 = '2014-09-01'
		holiday2 = ''
		holiday3 = ''
		
		holiday_begin = '2014-9-14'
		holiday_end = '2014-9-19'
		
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
	
	def testGet_date_strings(self):
		self.assertEqual(['2014-8-25', 
						  '2014-10-03', 
						 ['2014-09-01'], 
						 ['2014-9-14', '2014-9-19']], 
						 self.get_date_strings())
						 
						 
	def testConvert_dates(self):
		
		self.assertEqual([datetime.strptime('2014-8-25', '%Y-%m-%d'), 
						  datetime.strptime('2014-10-03', '%Y-%m-%d'), 
						 [datetime.strptime('2014-09-01', '%Y-%m-%d')], 
						 [datetime.strptime('2014-9-14', '%Y-%m-%d'), 
						 datetime.strptime('2014-9-19', '%Y-%m-%d')]],
						 self.convert_dates(self.get_date_strings()))
	def testExt_Holiday(self):
		self.assert
						 
unittest.main()


		