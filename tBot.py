# tBot. A small, fully operational IRC bot.
### Cajun Slang - Used in front of any name, “T” means petit (little); T-Sam, etc.

# Tegan Lamoureux
# tegan@teux.me

# FYI - this is my first (minorly complex) python program and this code is
# probably awful, inefficient, and ugly. It's also a work in progress, hence
# the comment jungle. But I'm learning, and that's the point! :)
#myfirstlovewasc++ #comments_in_python_are_just_long_hashtags

#TODO:
# Make sure pong is replying correctly (parse out message?) raw data looks like:
#     "b'PING :hobana.freenode.net\r\n'"
# Add private message feature. Spawn a new thread/process?
# Also parse incoming text string so anytime bot name is mentioned, she replies.
##### ^^Scratch that, just make a parse function. Will be useful.
# Fix user/nick globals? still an issue?
# Convert to interactive, and allow user to type manually through bot from
#     server side. Switch to threading to handle user input while bot still
#     handles everything else.
# Fix verbose output, unicode_escape, and clean up so that if sent to log,
#     doesn't look so awful.
# Fix talking to herself about pie (have her ignore herself when parsing).

import socket
import ssl
import sys
import pprint
import time


# Bot Name Options
bot_nick = "tBot_says_rawr"
bot_name = "tBot_real_name"
bot_user = "tBot_user_name"

# Network Options
is_verbose = True                 #will print buffer info if true, if not, will run silently
use_ssl    = True                 #set to true to connevt via SSL
serv_name   = "chat.freenode.net"  #server hostname
chan_name   = "#tbottest"          #channel to join
chan_key    = ""                   #password (if none, leave empty)

# Flags
tbot_go = True # main loop flag

# Message function! Will send a message or action to our channel.
def send_message(messageText, is_action):
    # Construct IRC message/action command, and concatenate message with it.
    if is_action:
        message = "PRIVMSG " + chan_name + " :" + "\x01" + "ACTION " + str(messageText) + "\x01" + "\r\n"
    else:
        message = "PRIVMSG " + chan_name + " :" + str(messageText) + "\r\n"

    irc_server.sendall(bytes(message, 'UTF-8'))
    return

# Will grab (and clear!!) and print the socket buffer. Mainly for debugging.
def print_buffer():
    print(bytes(str(irc_server.recv(4096)), "UTF_8").decode("unicode_escape"))
    return

if use_ssl:
    servPort = 6697
    context = ssl.create_default_context()
    irc_server = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=serv_name)
    irc_server.connect((serv_name, servPort))
    #cert = irc_server.getpeercert() #TODO: perform basic cert verification
else:
    servPort = 6667
    irc_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc_server.connect((serv_name, servPort))

# Sleep for a bit because some servers don't like fast commands (or my sockets are slow?)
time.sleep(.01)
if is_verbose: print_buffer()

#set username, nick, join channel
irc_server.sendall(("USER " + bot_user + " 0 * :" + bot_name + "\r\n").encode("utf_8"))
time.sleep(.01)
if is_verbose: print_buffer()

irc_server.sendall(("NICK " + bot_nick + "\r\n").encode('utf_8'))
time.sleep(.01)
if is_verbose: print_buffer()

# TODO: grab nick from server and replace bot_nick, in case it's already in use
# and the server gives us an alt nick. this way response will still work.

irc_server.sendall(("JOIN " + chan_name + chan_key + "\r\n").encode('utf_8'))
time.sleep(.01)
if is_verbose: print_buffer()

while tbot_go:
    #grab buffer from socket
    readBuffer = irc_server.recv(4096)

    #n = input("[tleauxBot]: ") #switch this to threading

    # Parser Section
    # check buffer and act on text. probs an easier way to do this but it works for now
    # TODO: switch to a matrix of checks and responses, so don't have to hard-code them
    if ' PRIVMSG ' in str(readBuffer): #to stop her from flooding replies when the server says her name
        if bot_nick in str(readBuffer):
            if 'go away' in str(readBuffer):
                send_message("aww ok. bye you guys. :<", False)
                tbot_go = False

            elif 'help' in str(readBuffer):
                send_message("What's the point? All anyone ever does is \x1Flie\x1F. :(", False)
                time.sleep(3)
                send_message("*mumble mumble*", True)
                time.sleep(1.5)
                send_message("stupid cake", False)

            elif 'source' in str(readBuffer):
                send_message("My source can be found at https://github.com/tegan-lamoureux/tBot ^-^", False)

            else:
                tempB = str(readBuffer).partition(':')
                tempUName = tempB[2].split('!')
                send_message("Hi " + tempUName[0] + "! Ask me for \'help\' or \'source\'.\r\n", False)

    if 'PING' in str(readBuffer):   #TODO: fix so replies with server string? or fine as-is?
        irc_server.sendall(b"PONG\r\n")
        if is_verbose: print("PONG")

    if is_verbose: print (str(readBuffer))

irc_server.sendall(b"QUIT\r\n")
irc_server.close()
