import sys
from g_python.gextension import Extension
from g_python.hmessage import Direction

extension_info = {
    "title": "Dodgeball Bot",
    "description": ":dballcmd to see commands",
    "version": "0.1",
    "author": "Yarkin"
}

ext = Extension(extension_info, sys.argv, silent=True)
ext.start()

allowed_values = []
dodgeball = False
x = 0
y = 0

def coords(coord):
    global x, y, dodgeball
    if dodgeball:
        _, x, y, _ = coord.packet.read("iiii")
        ext.send_to_client('{in:Whisper}{i:-1}{s:"Coords set to: x: ' +str(x)+ ' y: '+str(y)+ '"}{i:0}{i:34}{i:0}{i:-1}')

def dice(dice):
    global allowed_values, x, y, dodgeball
    diceid, num = dice.packet.read('ii')
    if num in allowed_values:
        print(diceid, num)
        ext.send_to_server('{out:MoveAvatar}{i:' + str(x) + '}{i:' + str(y) + '}')

def message(message):
    global allowed_values, dodgeball
    (text, color, index) = message.packet.read('sii')
    if dodgeball is not False and text.lower().startswith(':num '):
        try:
            nums = [int(num) for num in text.split(' ')[1:]]
            if all(1 <= num <= 6 for num in nums):
                allowed_values = nums
                message.is_blocked = True
                ext.send_to_client('{in:Whisper}{i:-1}{s:"Dice numbers set to ' + str(allowed_values) + '"}{i:0}{i:34}{i:0}{i:-1}')
        except:
            pass
    else:
        print("idk")

    if text.lower().startswith(':dballon'):
        message.is_blocked = True
        dodgeball = True
        ext.send_to_client('{in:Whisper}{i:-1}{s:"Dodgeball Bot is On"}{i:0}{i:34}{i:0}{i:-1}')

    elif text.lower().startswith(':dballoff'):
        message.is_blocked = True
        dodgeball = False
        ext.send_to_client('{in:Whisper}{i:-1}{s:"Dodgeball Bot is Off"}{i:0}{i:34}{i:0}{i:-1}')

    elif text.lower().startswith(':numreset'):
        allowed_values = []    
        message.is_blocked = True
        ext.send_to_client('{in:Whisper}{i:-1}{s:"Dice numbers are resetted"}{i:0}{i:34}{i:0}{i:-1}')

    elif text.lower().startswith(':dballcmd'):
        message.is_blocked = True
        ext.send_to_client('{in:Whisper}{i:-1}{s:"":dballon" turns the bot on\n":dballoff" turns the bot off\nPress "alt" and move the furni where you wanna walk\nTo set dice number type :num "number" to add, you can add multiple numbers (1-6)\n:numreset to reset all numbers."}{i:0}{i:34}{i:0}{i:-1}')

ext.intercept(Direction.TO_CLIENT, dice, 'DiceValue')
ext.intercept(Direction.TO_SERVER, message, 'Chat')
ext.intercept(Direction.TO_SERVER, coords, 'MoveObject')