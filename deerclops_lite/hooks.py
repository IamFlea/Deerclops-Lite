import time
import datetime as dt
#
import settings
from serverlogsreader import ServerLogsReader
from logparser import ServerInfo

if settings.release_version:
    import sys
    sys.stdout = open("/tmp/carrat_reader.out", "w")
    sys.stderr = open("/tmp/carrat_reader.err", "w")


######

SLEEP_TIME_SECONDS = 1 

class ProxyBot(object):
    """docstring for ProxyBot"""
    def __init__(self, shared_memory, client):
        super(ProxyBot, self).__init__()
        self.shared_memory = shared_memory
        self.logger = ServerLogsReader(settings.master_log, settings.cave_log)
        
        self.server_info = ServerInfo(client)

        self.time = "N/A"

    def checkLogs(self):
        self.server_info.clear()
        self.server_info.time = self.time
        for obj in self.logger: 
            self.server_info.checkObj(obj)


    def updateStatus(self):
        # Updates status        
        if self.server_info.sendUpdate: 
            try:
                msg = self.server_info.getPlayerListMessage()
                self.shared_memory[0] = msg
                #print(msg)
                
            except BrokenPipeError:
                print(f'{self.time}  [WARNING] Pipe is broken!', file=sys.stder)
            except TypeError:
                return

    def doRoutine(self, time):
        self.time = time
        self.logger.check()
        if self.logger:
            self.checkLogs()

            self.updateStatus()
        #print(self.server_info.players)
        #print(time)

    def run(self):
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        for server in self.servers:
            server.loop = loop
        """
        while True:
            timestamp_obj = dt.datetime.now()
            timestamp = timestamp_obj.strftime('%H:%M:%S')
            self.doRoutine(timestamp)
            
            # Sleep for a while
            time.sleep(SLEEP_TIME_SECONDS)

        
if __name__ == '__main__':
    pb = ProxyBot([None], {})
    pb.run()