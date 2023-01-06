import time as sleepytime
import webbrowser
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dateutil.parser import parse
from datetime import datetime, time, date, timedelta
import pytz
import icalendar
import shutil

'''
import warnings
warnings.filterwarnings('ignore','A device attached to the system is not functioning.')
    except Exception as e:
        if 'A device attached to the system is not functioning.' in str(e):
            pass
        else:
            raise e
'''

# Open the webpage in a browser
driver = webdriver.Chrome()
driver.get('https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202225?collCode=')

n = range(1,100) # can use crazy high range because added break to for loop if TimeoutException. Also, starting with 1 as thats the first xpath identifying index.
n1 = range(1,20) # Number of list of colleges along left hand side of term master schedule +2
n2 = range(1,50) # Number of major/class-types (the button in the middle of the webpage)+2
n3 = range(1,500) # Number of classes within each major/class-type +a lot

#def click_element(xpath0)

def create_ics():
    for i in range(len(events)):
        if events[i]=='async':
            break
        # Create a calendar
        cal = icalendar.Calendar()
        cal.add('prodid', '-//My Calendar//mxm.dk//')
        cal.add('version', '2.0')

        # Add the recurring event
        event = icalendar.Event()
        event.add('summary', events[i][0])
        event.add('location', events[i][1])
        event.add('description', events[i][2])
        event.add('dtstart', datetime.strptime(events[i][3], '%Y%m%dT%H%M%S'))
        event.add('dtend', datetime.strptime(events[i][4], '%Y%m%dT%H%M%S'))
        event.add('dtstamp', datetime.strptime(events[i][7], '%Y-%m-%d %H:%M:%S.%f%z'))
        event.add('rrule', {'freq': 'weekly', 'byday': events[i][6], 'until': datetime.strptime(events[i][5], '%Y%m%dT%H%M%S')}) #'count': weeks*len(eventdays)
        cal.add_component(event)

        # make the file name
        mainpart = events[i][0].split(' - ')
        if events[i][2][9] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            otherpart = events[i][2][9]
        else:
            otherpart = events[i][2][9:13]
        file_name = mainpart[0].replace(" ", "-")+'-'+otherpart.strip()+'.ics'
        print(file_name)
        
        # Write the calendar to a file
        with open(file_name, 'wb') as f:
            f.write(cal.to_ical())
        shutil.move(file_name, 'ics_files/'+file_name)

def readx(xpath_string):
    xpath_search = wait.until(EC.presence_of_element_located((By.XPATH, xpath_string)))
    extracted_text = xpath_search.text
    return extracted_text

