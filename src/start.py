import uuid
import copy

class Field:
    def __init__(self, name, value="", opt=""):
        self.name = name
        self.value = value
        self.opt = opt

    def load(self, lines):
        pass

    def dump(self):
        ret = self.name
        ret += ";%s"%(self.opt) if self.opt!="" else ""
        ret += ":%s"%(self.value)
        return ret


calendar_field_map = { x.name:x for x in [
    Field("VERSION", value="2.0"),
    Field("METHOD", value="PUBLISH"),
    Field("X-WR-TIMEZONE", value="Asia/Shanghai"),
    Field("X-APPLE-CALENDAR-COLOR", value="#540EB9"),
    Field("X-WR-CALNAME"),
] }

event_field_map = { x.name:x for x in [
    Field("UID"),
    Field("SEQUENCE", value="0"),
    Field("SUMMARY"),
    Field("DTSTART", opt="VALUE=DATE"),
    Field("DTEND", opt="VALUE=DATE"),
] }

alarm_field_map = { x.name:x for x in [
    Field("TRIGGER", opt="VALUE=DATE-TIME", value="19760401T005545Z"),
    Field("ACTION", opt="NONE"),
] }




"""
BEGIN:VALARM
TRIGGER;VALUE=DATE-TIME:19760401T005545Z
ACTION:NONE
END:VALARM
"""
class Alarm:
    def __init__(self):
        self._field_map = copy.copy(alarm_field_map)
    
    def load(self, lines):
        pass
    
    def dump(self):
        ret = ["BEGIN:VALARM"] 
        ret += [ x.dump() for x in self._field_map.values() ] 
        ret += ["END:VALARM"]
        return ret


"""
BEGIN:VEVENT
UID:2020-0124-0001
DTSTART;VALUE=DATE:20200124
DTEND;VALUE=DATE:20200124
SUMMARY:除夕     
SEQUENCE:0
END:VEVENT
"""
class Event:
    def __init__(self, summary="", dt=""):
        self._field_map = copy.deepcopy(event_field_map)
        self._field_map["UID"].value = uuid.uuid4()
        self._field_map["SUMMARY"].value = summary
        self._field_map["DTSTART"].value = dt
        self._field_map["DTEND"].value = dt
        self._alarm = Alarm()

    def load(self, lines):
        pass

    def dump(self):
        ret = ["BEGIN:VEVENT"]
        ret += [ x.dump() for x in self._field_map.values() ]
        ret += self._alarm.dump()
        ret += ["END:VEVENT"]
        return ret



"""
BEGIN:VCALENDAR
VERSION:2.0
X-WR-CALNAME:订阅法定节假日
X-APPLE-CALENDAR-COLOR:#540EB9
X-WR-TIMEZONE:Asia/Shanghai
METHOD:PUBLISH
"""
class Calendar:
    def __init__(self,name=""):
        self._field_map = copy.deepcopy(calendar_field_map)
        self._field_map["X-WR-CALNAME"].value = name
        self._events = []

    def load(self, lines):
        pass

    def dump(self):
        ret = ["BEGIN:VCALENDAR"]
        ret += [ x.dump() for x in self._field_map.values() ]
        for event in self._events:
            ret += event.dump()
        return ret

    def load_from_ics(self, filename):
        pass

    def save_as_ics(self, filename):
        with open(filename, "w") as f :
            for line in self.dump():
                f.write(line + '\n')

    def add_event(self, event):
        self._events.append(event)



def main():
    calendar = Calendar("test_calendar")
    calendar.add_event(Event(summary="act1", dt="20240224"))
    calendar.add_event(Event(summary="act2", dt="20240225"))
    calendar.add_event(Event(summary="act3", dt="20240226"))
    calendar.add_event(Event(summary="act4", dt="20240227"))
    calendar.save_as_ics("test.ics")



if __name__ == "__main__":
    main()