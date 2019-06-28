import discord
import container
import socket

host = socket.gethostname()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.startswith("!code "):
            args = message.content.strip().replace("!code C\n", "!code C ").replace("!code c\n", "!code c ").split(" ", 2)
            print(args)
            r = container.run_code(args[1], args[2])
            if r.ccr == "":
                await message.channel.send("Code Result: ```" + r.cr + "```\n`" + r.uuid + "|" + host + "|NOCHROOT`")
            else:
                await message.channel.send("CC Result: ```" + r.ccr + "```\nCode Result: ```" + r.cr + "```\n`" + r.uuid + "|" + host +"|NOCHROOT`")

client = MyClient()
client.run('NTkxNzI0MTczNjkzMjg4NDcw.XRWE_g.SHe_YwT_L61mdgyELjGcQUB9p5c')