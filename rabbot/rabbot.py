from pprint import pprint as pprint
import telepot


with open('token.txt') as tokenfile:
    token = tokenfile.readline().strip()


bot = telepot.Bot(token)


def handle(msg):
    pprint(msg)


bot.message_loop(handle)

# What to do, what to do?
#
# * user says '@Bot open'
