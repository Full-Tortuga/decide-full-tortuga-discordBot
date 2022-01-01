import discord
from discord.ext import commands
import requests
import re
from collections import OrderedDict
from requests.api import post
import os
from requests.models import Response
from selenium import webdriver
import base64


URL_BASE = "http://127.0.0.1:8000/"


#bot prefix
bot = commands.Bot(command_prefix='!') 

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="preparado para ayudar"))
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
        !results númerovotación - Muestra los resultados de la votación que elijas.
        !details númerovotación - Muestra los detalles de la votación que elijas.
        !graphs númerovotacion - Devuelve las gráficas de la votación que solicites."""

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

            await context.send("Has elegido ver los resultados de la votación con id " + str(id) + ", cuyo nombre es " + str(name) + ", y su descripción: " + str(desc) + """".
Los resultados de esta votación son:""")
            for i in range(0,len(r)):
                r1 = r[i]
                info1 = r1.split("), ")
                votes1 = info1[2]
                numvotes1 = votes1.split(", ")[1]
                opt1 = info1[0]
                optname1 = opt1.split(", ")[1]
                await context.send("- " + optname1 + ", la cual obtuvo " + numvotes1 + " voto(s) en total.")
            #FIRST OPTION
            # r1 = r[0]
            # info1 = r1.split("), ")
            # votes1 = info1[2]
            # numvotes1 = votes1.split(", ")[1]
            # opt1 = info1[0]
            # optname1 = opt1.split(", ")[1]

            #SECOND OPTION
            # r2 = r[1]
            # info2 = r2.split("), ")
            # votes2 = info2[2]
            # numvotes2 = votes2.split(", ")[1]
            # opt2 = info2[0]
            # optname2 = opt2.split(", ")[1]

        #     response=  "Has elegido ver los resultados de la votación con id " + str(id) + ", cuyo nombre es " + str(name) + ", y su descripción: " + str(desc) + """". 
        #     Las opciones de esta votación eran: 
        #     - """ + optname1 + ", la cual obtuvo " + numvotes1 + """ voto(s) en total.
        #     - """ + optname2 + ", la cual obtuvo " + numvotes2 + " voto(s) en total."

        else:

            await context.send("Esa votación aún no está cerrada, vuelva a intentarlo más tarde.")

    except:
        await context.send("Lo siento, ha habido un error. ¡Vuélvelo a intentar!")



@bot.command(name='graphs')
async def graphs(context, num):
    opengraph = open_graphs_generator_view(num)
    print(opengraph)
    base64_url_list=eval(opengraph[0]['graphs_url'])
    print(base64_url_list)
    b64_images=[]
    await context.send('Ahora mismo te las mando.')
    
    for i in range(0,len(base64_url_list)):
        b64_images.append(base64_url_list[i].split(",")[1])
        path="graph_"+str(num)+"_"+str(i)+".png"
        with open(path,"wb") as f:
            f.write(base64.b64decode(b64_images[i]))
        await context.send(file=discord.File(path))
        os.remove(path)
    # except:
    #     response = "Lo siento, esa votación no está disponible. Vuélvelo a intentar."
    #     await context.send(response)

def open_graphs_generator_view(num):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver=webdriver.Chrome(options=options)
    driver.get(URL_BASE+ 'visualizer/' + str(num))  #VISUALIZER_VIEW will be taken from setting in production
    return requests.get(URL_BASE + "visualizer/" + str(num) + "/graphs").json()
     



bot.run('OTE3ODkzNjg1MjM5MjM4NzQ3.Ya_VHA.ssIhbCWQMJ1eHqaEW33ztOp7Eyw')