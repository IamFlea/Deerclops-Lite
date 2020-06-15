# Discord Token.. Similar to DST klei's token.
# Do not reveal it! Else somebody could abuse it!!
token = "topsecret-discord-token"

# Full path to the Master log
master_log = "/home/dst/.klei/DoNotStarveTogether/Server1/Master/server_log.txt"


# Full path to the Cave log 
cave_log   = "/home/dst/.klei/DoNotStarveTogether/Server1/Caves/server_log.txt"


# Discord guild ID, channel id and message id for updating who is online 
guild_id = 11111111
channel_id = 22222222
message_id = 33333333

# Command prefix `.dst` or `!dst` or `$dst
prefix = "."

# This will move logs into `/tmp/` folder
# Set this true, if you want to run the bot on a background. I.e. `python3 main.py &`
# True | False
release_version = False

# Do you want to print icons next to the name? Else it prints text.
# True | False
with_icons = False
# Discord icons 
# If you want to change 
icon = {
    # Default icon (if icon not found below)
    '' : ':question:',
    # Player characters. Outsourced from DFT servers
    # If you want your own replace right column, you need to get the icon's ID. 
    # You can get it by adding the backslash before the icon name
    # E. g.   \:WilsonThinking:
    #passed
    'wilson': '<:WilsonThinking:452781866110418956>',
    'willow': ':grey_question:',
    'wolfgang': ':grey_question:',
    'wendy': '<:WendyTired:577065189795561472>',

    'wx78': '<:WX78Surprised:563769560981962752>',
    'wickerbottom': '<:WickerbottomShocked:530457512911044608>',
    'woodie' : ':grey_question:',
    'wes' : ':grey_question:',

    'waxwell' : ':grey_question:',
    'wathgrithr' : '<:WigfridAngry:577065278509416448>',
    'webber' : '<:Stewebber:635547294519001128>',
    'winona' : ':grey_question:',

    'wortox' :  ':grey_question:',
    'warly': ':grey_question:',
    'wormwood' : ':grey_question:',
    'wurt' : ':grey_question:', 

    'walter' : ':grey_question:', 
    # Misc. 
    'minerhat' : ':question:',

    # Day changes
    'day' : ':sunny:',
    'dusk' : ':white_sun_cloud:',
    'night' : ':crescent_moon:',
}

separator = "ᅚ"

# Some stupid stuff for status
# You can make some simple story here  or meme.. whatever
# this should indicate if the bot is not stucked. 
status_suffixes = [
    f'{separator}Nice one!',
    f'{separator}Chump!',
    f'{separator}Big head!',
    f'{separator}You stink!',
]
# Speed of changing the upper status suffixes
status_change_speed = 15

# Selects random response to `hello`
hello_responses = [
    f'Nice one!',
    f'Chump!',
    f'Big head!',
    f'You stink!',
]


