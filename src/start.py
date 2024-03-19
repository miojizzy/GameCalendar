import uuid
import copy
import yaml

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
    Field("DTSTART", opt="VALUE=DATE-TIME"),
    Field("DTEND", opt="VALUE=DATE-TIME"),
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
    def __init__(self, conf):
        self._field_map = copy.deepcopy(event_field_map)
        self._field_map["UID"].value = uuid.uuid4()
        self._alarm = Alarm()

    def load(self, lines):
        pass

    def dump(self):
        ret = ["BEGIN:VEVENT"]
        ret += [ x.dump() for x in self._field_map.values() ]
        ret += self._alarm.dump()
        ret += ["END:VEVENT"]
        return ret
    
class LineEvent(Event):
    def __init__(self, conf):
        super().__init__(conf)
        self._field_map["SUMMARY"].value = conf["name"]
        self._field_map["DTSTART"].value = conf["start"]
        self._field_map["DTEND"].value = conf["end"]


class PointEvent(Event):
    def __init__(self, conf, tt):
        super().__init__(conf)
        if tt == "start":
            self._field_map["SUMMARY"].value = conf["name"] + " 开始"
            self._field_map["DTSTART"].value = conf["start"]
            self._field_map["DTEND"].value = conf["start"]
        else:
            self._field_map["SUMMARY"].value = conf["name"] + " 结束"
            self._field_map["DTSTART"].value = conf["end"]
            self._field_map["DTEND"].value = conf["end"]



"""
BEGIN:VCALENDAR
VERSION:2.0
X-WR-CALNAME:订阅法定节假日
X-APPLE-CALENDAR-COLOR:#540EB9
X-WR-TIMEZONE:Asia/Shanghai
METHOD:PUBLISH
"""
class Calendar:
    def __init__(self, conf):
        self._field_map = copy.deepcopy(calendar_field_map)
        self._field_map["X-WR-CALNAME"].value = conf["name"]
        #self._events = [ LineEvent(event) for event in conf["events"] ]
        self._events = []
        for event in conf["events"]:
            self._events.append(PointEvent(event, "start"))
            self._events.append(PointEvent(event, "end"))
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

    def save_as_ics(self):
        filename="%s.ics"%(self._field_map["X-WR-CALNAME"].value)
        with open(filename, "w") as f :
            for line in self.dump():
                f.write(line + '\n')




def main():
    with open("conf/conf.yaml", "r") as f:
        data = yaml.load(f,Loader=yaml.FullLoader)
        for item in data:
            calendar = Calendar(item)
            calendar.save_as_ics()



if __name__ == "__main__":
    main()