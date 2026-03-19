import socket
import threading
import wave
import json
import time
import re
import sys

import keyboard
import ollama
import pyaudio
import pytchat
import winsound
from emoji import demojize

from utils.TTS import *
from utils.promptMaker import *
from utils.subtitle import *
from utils.translate import *
from utils.twitch_config import *
from utils import diagnostico  # <--- NUEVO: módulo de diagnóstico

# ESTE ES EL LINK DE DRIVE PARA EL ARCHIVO MODEL.PT QUE PESA 54 MB:
# https://drive.google.com/drive/folders/1uQ8XTQyBSxrwD7qRdGUeUIxTDaBD4Sfe?hl=es

# ANTES DE USAR ESTA VERSIÓN, YA QUE JODÍ EL ENTORNO VIRTUAL, USA ESTE COMANDO LA PRIMERA VEZ QUE VAYAS
# A USAR EL POWER SHELL: .\.venv\Scripts\Activate.ps1
# CON ESE COMANDO SI TE VA A ADMITIR ESCRIBIR PYTHON RUN.PY
# id de stream yt: a0ciEBctkAY
# id de stream twitch:

# Configurar consola para UTF-8
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

# ============================================
# CONFIGURACIÓN GLOBAL
# ============================================
conversation = []
history = {"history": conversation}

mode = 0
total_characters = 0
chat = ""
chat_now = ""
chat_prev = ""
is_Speaking = False
owner_name = "Usuario"
blacklist = ["Nightbot", "streamelements"]

# Modelo de Ollama
OLLAMA_MODEL = "gemma3:4b"

# Cable virtual
CABLE_DEVICE_NAME = "CABLE Input"

# Idioma actual
current_language = "es"

# ============================================
# FUNCIÓN: Grabar audio desde micrófono
# ============================================
def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "input.wav"

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    print("🎤 Grabando... (mantén M)")
    while keyboard.is_pressed('M'):
        data = stream.read(CHUNK)
        frames.append(data)

    print("⏹️ Grabación detenida.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    transcribe_audio("input.wav")

# ============================================
# FUNCIÓN: Transcribir audio a texto
# ============================================
def transcribe_audio(file):
    global chat_now, current_language

    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()

        with sr.AudioFile(file) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.record(source)

        try:
            chat_now = recognizer.recognize_google(audio)
            print(f"🗣️ Tú: {chat_now}")
        except sr.UnknownValueError:
            print("❌ No se pudo entender el audio")
            return
        except sr.RequestError:
            print("❌ Error con el servicio de reconocimiento")
            return

        from utils.translate import detect_google
        current_language = detect_google(chat_now)
        print(f"🌐 Idioma detectado: {current_language}")

    except Exception as e:
        print(f"❌ Error transcribiendo audio: {e}")
        return

    result = owner_name + " dijo: " + chat_now
    conversation.append({'role': 'user', 'content': result})
    ollama_answer()

# ============================================
# FUNCIÓN: Obtener respuesta de Ollama
# ============================================
def ollama_answer():
    global total_characters, conversation

    total_characters = sum(len(d['content']) for d in conversation)
    while total_characters > 4000:
        try:
            conversation.pop(2)
            total_characters = sum(len(d['content']) for d in conversation)
        except Exception as e:
            print(f"Error limpiando historial: {e}")

    with open("conversation.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

    prompt = getPrompt(current_language)

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=prompt,
            options={
                "num_predict": 150,
                "temperature": 0.8,
                "top_p": 0.9
            }
        )
        message = response['message']['content']
    except Exception as e:
        print(f"❌ Error llamando a Ollama: {e}")
        message = "Lo siento, tuve un problema. ¿Puedes repetir la pregunta?"

    conversation.append({'role': 'assistant', 'content': message})
    translate_text(message)

# ============================================
# FUNCIÓN: Generar voz y enviar a cable virtual
# ============================================
def translate_text(text):
    global is_Speaking, chat_now, current_language

    print(f"\n🤖 Mombii ({current_language}): {text}")

    generate_subtitle(chat_now, text)

    is_Speaking = True

    try:
        from utils.TTS import hablar_en_idioma
        hablar_en_idioma(text, current_language, CABLE_DEVICE_NAME)
    except Exception as e:
        print(f"❌ Error generando voz: {e}")
        winsound.Beep(500, 500)

    is_Speaking = False

    time.sleep(1)
    for archivo in ["output.txt", "chat.txt"]:
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                f.truncate(0)
        except:
            pass

# ============================================
# FUNCIÓN: Capturar chat de YouTube
# ============================================
def yt_livechat(video_id):
    global chat, current_language
    live = pytchat.create(video_id=video_id)
    while live.is_alive():
        try:
            for c in live.get().sync_items():
                if c.author.name in blacklist:
                    continue
                if not c.message.startswith("!"):
                    chat_raw = re.sub(r':[^\s]+:', '', c.message)
                    chat_raw = chat_raw.replace('#', '')

                    from utils.translate import detect_google
                    idioma_msg = detect_google(chat_raw)
                    current_language = idioma_msg
                    print(f"🌐 Idioma del chat: {idioma_msg}")

                    chat = c.author.name + ' dijo: ' + chat_raw
                    print(chat)
                time.sleep(1)
        except Exception as e:
            print(f"Error en chat de YT: {e}")

# ============================================
# FUNCIÓN: Capturar chat de Twitch
# ============================================
def twitch_livechat():
    global chat, current_language
    sock = socket.socket()
    sock.connect((server, port))

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    time.sleep(1)

    regex = r":(\w+)!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :(.+)"

    while True:
        try:
            resp = sock.recv(2048).decode('utf-8', errors='ignore')
            print(f"[DEBUG RAW] {repr(resp)}")

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
                continue

            if 'PRIVMSG' in resp:
                resp = demojize(resp)
                match = re.match(regex, resp)

                if match:
                    username = match.group(1)
                    message = match.group(2)

                    if username in blacklist:
                        continue

                    from utils.translate import detect_google
                    idioma_msg = detect_google(message)
                    current_language = idioma_msg
                    print(f"🌐 Idioma del chat: {idioma_msg}")

                    chat = username + ' dijo: ' + message
                    print(chat)
                else:
                    print(f"⚠️ Línea PRIVMSG no coincide: {resp.strip()}")
        except Exception as e:
            print(f"Error en chat de Twitch: {e}")
            time.sleep(1)

# ============================================
# FUNCIÓN: Procesar diagnóstico (para modo 4)
# ============================================
def procesar_diagnostico(mensaje_original, idioma):
    """
    Ejecuta el diagnóstico y genera una respuesta con la IA.
    """
    global chat_now, current_language
    print("🔧 Ejecutando diagnóstico...")
    try:
        # 1. Obtener datos de diagnóstico
        datos = diagnostico.ejecutar_diagnostico()
        print("✅ Diagnóstico completado.")

        # 2. Preparar prompt especial
        prompt_diagnostico = f"""
Eres Mombii, una asistente técnica experta.
El usuario ha solicitado un diagnóstico de su computadora.
Estos son los datos recopilados de las herramientas:

{datos}

Basándote en esta información, interpreta el estado del hardware.
Si hay problemas, indica si son graves o leves, y qué podría estar causándolos.
No des instrucciones para reparar automáticamente, solo diagnóstico y recomendaciones generales.
Responde en el idioma '{idioma}' de forma clara y profesional.
"""
        # 3. Llamar a Ollama directamente
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt_diagnostico}],
            options={"num_predict": 300, "temperature": 0.5}
        )
        respuesta_ia = response['message']['content']

        # 4. Mostrar y vocalizar
        chat_now = mensaje_original  # Para subtítulos
        current_language = idioma
        translate_text(respuesta_ia)

    except Exception as e:
        print(f"❌ Error en diagnóstico: {e}")
        chat_now = mensaje_original
        current_language = idioma
        translate_text("Lo siento, hubo un problema al ejecutar el diagnóstico.")

