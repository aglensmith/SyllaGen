from datetime import date, timedelta, datetime
from syllabus import *

def test_makedate_string():
	assert Syl.makedate('2014-08-25') == datetime.strptime('2014-08-25', '%Y-%m-%d')
def test_makedate_empty():	
	assert Syllabus.makedate('') == None
def test_makedate_list():
	assert Syllabus.makedate(['2014-08-25', '2014-08-26']) == [datetime(2014, 8, 25), 
	datetime(2014, 8, 26)]
def test_makestr():
	assert Syllabus.makestr(datetime(2014, 8, 25)) == 'Monday, 08/25'
def test_weeknum():
	assert Syllabus.weeknum(datetime.today()) == datetime.today().strftime('%W')
#def test_generate_syllabus():
#	assert Syllabus.generate('a') == [
#	['Week1', 'Monday, 08/25', 'Wednesday, 08/27', 'Friday, 08/29'],
#	['Week2', 'Wednesday, 09/03', 'Friday, 09/05'], 
#	['Week3', 'Tuesday, 09/16', 'Thursday, 09/18'],
#	['Week4', 'Monday, 09/22', 'Wednesday, 09/24', 'Friday, 09/26'],
#	['Week5', 'Tuesday, 09/30', 'Thursday, 10/02'],
#	['week6', 'Monday, 10/06', 'Wednesday, 10/08', 'Friday, 10/10']]
def test_altsched_a():
	day_a = Syllabus.altsched('a')
	assert day_a[0] == Syllabus.term_days[0]
	assert day_a[1] != Syllabus.term_days[1]
	for i in day_a:
		assert date.weekday(i) != 5 or 6
									
									


