# schedule-web-scraper
Fetches Drexel University's public class information and returns .ics files for easy import to anyone's calendar of choice.
Example of scrapeable webpage: https://termmasterschedule.drexel.edu/webtms_du/collegesSubjects/202345?collCode=

The last scrape was made on March 27, 2023 for Spring Term and the files created from that are available here: https://drive.google.com/drive/folders/1csOfYbTootzJR39_Eh-OaNzF7GiFzTeo

The program is just one python file that goes to as specified term and gets all schedules for every class that is synchronous (i.e. the time listed on the term master schedule is not "TBD") It takes some time to run but throws all the .ics files into one folder. Then, anyone can easily manually find their classes to import it to their calendar, as fast as two taps on mobile.
