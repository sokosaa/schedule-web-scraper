# schedule-web-scraper
Fetches Drexel University's public master schedule and returns .ics files for easy import to your calendar of choice.

The last scrape was made on Jannuary 5, 2023 and the files created from that are available here: https://drive.google.com/drive/folders/1sCCcYJqeBMSnQKWlqBrv_si_sHSPS9D8?usp=sharing

Currently, the program is just one python file that goes to the Winter 22-23 Term and gets all schedules for every class that is synchronous (i.e. the time listed on the term master schedule is not "TBD") It takes a while to run, and throws all the .ics files into one folder, and then the user has to manually find their classes to add to their calendar. Also note: Classes which are not recurring and only meet on select specific days will only display first meeting of the class. This will be fixed soon.

The coming change will be user specific course selections, scraping in real time, and one .ics file as output.
