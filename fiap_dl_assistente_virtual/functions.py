import os
import pyttsx3
import pyaudio
import speech_recognition as sr


assistente = pyttsx3.init()
recon = sr.Recognizer()
inpvoz = ""


def retorno(frase):
    assistente.say(frase)
    assistente.setProperty("voice", b"brasil")
    assistente.setProperty("rate", 210)
    assistente.setProperty("volume", 1)
    assistente.runAndWait()


def ouvir(source):
    recon.adjust_for_ambient_noise(source)
    audio = recon.listen(source)
    inpvoz = recon.recognize_google(audio, language="pt-BR")
    return inpvoz


def continuar(source):
    retorno(
        "Posso ajudar com algo mais? Responda sim para continuar e não para finalizar!"
    )
    continuar = ouvir(source)
    print(f"Você disse {continuar}")
    return continuar
