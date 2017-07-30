import discord
import asyncio
import logging
import os
import urllib.request
from urllib.request import Request, urlopen
import shutil

logging.basicConfig(level=logging.INFO)

client = discord.Client();
server = "";

occupied = False;
currentUser = "";

@client.event
async def on_ready():
    print("Client logged in");
    global server;
    server = client.get_server("225224650899193859");
    global currentUser;
    currentUser = server.get_member("181632171470094336");
    await client.change_presence(game=discord.Game(name="Type '>>status'"));
    
@client.event
async def on_message(message):
    global server;
    global occupied;
    global currentUser;

    if message.channel != server.get_channel("340522118968115201"):
        return;
    
    # >>status
    if message.content.lower().startswith(">>status"):
        print("Status command received");
        await client.send_message(message.channel, "*Debug: Status command received*");
        if occupied:
            await client.send_message(message.channel, message.author.mention + " Collab file is currently being used by " + currentUser.nick + ".");
        else:
            await client.send_message(message.channel, message.author.mention + " Collab file is open. Type '>>pull' to join the collab.");
    # >>pull
    elif message.content.lower().startswith(">>pull"):
        print("Pull command received");
        await client.send_message(message.channel, "*Debug: Pull command received*");
        if occupied:
            print("Currently in use by " + currentUser.nick);
            await client.send_message(message.channel, "Currently in use by " + currentUser.nick);
        else:
            print("The current collab user has been set to " + message.author.mention + ".");
            occupied = True;
            currentUser = message.author;
            await client.send_file(message.channel, "SFMEvent/collab.dmx", content="The current collab user has been set to " + message.author.mention + ". Here's the session file:");
            await client.send_message(message.channel, message.author.mention + " You have 4 hours to submit content to the collab. Attach your finished file with the comment '>>push' to submit the file.");
            await client.send_message(message.channel, "Type '>>cancel' if you wish to cancel your submission period so that others can participate.");
            await asyncio.sleep(14400);
            if occupied and message.author == currentUser:
                occupied = False;
                await client.send_message(server.get_channel("341033980176629760"), "The collab is now open. Submission time has expired for " + currentUser.mention + ".");
            
    # >>push
    elif message.content.lower().startswith(">>push"):
        await client.send_message(message.channel, "*Debug: Push command received*");
        print(message.attachments);
        if message.author == currentUser and occupied:
            if len(message.attachments) > 1:
                await client.send_message(message.channel, message.author.mention + " Too many attachments. Only one attachment is allowed. Pls no confuse bot.");
            elif len(message.attachments) == 0:
                await client.send_message(message.channel, message.author.mention + " Please attach a file with a '>>push' comment added onto it.");
            else:
                print(message.attachments[0]);
                await client.send_message(message.channel, "*Debug: Attachment URL is " + message.attachments[0].get("url") + "*");
                # The most basic anti-griefing measure in history of humanity
                if os.path.getsize("SFMEvent/collab.dmx") <= message.attachments[0].get("size") and message.attachments[0].get("filename") == "collab.dmx":
                    # Download submitted file
                    with urllib.request.urlopen(Request(message.attachments[0].get("url"), headers={'User-Agent': 'Mozilla/5.0'})) as response, open("SFMEvent/collab.dmx", 'wb') as out_file:
                        shutil.copyfileobj(response, out_file);
                    await client.send_message(message.channel, message.author.mention + " File accepted. The collab status is now open. Type '>>pull' to join the collab.");
                else:
                    await client.send_message(message.channel, message.author.mention + " File has been caught in the bot's filter and has not been accepted. Message the admins if you believe this is a mistake.");
        else:
            if occupied:
                await client.send_message(message.channel, message.author.mention + " The collab file is currently being used by " + currentUser.nick + ". Please wait for your turn.");
            else:
                await client.send_message(message.channel, message.author.mention + " The collab file is currently open. Type '>>pull' to participate.");
    elif message.content.lower().startswith(">>cancel"):
        await client.send_message(message.channel, "*Debug: Cancel command received*");
        if message.author == currentUser and occupied:
            occupied = False;
            await client.send_message(message.channel, "Participation has been cancelled by " + message.author.mention + " . The collab file is now open. Type '>>pull' to participate.");
        else:
            if occupied:
                await client.send_message(message.channel, message.author.mention + " The collab file is currently being used by " + currentUser.nick + ". Command ignored.");
            else:
                await client.send_message(message.channel, message.author.mention + " The collab file is currently open. Command ignored.");
                    
    # Admin values for debug
    elif discord.utils.get(server.roles, name="Admins") in message.author.roles:
        # >>setocc [true/false]
        if message.content.lower().startswith(">>setocc"):
            if "false" in message.content.lower():
                occupied = False;
                print("Occupied status set to false.");
                await client.send_message(message.channel, "*Debug: Occupied status set to false*");
            elif "true" in message.content.lower():
                occupied = True;
                print("Occupied status set to true.");
                await client.send_message(message.channel, "*Debug: Occupied status set to true*");
            else:
                print("No arguments given for >>setocc. Occupied status unchanged.")
                await client.send_message(message.channel, "*Debug: No arguments given. Occupied status unchanged.*");
        if message.content.lower().startswith(">>forcepush"):
            await client.send_message(message.channel, "*Debug: Force push command received*");
            print(message.attachments);
            if len(message.attachments) > 1:
                await client.send_message(message.channel, message.author.mention + " Too many attachments. Only one attachment is allowed. Pls no confuse bot.");
            elif len(message.attachments) == 0:
                await client.send_message(message.channel, message.author.mention + " Please attach a file with a '>>forcepush' comment added onto it.");
            else:
                print(message.attachments[0]);
                await client.send_message(message.channel, "*Debug: Attachment URL is " + message.attachments[0].get("url") + "*");
                # Download submitted file
                with urllib.request.urlopen(message.attachments[0].get("url")) as response, open("SFMEvent/collab.dmx", 'wb') as out_file:
                    shutil.copyfileobj(response, out_file);
                await client.send_message(message.channel, message.author.mention + " File accepted. The collab status is now open. Type '>>pull' to join the collab.");

client.run("--snip--");
