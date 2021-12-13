import discord
from discord.ext import commands
import requests
import json
import asyncio
import os
from collections import OrderedDict
import re

from requests.api import post

URL_BASE = "http://127.0.0.1:8000/"

bot = commands.Bot(command_prefix='!') #bot prefix


@bot.command(name='how')
async def how(context):
    response = """Este bot se utiliza para devolver los resultados de las distintas votaciones que se realizan en la web de Decide. 
    Si no estás registrado y quieres hacerlo, utiliza el comando !register. 
    Si ya estás registrado, utiliza !help para ver los distintos comandos disponibles. Gracias."""
    await context.send(response)


@bot.command(name='helpcommands')
async def helpcommands(context):
    response= """Los comandos disponibles a usar son los siguientes:
        !register - Para registrarte en caso de no haberlo hecho.
        !how - Explica el funcionamiento del bot.
        !results - Muestra los resultados de la votación que elijas.
        !details - Muestra los detalles de la votación que elijas."""
    await context.send(response)

@bot.command(name='details')
async def details(context, num):
    urlvoting = "gateway/voting/?id=" 
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
    url = URL_BASE + "gateway/voting/?id="  + num
    req = requests.get(url)

    try:
        data = req.json()[0]
        if(data['end_date'] != None):
            id = data['id']
            name = data['name']
            desc = data['desc']
            response= "Has elegido ver los resultados de la votación con id " + str(id) + ", cuyo nombre es " + str(name) + ", y su descripción: " + str(desc) + ". " 
        else:
            response="Esa votación aún no está cerrada, vuelva a intentarlo más tarde."
    except:
        response = "Lo siento, ha habido un error. ¡Vuélvelo a intentar!"
    await context.send(response)


bot.run('OTE3ODkzNjg1MjM5MjM4NzQ3.Ya_VHA.PSxgyoAQrJEODXQaAwMhnYZDjwI')