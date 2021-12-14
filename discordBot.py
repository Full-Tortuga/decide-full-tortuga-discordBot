import discord
from discord.ext import commands
import requests
import re
from collections import OrderedDict
from requests.api import post
import os

URL_BASE = "http://127.0.0.1:8000/"


#bot prefix
bot = commands.Bot(command_prefix='!') 

@bot.event
async def on_ready():
    print("Hola soy votitos. Estoy listo para funcionar.")

@bot.command(name='how')
async def how(context):

    #Explain the use of the bot

    response = """Este bot se utiliza para devolver los resultados de las distintas votaciones que se realizan en la web de Decide. 
    Si no estás registrado y quieres hacerlo, utiliza el comando !register. 
    Si ya estás registrado, utiliza !help para ver los distintos comandos disponibles. Gracias."""
    await context.send(response)


@bot.command(name='helpcommands')
async def helpcommands(context):

    #Send the different commands the bot has

    response= """Los comandos disponibles a usar son los siguientes:
        !register - Para registrarte en caso de no haberlo hecho.
        !how - Explica el funcionamiento del bot.
        !results - Muestra los resultados de la votación que elijas.
        !details - Muestra los detalles de la votación que elijas."""

    await context.send(response)

@bot.command(name='details')
async def details(context, num):

    #Shows the details of the voting the user asks for

    urlvoting = "voting/?id=" 
    url = URL_BASE + urlvoting + num
    req = requests.get(url)

    try:
        data = req.json()[0]
        id = data['id']
        name = data['name']
        desc = data['desc']
        postproc = data['postproc']
        response= "Has elegido ver la votación con id " + str(id) + ", cuyo nombre es " + str(name) + ", y su descripción: " + str(desc) + "." 
    
    except:
        response = "Lo siento, ha habido un error. ¡Vuélvelo a intentar!"

    await context.send(response)
        

@bot.command(name='results')
async def results(context, num):

    #Show the results of the voting the user asks for

    url = URL_BASE + "voting/?id="  + num
    req = requests.get(url)

    try:

        data = req.json()[0]
        if(data['end_date'] != None):
            id = data['id']
            name = data['name']
            desc = data['desc']
            postproc = data['postproc']
            r = re.findall("t\(\[(.*?)\]\)", postproc)

            #FIRST OPTION
            r1 = r[0]
            info1 = r1.split("), ")
            votes1 = info1[2]
            numvotes1 = votes1.split(", ")[1]
            opt1 = info1[0]
            optname1 = opt1.split(", ")[1]

            #SECOND OPTION
            r2 = r[1]
            info2 = r2.split("), ")
            votes2 = info2[2]
            numvotes2 = votes2.split(", ")[1]
            opt2 = info2[0]
            optname2 = opt2.split(", ")[1]

            response= "Has elegido ver los resultados de la votación con id " + str(id) + ", cuyo nombre es " + str(name) + ", y su descripción: " + str(desc) + """". 
            Las opciones de esta votación eran: 
            - """ + optname1 + ", la cual obtuvo " + numvotes1 + """ voto(s) en total.
            - """ + optname2 + ", la cual obtuvo " + numvotes2 + " voto(s) en total."

        else:

            response="Esa votación aún no está cerrada, vuelva a intentarlo más tarde."

    except:
        response = "Lo siento, ha habido un error. ¡Vuélvelo a intentar!"

    await context.send(response)


bot.run('OTE3ODkzNjg1MjM5MjM4NzQ3.Ya_VHA.jGZPhpz5aHeZzv0bfRNfmqLHVUw')