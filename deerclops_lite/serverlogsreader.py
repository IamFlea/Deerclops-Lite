import json
import re 

from reader import Reader

#[BOT]
RE_DFTA = re.compile(r'^[^\s]*\s\[DFTA\] (.*)$', re.MULTILINE)
# Logging out of the caves

#RE_SIMPAUSED = re.compile(r'^[^\s]*\sSim paused$', re.MULTILINE)
RE_DISCONNECTED = re.compile(r'^[^\s]*\s\[Shard\] \(([^\)]*)\) disconnected from .*$', re.MULTILINE)


class ServerLogsReader(list):
    def __init__(self, path_master_log, path_cave_log):
        self.master_log = Reader(path_master_log)
        if path_cave_log:
            self.caves_log = Reader(path_cave_log)
        else:
            self.checkLogCave = lambda : None

    def checkLog(self, data, isCave):
        for msg in re.findall(RE_DFTA, data):
            if msg: 
                x = json.loads(msg)
                x['cavelog'] = isCave
                self.append(x)
                #print(x)
        for msg in re.findall(RE_DISCONNECTED, data):
            if msg: 
                x = {"category": "shard_disconnected", "userid": msg}
                self.append(x)
                #print(x)
                

    def checkLogMaster(self):
        data = self.master_log.read()
        self.checkLog(data, False)

    def checkLogCave(self):
        data = self.caves_log.read()
        self.checkLog(data, True)



    def check(self):
        # Clear the list
        self.clear()
        self.checkLogMaster()
        self.checkLogCave()
