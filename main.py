import discord
import random
import urllib.request, json
from datetime import date, datetime
from datetime import time as dtime
import datetime
import time
import demjson
from babel.dates import format_date, format_datetime, format_time
import embeds

TOKEN = open(".token", "r").read()
client = discord.Client()

public_club_schedule_url = "https://spreadsheets.google.com/feeds/list/1R0EYEPVmGvd_fwmIoDA8C59D6pJJWcuJLz_t3cAJutA/od6/public/basic?alt=json"
public_exec_schedule_url = "https://spreadsheets.google.com/feeds/list/10smcBDbhRHxdlDIWfdKL44PWbuJ7_44Tzb0carSNk6g/od6/public/basic?alt=json"


@client.event
async def on_message(message):
    member = message.author
    if member == client.user:
        return
    if len(message.content.split(" ")) < 2:
        command = message.content
    else:
        command, param = message.content.split(" ")[0:1]
    command = command[1:]
    if command == "help":
        embed = embeds.help
        await message.channel.send(embed=embed)
    elif command == 'meeting':
        data = get_data(public_club_schedule_url)
        next_meeting = None
        for entry in data['entry']:
            m, d, y = list(map(int, entry['title']['$t'].split("/")))
            print(dirtyjsonload(entry['content']['$t'])[
                      "meetingtype"])
            if datetime.date(y, m, d) > datetime.date.today() and dirtyjsonload(entry['content']['$t'])[
                "meetingtype"] == "Normal Meeting":
                next_meeting = entry
                break
        next_meeting_date, meeting_type, meeting_times, meeting_location, meeting_notes = parse_content(
            next_meeting)
        embed = generate_meeting_info_embed(next_meeting_date, meeting_type, meeting_times, meeting_location,
                                            meeting_notes)
        await message.channel.send(embed=embed)
    elif command == 'event':
        data = get_data(public_club_schedule_url)
        next_meeting = None
        for entry in data['entry']:
            m, d, y = list(map(int, entry['title']['$t'].split("/")))
            if datetime.date(y, m, d) > datetime.date.today() and dirtyjsonload(entry['content']['$t'])[
                "meetingtype"] != "Normal Meeting":
                next_meeting = entry
                break
        next_meeting_date, meeting_type, meeting_times, meeting_location, meeting_notes = parse_content(
            next_meeting)
        embed = generate_meeting_info_embed(next_meeting_date, meeting_type, meeting_times, meeting_location,
                                            meeting_notes)
        await message.channel.send(embed=embed)
    elif command == 'next':
        data = get_data(public_club_schedule_url)
        next_meeting = None
        for entry in data['entry']:
            m, d, y = list(map(int, entry['title']['$t'].split("/")))
            if datetime.date(y, m, d) > datetime.date.today():
                next_meeting = entry
                break
        next_meeting_date, meeting_type, meeting_times, meeting_location, meeting_notes = parse_content(
            next_meeting)
        embed = generate_meeting_info_embed(next_meeting_date, meeting_type, meeting_times, meeting_location,
                                            meeting_notes)
        await message.channel.send(embed=embed)
    elif command == 'exec':
        isExec = False
        for role in member.roles:
            if role.name == "Executive":
                isExec = True
                break
        if not isExec:
            return
        data = get_data(public_exec_schedule_url)
        next_meeting = get_next_meeting(data, meeting_type="Executive")
        next_meeting_date, meeting_type, meeting_times, meeting_location, meeting_notes = parse_content(
            next_meeting)
        embed = generate_meeting_info_embed(next_meeting_date, meeting_type, meeting_times, meeting_location,
                                            meeting_notes)
        await message.channel.send(embed=embed)
    elif command == 'rules':
        await message.channel.send(embed=embeds.rules)
    elif command == 'welcome':
        await member.send(embed=embeds.welcome)
        await member.send(embed=embeds.rules)
        await member.send(embed=embeds.help)
        await message.channel.send("A DM has been sent to you!")


def get_next_meeting(data, meeting_type="none"):
    next_meeting = None
    for entry in data['entry']:
        m, d, y = list(map(int, entry['title']['$t'].split("/")))
        print(dirtyjsonload(entry['content']['$t'])["meetingtype"] == meeting_type)
        if datetime.date(y, m, d) > datetime.date.today() and (dirtyjsonload(entry['content']['$t'])[
                                                                   "meetingtype"] == meeting_type or meeting_type is "none"):
            next_meeting = entry
            break
    return next_meeting


def get_data(spreadsheet_url):
    with urllib.request.urlopen(spreadsheet_url) as url:
        data = json.loads(url.read().decode())["feed"]
        return data


def parse_content(entry):
    m, d, y = list(map(int, entry['title']['$t'].split("/")))
    content = dirtyjsonload(entry['content']['$t'])
    meeting_type = content["meetingtype"]
    meeting_times = content["times"] if "times" in content else False
    meeting_location = content["location"] if "location" in content else False
    meeting_notes = content["notes"] if "notes" in content else False
    next_meeting_date = datetime.datetime(y, m, d)
    return next_meeting_date, meeting_type, meeting_times, meeting_location, meeting_notes


def generate_meeting_info_embed(next_meeting_date, meeting_type, meeting_times, meeting_location, meeting_notes):
    embed = discord.Embed(title=format_date(next_meeting_date, locale='en'),
                          description=next_meeting_date.strftime('%A'),
                          color=0xc69249)
    embed.set_thumbnail(
        url="https://raw.githubusercontent.com/VikingsDev/VikingsDev.github.io/master/images/vikingsdev-icon.png")
    embed.add_field(name=meeting_type,
                    value=meeting_location if meeting_location is not False else "No meeting location.",
                    inline=True)
    if meeting_times is not False:
        if meeting_notes is False:
            embed.add_field(name="Meeting Time", value=meeting_times,
                            inline=True)
        else:
            embed.add_field(name=meeting_times, value=meeting_notes,
                            inline=True)

    elif meeting_notes is not False:
        embed.add_field(name=" ", value=meeting_notes,
                        inline=True)
    return embed


@client.event
async def on_member_join(member):
    await member.send(embed=embeds.welcome)
    await member.send(embed=embeds.rules)
    await member.send(embed=embeds.help)


def dirtyjsonload(string):
    splitted_string = string.split(",")
    dict = {}
    for variable in splitted_string:
        key = variable[0:variable.find(":")].strip()
        value = variable[variable.find(":") + 1:].strip()
        dict[key] = value
    return dict


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