# ============================================
# FUNCIÓN: Chat por texto (modo 4) con diagnóstico
# ============================================
def chat_texto():
    global chat, current_language, is_Speaking
    print("\n" + "="*50)
    print("   MODO CHAT POR TEXTO")
    print("   Escribe tu mensaje y presiona ENTER")
    print("   Comandos especiales: 'diagnostica', '!diagnostico' para diagnóstico")
    print("   Escribe 'salir' para volver al menú")
    print("="*50 + "\n")

    while True:
        try:
            mensaje = input("Tú: ").strip()

            if mensaje.lower() == 'salir':
                print("\n👋 Saliendo del modo chat...")
                break

            if mensaje:
                from utils.translate import detect_google
                idioma = detect_google(mensaje)
                print(f"🌐 Idioma detectado: {idioma}")

                # Detectar si es un comando de diagnóstico
                if any(palabra in mensaje.lower() for palabra in ['diagnostica', '!diagnostico', 'diagnóstico', 'analiza mi pc']):
                    # Ejecutar diagnóstico directamente (sin pasar por el hilo preparation)
                    procesar_diagnostico(mensaje, idioma)
                else:
                    # Flujo normal: asignar a chat y esperar que el hilo lo procese
                    chat = "Usuario dijo: " + mensaje
                    current_language = idioma

                    # Esperar a que Mombii comience a hablar
                    timeout = 10
                    while not is_Speaking and timeout > 0:
                        time.sleep(0.1)
                        timeout -= 0.1

                    # Esperar a que termine de hablar
                    while is_Speaking:
                        time.sleep(0.1)

                    time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n👋 Saliendo del modo chat...")
            break
        except Exception as e:
            print(f"❌ Error en chat de texto: {e}")
            time.sleep(1)

# ============================================
# FUNCIÓN: Preparación (hilo principal)
# ============================================
def preparation():
    global conversation, chat_now, chat, chat_prev
    while True:
        chat_now = chat
        if not is_Speaking and chat_now and chat_now != chat_prev:
            conversation.append({'role': 'user', 'content': chat_now})
            chat_prev = chat_now
            ollama_answer()
        time.sleep(1)

# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    try:
        print("=" * 50)
        print("   ASISTENTE MOMBII - MODO MULTILINGÜE")
        print("   Responde en el mismo idioma en que le hablen")
        print("=" * 50)
        print("Modos disponibles:")
        print("1 - Micrófono (habla con MOMBII)")
        print("2 - YouTube Live")
        print("3 - Twitch Live")
        print("4 - Chat por texto (con diagnóstico)")

        mode = input("Selecciona modo (1, 2, 3 o 4): ")

        if mode == "1":
            print("\n🎤 Modo MICRÓFONO")
            print("Mantén presionada la tecla M para hablar")
            print("Suelta la tecla para que MOMBII procese tu mensaje\n")
            while True:
                if keyboard.is_pressed('M'):
                    record_audio()

        elif mode == "2":
            live_id = input("ID del live de YouTube: ")
            t = threading.Thread(target=preparation)
            t.start()
            yt_livechat(live_id)

        elif mode == "3":
            print("Usando configuración de Twitch...")
            t = threading.Thread(target=preparation)
            t.start()
            twitch_livechat()

        elif mode == "4":
            t = threading.Thread(target=preparation)
            t.start()
            chat_texto()

    except KeyboardInterrupt:
        print("\n👋 Programa terminado.")
        try:
            t.join()
        except:
            pass
