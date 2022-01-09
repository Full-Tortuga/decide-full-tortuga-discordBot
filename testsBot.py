import unittest
from discord import message
from discord.ext import commands
import requests
import json

URL_BASE = "http://127.0.0.1:8000/"


class testsBot(unittest.TestCase):


    def test_isOn(self):
        try:
            r = requests.get(URL_BASE)
            self.assertEqual(r.status_code, 404)
        except:
            test_value = True
            message = "El servidor está apagado."
            self.assertFalse(test_value, message)

    def test_details(self):
        urlvoting = "voting/?id=" 
        url = URL_BASE + urlvoting + "1"
        r = requests.get(url)

        self.assertEqual(r.status_code, 200)
    
    def test_details_multiple(self):
        urlvoting = "voting/multipleVoting/?id="
        url = URL_BASE + urlvoting + "2"
        r= requests.get(url)

        data= r.json()[0]
        name = data['name']
        self.assertEqual(name, "prueba 2 multiple")

    def test_details_score(self):
        urlvoting = "voting/scoreVoting/?id="
        url = URL_BASE + urlvoting + "1"
        r= requests.get(url)

        data= r.json()[0]
        desc = data['desc']
        self.assertEqual(desc, "prueba")

    def test_details_wrong(self):
        urlvoting = "voting/?id=" 
        url = URL_BASE + urlvoting + "wrong"
        r = requests.get(url)

        self.assertEqual(r.status_code, 400)

    def test_graphs(self):
        urlvisualize = "visualizer/" 
        urlgraph = "graphs"
        url = URL_BASE + urlvisualize + "1/" + urlgraph
        r = requests.get(url)

        self.assertEqual(r.status_code, 200)

    def test_graphs_wrong(self):
        urlvisualize = "visualizer/" 
        urlgraph = "graphs"
        url = URL_BASE + urlvisualize + "wrong/" + urlgraph
        r = requests.get(url)

        self.assertEqual(r.status_code, 404)

if __name__ == '__main__':
    unittest.main()