def read_page():
    sleep()
    # Wait for the element to be present
    wait = WebDriverWait(driver, 3)
    
    # first check if no time availble so program moved on to next item if so
    Times = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[3]')
    if Times == 'TBD':
        return 'async'

    # Get title/EventName info
    SubjectCode = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]')
    CourseNumber = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]')
    Title = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[6]/td[2]')
    EventName = SubjectCode+' '+CourseNumber+' - '+Title

    # Get location info
    Building = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[5]')
    Room = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[6]')
    Campus = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[7]/td[2]')
    if Campus == 'Online' or Campus == 'Remote':
        Location = 'Online'
    else:
        Location = Building+', '+Room+' ('+Campus+')'

    # Get descrtiption info
    Section = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]')
    #Section = '<b>Section: </b>'+Section
    Section = 'Section: '+Section
    CRN = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]')
    #CRN = '<b>CRN: </b>'+CRN
    CRN = 'CRN: '+CRN
    Credits = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[5]/td[2]')
    #Credits = '<b>Credits: </b>'+Credits
    Credits = 'Credits: '+Credits
    Instructors = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[8]/td[2]')
    #Instructors = '<b>Instructor(s): </b>'+Instructors
    Instructors = 'Instructor(s): '+Instructors
    InstructionType = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[9]/td[2]')
    #InstructionType = '<b>Type: </b>'+InstructionType
    InstructionType = 'Type: '+InstructionType
    #InstructionMethod = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[10]/td[2]')
    MaxEnroll = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[11]/td[2]')
    #MaxEnroll = '<b>Max Enroll: </b>'+MaxEnroll
    MaxEnroll = 'Max Enroll: '+MaxEnroll
    Enroll = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[12]/td[2]')
    #Enroll = '<b>Enroll: </b>'+Enroll
    Enroll = 'Enroll: '+Enroll
    SectionComments = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/table/tbody/tr[13]/td[2]/table/tbody/tr/td')
    #SectionComments = '<b>Section Comments: </b>'+SectionComments
    SectionComments = 'Section Comments: '+SectionComments
    CourseDescription = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div[1]')
    CourseDescription = CourseDescription[20:]
    #CourseDescription = '<b>Course Description: </b>'+CourseDescription
    CourseDescription = 'Course Description: '+CourseDescription
    College = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div[3]')
    College = College[9:]
    #College = '<b>College: </b>'+College
    College = 'College: '+College
    Department = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div[4]')
    Department = Department[12:]
    #Department = '<b>Department: </b>'+Department
    Department = 'Department: '+Department
    #if SectionComments=='<b>Section Comments: </b>None':
    if SectionComments=='Section Comments: None':
        Description = Section+'\n'+Instructors+'\n'+InstructionType+'\n'+Credits+'\n\n'+MaxEnroll+'\n'+Enroll+'\n'+CRN+'\n'+College+'\n'+Department+'\n\n'+CourseDescription
    else:
        Description = Section+'\n'+Instructors+'\n'+InstructionType+'\n'+Credits+'\n\n'+MaxEnroll+'\n'+Enroll+'\n'+CRN+'\n'+College+'\n'+Department+'\n'+SectionComments+'\n\n'+CourseDescription

    # Get time info (and Parse the time string into a time object)
    time_format = '%I:%M %p'
    StartTime = datetime.strptime(Times.split(' - ')[0], time_format).time()
    EndTime = datetime.strptime(Times.split(' - ')[1], time_format).time()

    # Get days of the week recurrance info
    Days1L = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[4]')
    Days = []
    if 'TBD' in Days1L: Days.append('TBD')
    else:
        if 'M' in Days1L: Days.append('MO')
        if 'T' in Days1L: Days.append('TU')
        if 'W' in Days1L: Days.append('WE')
        if 'R' in Days1L: Days.append('TH')
        if 'F' in Days1L: Days.append('FR')

    # Get date info (of first occurance)
    FirstDate = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[1]')
    FirstDate = parse(FirstDate).date()
    #FirstDate = FirstDate.strftime('%Y%m%d')
    if str(FirstDate) == '2023-01-09':
        if 'MO' in Days:
            delta = timedelta(days=0)
        elif 'TU' in Days:
            delta = timedelta(days=1)
        elif 'WE' in Days:
            delta = timedelta(days=2)
        elif 'TH' in Days:
            delta = timedelta(days=3)
        elif 'FR' in Days:
            delta = timedelta(days=4)
        FirstDate += delta
     
    # Combine date and time info (combine date and time objects into a single datetime object, and then convert to string in the desired format)
    FirstDateStartTime = datetime.combine(FirstDate, StartTime)
    FirstDateEndTime = datetime.combine(FirstDate, EndTime)
    FirstDateStartTime = FirstDateStartTime.strftime('%Y%m%dT%H%M%S')
    FirstDateEndTime = FirstDateEndTime.strftime('%Y%m%dT%H%M%S')

    # Get date info (of end date)
    LastDate = readx('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]')
    LastDate = parse(LastDate).date()
    LastDate = LastDate.strftime('%Y%m%d')
    LastDate = LastDate+'T000000'
    
    # Get current time to know when this program read the term master schedule (get UTC time and convert to EST)
    utc_time = datetime.utcnow()
    est_time = utc_time.astimezone(pytz.timezone('US/Eastern'))
    timestamp = str(est_time)
    
    '''
    all_vars = locals()
    all_vars.pop('wait')
    all_vars.pop('Times')
    all_vars.pop('time_format')
    all_vars.pop('StartTime')
    all_vars.pop('EndTime')
    all_vars.pop('Days1L')
    '''
    
    return EventName, Location, Description, FirstDateStartTime, FirstDateEndTime, LastDate, Days, timestamp

def sleep():
    sleepytime.sleep(0.2) #increase if slow internet connection while using program

events = []

sleep()
for i in n1: 
    sleep()
    si = str(i)
    xpath1 = '//*[@id="sideLeft"]/a['+si+']'
    # Wait for the element to be present
    wait = WebDriverWait(driver, 5)
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath1)))
        element.click()
    except TimeoutException:
        break

    for j in n2:
        sleep()
        sj = str(j)
        xpath2 = '/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr[3]/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/div['+sj+']/a'
        # Wait for the element to be present
        wait = WebDriverWait(driver, 5)
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath2)))
            element.click()
        except TimeoutException:
            break

        for k in n3:
            sleep()
            sk = str(k)
            xpath3 = '//*[@id="sortableTable"]/tbody[1]/tr['+sk+']/td[6]/span/a'
            # Wait for the element to be present
            wait = WebDriverWait(driver, 5)
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath3)))
                element.click()
            except TimeoutException:
                driver.back()
                break
            events.append(read_page()) #useless list as its reset every iteration - will be removed 
            create_ics()
            events = [] 
            driver.back()

driver.close()
