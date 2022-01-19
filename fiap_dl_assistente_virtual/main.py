import json
import requests
import webbrowser
import speech_recognition as sr

from bs4 import BeautifulSoup
from urllib.request import urlopen
from functions import retorno
from functions import ouvir
from functions import continuar


recon = sr.Recognizer()


def main():
    with sr.Microphone() as source:
        recon.adjust_for_ambient_noise(source)
        retorno(
            "Olá! Sou a assistente virtual e vou te auxiliar com a pesquisa de serviços. Qual serviço você deseja pesquisar?"
        )
        print("Por favor, diga o nome do serviço!")

        while True:
            try:
                acao = str(ouvir(source))
                print(f"Você disse: {acao}")

                if " " in acao:
                    acao = acao.replace(" ", "%20")

                url = f"https://portalunico.estaleiro.serpro.gov.br/api/search/?q={acao.lower()}&ordenacao=-relevancia&categoriasFiltro=&orgaosFiltro=&tipo=Servico%7CTema&pagina=1&tam_pagina=30"

                link = f"https://www.gov.br/pt-br/search?SearchableText={acao.lower()}"

                chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

                webbrowser.get(chrome_path).open(link)

                response = urlopen(url)

                data_json = json.loads(response.read())

                items = data_json.get("items")

                retorno("Esses são os 10 principais resultados de pesquisa: ")

                for k, v in enumerate(items[0:10]):
                    retorno(f'{k+1} - {v["title"]}')

                retorno("Diga o número da sua opção: ")

                try:
                    escolha = ouvir(source)
                except:
                    retorno("Não entendi! Por favor, repita sua opção.")
                    escolha = ouvir(source)

                while int(escolha) not in range(1, 11):
                    retorno("Por favor, escolha a sua opção entre 1 e 10!")
                    try:
                        escolha = ouvir(source)
                    except:
                        retorno("Não entendi! Por favor, repita sua opção.")
                        escolha = ouvir(source)

                servico_escolhido = (
                    f'https://www.gov.br{items[int(escolha)-1]["contentUrl"]}'
                )

                chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

                webbrowser.get(chrome_path).open(servico_escolhido)

                retorno(
                    f'Certo! Aqui você vai encontrar as instruções sobre {items[int(escolha)-1]["title"]}'
                )

                retorno(f"Deseja que eu leia a descrição?")

                ler = ouvir(source)

                if str(ler.lower()) in ("sim"):
                    html = requests.get(servico_escolhido).content

                    soup = BeautifulSoup(html, "html.parser")

                    titulo = soup.find(
                        "a", class_="titulo toggle-link", id="dados_basicos"
                    ).getText()
                    conteudo = soup.find("div", class_="conteudo").getText()

                    retorno(conteudo)

                cont = continuar(source)

                if "não" in cont:
                    retorno(
                        "Gostaria de saber se consegui te ajudar. Por favor, responda 1 para sim e 2 para não."
                    )

                    try:
                        pesquisa = ouvir(source)
                    except:
                        retorno("Não entendi! Por favor, repita sua opção.")
                        pesquisa = ouvir(source)

                    while int(pesquisa) not in (1, 2):
                        retorno("Por favor, escolha 1 para sim ou 2 para não.")
                        pesquisa = ouvir(source)
                    break
                else:
                    retorno("Qual serviço você deseja pesquisar?")
            except:
                retorno(
                    "Desculpe, não entendi. Ainda estou aprendendo. Vamos começar novamente!"
                )
                retorno("Qual serviço você deseja pesquisar?")


if __name__ == "__main__":
    main()
