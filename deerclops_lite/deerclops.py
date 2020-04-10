import discord
import random
import settings 
from utils import strDecompose


class Deerclops(discord.Client):
    def __init__(self):
        super(Deerclops, self).__init__()
        self.publicCommandList = {
            'hello' : self.cmdHelloWorld,
            'dst' : self.cmdServerInfo,
            'dft' : self.cmdServerInfo,
            'дст' : self.cmdServerInfo,
            'help' : self.cmdHelp,
            'man' : self.cmdHelp,
        }
        self.publicCommandMemes = {
            'meow' : self.cmdMeow,
            'woof' : self.cmdWoof,
            'birb' : self.cmdBirb,
            'bird' : self.cmdBirb,
            'quack' : self.cmdBirb,
        }

    # Alias for Placeholder
    def cmdHelloWorld(self):
        self.response = random.choice(settings.hello_responses)

    # Memes hello world
    # Creates embed response
    def sendRandomImage(self, image_type, image_count):
        rand = random.randint(1, image_count)
        img_url = f"https://nadeko-pictures.nyc3.digitaloceanspaces.com/{image_type}/{rand:03d}.png"
        self.response = discord.Embed()
        self.response.set_image(url=img_url)

    # Shows random cat
    def cmdMeow(self):
        self.sendRandomImage("cats", 772)
    
    # Shows random dog
    def cmdWoof(self):
        self.sendRandomImage("dogs", 749)

    # Shows random bird
    def cmdBirb(self):
        self.sendRandomImage("birds", 577)

    # Shows cat as princess Leia
    # TODO make better help
    def cmdHelp(self):
        self.response = f"""**Public commands**
    `{settings.prefix}hello`  Prints hello world
    `{settings.prefix}dst`  Show server info and who is online. You can also check #whois
    `{settings.prefix}dft`  Alias for dst cmd
    `{settings.prefix}дст`  Alias for dst cmd
    `{settings.prefix}help`  Prints this help
    `{settings.prefix}man`  Alias for help cmd

**Public commands that you can use at #meme**
    `{settings.prefix}meow`  Show "random" :cat: image
    `{settings.prefix}woof`  Show "random" :dog: image
    `{settings.prefix}birb`  Show "random" :bird: image
    `{settings.prefix}bird`  Alias for birb cmd
    `{settings.prefix}quack` Alias for birb cmd
Made with <3 by Kova
"""
    
    # Checks if the server is active or not. 
    def cmdServerInfo(self):
        try:
            self.response = self.last_msg
        except AttributeError:
            self.response = "Try it later."
        

    # Return the method from the  command list
    def _findInCommandList(self, commandList):
        for _cmd in commandList:
            if self.message.startswith(_cmd):
                return commandList[_cmd]
        return None


    def _getCommand(self):
        cmd = self._findInCommandList(self.publicCommandList )
        if cmd is not None:
            return cmd
        # Check if it is memes channel
        if self.server_name == 'memes':
            cmd = self._findInCommandList(self.publicCommandMemes)
        if cmd is not None:
            return cmd
        # default:
        return lambda: None


    async def parseCommands(self, message):
        # Optimize command parsing
        # Check if the first character is equal to command starter
        if not message.content:
            return
        if not message.content.startswith(settings.prefix):
            return 
        if message.channel.guild.id != settings.guild_id:
            print("Bad guild id")
            return 
        self.message = message.content[len(settings.prefix):]
        self.channel = message.channel
        self.server_name = message.channel.name
        try:
            self.author_name = message.author.name
            self.author_roles = [y.name for y in message.author.roles]
        except AttributeError: 
            self.author_roles = ["Admin"] if message.author.id in MAXWELLS else []
        # Result string and command
        self.response = None
        command = self._getCommand()
        # Run the command 
        command()
        # Send the response
        if self.response != None: 
            # Decompose the response and get the result 
            if isinstance(self.response, str):
                for response in strDecompose(self.response):
                    await message.channel.send(response)
            else:
                await message.channel.send(embed=self.response)


