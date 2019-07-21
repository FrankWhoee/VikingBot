import discord

rules = discord.Embed(title="Server Rules", locale='en',
                      description="We're not very strict in the server, but you CAN be banned if you violate "
                                          "these rules.",
                      color=0xc69249)
rules.set_thumbnail(
    url="https://raw.githubusercontent.com/VikingsDev/VikingsDev.github.io/master/images/vikingsdev-icon.png")
rules.add_field(name="1. Don't Spam",
                value="Don't post excessive amounts of same or similar messages repeatedly.",
                inline=True)
rules.add_field(name="2. Be Respectful",
                value="Bullying and discrimination is not tolerated.",
                inline=True)
rules.add_field(name="3. Don't post inappropriate content.",
                value="Don't post gorey, sexual, or scary content. This is an educational server.",
                inline=True)
rules.add_field(name="4. Keep content relevant to the channel.",
                value="This rule is just courtesy, it won't get you banned, but keep your discussion relevant "
                      "to the channel you're in.",
                inline=True)

welcome = discord.Embed(title="Welcome to VikingsDev", locale='en',
                        description="We're a server dedicated to the hack club, VikingsDev. To learn more about "
                                    "VikingsDev, go to https://vikingsdev.hackclub.com/",
                        color=0xc69249)
welcome.set_thumbnail(
            url="https://raw.githubusercontent.com/VikingsDev/VikingsDev.github.io/master/images/vikingsdev-icon.png")


help = discord.Embed(title="Help", description="List of commands that you can send.", color=0xc69249)
help.add_field(name="!help", value="You already know what this does.", inline=True)
help.add_field(name="!meeting", value="Shows the next VikingsDev meeting.", inline=True)
help.add_field(name="!next", value="Shows the next VikingsDev gathering. Includes both meetings and events.",
               inline=True)
help.add_field(name="!event", value="Shows the next VikingsDev event.",
               inline=True)
help.add_field(name="!rules", value="Shows the server rules.",
               inline=True)
help.add_field(name="!welcome", value="Sends the welcome message again.",
               inline=True)