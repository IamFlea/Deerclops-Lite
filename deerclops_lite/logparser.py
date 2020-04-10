import settings

class ServerInfo(object):
    """
    This class parses the response of the log.
    It is one big mess...
    """
    def __init__(self, the_client):
        super(ServerInfo, self).__init__()
        self.client = the_client
        self.categories = {
            "newday": self.newDay,
            "newphase": self.newPhase,
            
            "disconnected_klei": self.dummy, #parse_players_dc
            "shard_disconnected": self.disconnected,
            "connected": self.parse_players,
            "joined": self.parse_players,
            "spawned": self.parse_players,
            "despawned": self.parse_players,
            "left": self.dummy,
        }

        self.phase = "n/a"
        self.day = "n/a"
        self.season = "n/a"
        self.maxplayers = "n/a"
        self.sendUpdate = False


        self.players = {}
        #print(f"player list id je {id(self.players)}")

    def disconnected(self, inst):
        uid = inst['userid']
        if uid in self.players: 
            del self.players[uid]
            self.sendUpdate = True

    def dummy(self, inst):
        pass 

    def newPhase(self, inst):
        if inst['cavelog']:
            return
        self.phase = inst['phase']
        self.sendUpdate = True

    def newDay(self, inst):
        if inst['cavelog']:
            return
        self.parse_players(inst)
        

    def parse_players(self,inst):
        #print(inst)
        for player in inst['players']:
            player['checked'] = True 
            self.addPlayer(player)
            #print(player)
        #print(self.players)
        deleted_players = []
        
        for val in self.players:
            player = self.players[val]
            if 'checked' in player:
                del player['checked']
            else:
                deleted_players += [val]
            player['cave'] = not player['cave'] and inst['cavelog'] and player['prefab'] != '' \
                        or player['cave'] and not inst['cavelog'] and player['prefab'] != ''
        for val in deleted_players:
            del self.players[val]
        self.updateDay(inst)
        self.sendUpdate = True
        #print(f"UPDATED player list id je {id(self.players)}")

    def addPlayer(self, player):
        #print(self.players)
        try:
            userid = player['userid']
        except KeyError:
            return        
        self.players[userid] = player


    # Checks griefiness and add announces
    def checkObj(self, inst):

        category = inst['category']
        if category in self.categories:
            self.categories[category](inst)
        else:
            #print("UNKOWN CATEGORY")
            pass

    def clear(self):
        self.sendUpdate = False
        self.banlist = []
        self.message = ''
        self.report_message = ''

    def updateDay(self, inst):
        self.day = inst['day']
        self.phase = inst['phase']
        self.season = inst['season']
        self.maxplayers = inst['maxplayers']
        try:
            self.season_len = inst['remainingdaysinseason']
        except KeyError:
            self.season_len = -1


    # Return string for updating the message for @deerclops
    def getPlayerListMessage(self):
        players_cnt = len(self.players)
        phase_icon = ""
        try:
            phase_icon = f" {settings.icon[self.phase]}"
        except KeyError:
            pass
        
        season_len = f" {self.season_len} days left" if self.season_len > -1 else ""

        text = "" #f"**Autoupdating message**\n"
        text += f"Day {self.day} ({self.season}{season_len}){phase_icon}\n"
        text += f"Total players: {players_cnt}/{self.maxplayers}\n"
        
        if players_cnt:
            names = map(lambda x: self.players[x]['name'], self.players)
            m_chars = max(map(len, names))
            def getAge(x):
                try:
                    return self.players[x]['age']
                except KeyError:
                    #print(x, self.players[x])
                    return 'N/A'

            days = map(getAge, self.players)
            m_chars_days = max(map(lambda x: len(str(x)), days))

            prefabs = map(lambda x: self.players[x]['prefab'], self.players)
            m_chars_prefabs = max(map(len, prefabs)) + 2

        for _, player in self.players.items():
            try:
                icon = settings.icon[player['prefab']]
            except:
                icon = ':grey_question:'

            if player['prefab'] == '':
                prefab_str = "[Selecting]"
            else:
                prefab_str = f"[{player['prefab'].capitalize()}]"
            
            
            name = player['name'].replace('`', '\'').ljust(m_chars, ' ')
            score = str(player['age']).rjust(m_chars_days, ' ')
            if player['cave']:
                cave_icon = f" {settings.icon['minerhat']}"  
                cave_string = f" (caves)"
            else:
                cave_icon = ''
                cave_string = ''
            if settings.with_icons:
                text += f"{icon} `{name}  {score} days`{cave_icon}\n"
            else: 
                prefab = prefab_str.ljust(m_chars_prefabs, ' ')
                text += f"`{prefab}  {name}  {score} days{cave_string}`\n"
        #print(text)
        return text


