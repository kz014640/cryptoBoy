from datetime import datetime, timedelta
import time

class BotTime(object):
    def __init__(self,totalDays):
        timeToday = datetime.today()
        backdatedTime = datetime.today() - timedelta(days=totalDays)
        self.timeToday = time.mktime(timeToday.timetuple())
        self.backdatedTime = time.mktime(backdatedTime.timetuple())
    
    def startDate(self):
        return self.timeToday

    def endDate(self):
        return self.backdatedTime