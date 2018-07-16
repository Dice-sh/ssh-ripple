from pexpect import pxssh

class Bot:

    # initialize new client
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.ssh()

    # secure shell into client
    def ssh(self):
        try:
            bot = pxssh.pxssh()
            bot.login(self.host, self.user, self.password)
            return bot
        except Exception as e:
            print('[-] Connection failure.')
            print(e)

    # send commands to client
    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

# send commands to all bots in botnet
def command_bots(command):
    for bot in  botnet:
        attack = bot.send_command(command)
        print('[-] Output from' + bot.host)
        print(attack)

# list of bots in botnet
botnet = []

# add a new bot to the botnet
def add_bot(host, user, password):
    new_bot = Bot(host, user, password)
    botnet.append(new_bot)

add_bot('', '', '')

# commands can be typed here
command_bots('ls')


