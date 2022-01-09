import discord
from discord.ext import commands
import requests,re, os, time
from collections import OrderedDict
from requests.api import post
from requests.models import Response
from selenium import webdriver
import base64
from dotenv import load_dotenv
from testsBot import URL_BASE

load_dotenv()
TOKEN_BOT = os.environ['TOKEN']

try:
    requests.get("https://decide-full-tortuga-2.herokuapp.com/")
except:
    URL_BASE = "http://127.0.0.1:8000/"

#bot prefix
bot = commands.Bot(command_prefix='!') 

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="preparado para ayudar"))
    print("Hola soy votitos. Estoy listo para funcionar.")
 


@bot.command(name='hi')
async def how(context):

    #Explain the use of the bot

    response = """¡Hola! Este bot se utiliza para devolver los resultados de las distintas votaciones que se realizan en la web de Decide. 
    Utiliza !helpcommands para ver los distintos comandos disponibles. Gracias."""
    await context.send(response)


@bot.command(name='helpcommands')
async def helpcommands(context):

    #Send the different commands the bot has

    response= """Los comandos disponibles a usar son los siguientes:
        !hi - Explica el funcionamiento del bot.
        !types - Muestra los diferentes tipos de votación disponibles.
        !results tipodevotación númerovotación - Muestra los resultados de la votación que elijas.
        !details tipodevotación númerovotación - Muestra los detalles de la votación que elijas.
        !graphs tipodevotación númerovotacion - Devuelve las gráficas de la votación que solicites."""

    await context.send(response)

@bot.command(name='types')
async def types(context):
    #Explains the different types of votings.
    response = """Los tipos de votaciones que puedes buscar son:
    V - Votación normal.
    MV - Votación múltiple.
    SV - Votación de score.
    BV - Votación binaria.
    """
    
    await context.send(response)

@bot.command(name='details')
async def details(context, typevote, num):

    #Shows the details of the voting the user asks for
    url = translate_type_to_url(typevote, num)
    
    try:
        req = requests.get(url)
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
async def results(context, typevote, num):

    #Show the results of the voting the user asks for

    url = translate_type_to_url(typevote, num)

    try:
        req = requests.get(url)
        data = req.json()[0]
        if(data['end_date'] != None):
            id = data['id']
            name = data['name']
            desc = data['desc']
            postproc = data['postproc']
            if postproc == "[]":
                await context.send("Lo siento, todavía no se ha realizado el recuento de votos de esa votación.")
            else:
                r = re.findall("t\(\[(.*?)\]\)", postproc)

                await context.send("""Has elegido ver los resultados de la votación con id {}, cuyo nombre es {}, y su descripción: {}.
                    Los resultados de esta votación son:""".format(str(id), str(name), str(desc)))
                for i in range(0,len(r)):
                    r1 = r[i]
                    info1 = r1.split("), ")
                    votes1 = info1[2]
                    numvotes1 = votes1.split(", ")[1]
                    opt1 = info1[0]
                    optname1 = opt1.split(", ")[1]
                    await context.send("- " + optname1 + ", la cual obtuvo " + numvotes1 + " voto(s) en total.")

        else:

            await context.send("Esa votación aún no está cerrada, vuelva a intentarlo más tarde.")

    except:
        await context.send("Lo siento, ha habido un error. ¡Vuélvelo a intentar!")



@bot.command(name='graphs')
async def graphs(context, typevote, num):
    try:
        opengraph = open_graphs_generator_view(typevote, num)
        if opengraph is not None:
            base64_url_list=eval(opengraph[0]['graphs_url'])
            b64_images=[]
            await context.send('Ahora mismo te las mando.')
    
            for i in range(0,len(base64_url_list)):
                b64_images.append(base64_url_list[i].split(",")[1])
                path="graph_"+str(num)+"_"+str(i)+".png"
                with open(path,"wb") as f:
                    f.write(base64.b64decode(b64_images[i]))
                await context.send(file=discord.File(path))
                os.remove(path)
        else:
            await context.send("Lo siento, ha habido un error. Vuélvelo a intentar.")
    except:
        response = "Lo siento, esa votación no está disponible. Vuélvelo a intentar."
        await context.send(response)

def open_graphs_generator_view(typevote, num):
    res = ""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver=webdriver.Chrome(options=options)
        driver.get(URL_BASE+ translate_type_to_url_graphs(typevote, num))  #VISUALIZER_VIEW will be taken from setting in production
        driver.quit()
        time.sleep(5)
        res = requests.get(URL_BASE + "visualizer/graphs/?format=json&voting_id=" + str(num)+ "&voting_type="+ typevote).json()
       
    except:
        res = None
    return res 
    
def translate_type_to_url(typevote, num):
    path = "voting/"
    if( typevote == "BV"):
        url = URL_BASE + path + "binaryVoting/?id=" + num
    if( typevote  == "SV"):
        url = URL_BASE + path + "scoreVoting/?id=" + num 
    if (typevote == "MV"):
        url = URL_BASE + path + "multipleVoting/?id=" + num
    if( typevote == "V"):
        url =  URL_BASE + path + "?id=" + num
    return url

def translate_type_to_url_graphs(typevote, num):
    path = "visualizer/"
    if( typevote == "BV"):
        url = path + "binaryVoting/" + num
    if( typevote  == "SV"):
        url =  path + "scoringVoting/" + num 
    if (typevote == "MV"):
        url = path + "multipleVoting/" + num
    if( typevote == "V"):
        url = path + num
    return url

bot.run(TOKEN_BOT)

