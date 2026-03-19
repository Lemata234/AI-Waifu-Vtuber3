DE ANTEMANO PARA CUALQUIERA QUE LEA ESTO: Soy un vibe coder, apenas este es mi primer proyecto "serio" que no tiene mucho que ver con lo que me dedico, no esperen
que sea capaz de resolver muchas de sus dudas del codigo o inquietudes

-Mata

- son las 15:02 del 18/03/2026 para cuando escribes esto, quiero dejar en claro que este proyecto es originalmente de Ardha27 y en ningún momento pretendo robar su trabajo ni hacerlo pasar por propio. Quiero dejar en claro que, cualquiera que use el código, le deben dar credito a Ardha27 y a Lemata324.

- Nota: ya es 17 de marzo, mombii ya tiene habilitado el chat en la consola

DRIVE DEL ARCHIVO DEL MODEL.PT: https://drive.google.com/drive/folders/1uQ8XTQyBSxrwD7qRdGUeUIxTDaBD4Sfe?usp=sharing

Actualización: esta versión es la que funciona con la integración de Ollama local, tienes ver en run.py que versión de ia es la que se ejecuta
y así decidir cual usar. 

Este es el modelo que ya viene con el contexto e información acerca de la empresa NESKBULL. Para cuando escribes esto, son las 8:25 pm del 7 de marzo del 2025

cambios a realizar: debemos hallar la manera de implementar input por voz y texto de varios idiomas, y necesitamos que la IA (mombii) sea capaz de responder
en el idioma en el que se le habla. 

Actualización: todo eso se logró, solo faltan los subtitulos

actualización: casi jodo el proyecto, entonces debido a que fregué el entorno virtual de python original, debo siempre iniciar con un comando que lo active.

este es el comando para crear el entorno virtual y este para ejecutarlo

creación del entorno

py -3.10 -m venv .venv



activación (siempre ejecuten este antes de correr run.py)

.\ .venv\Scripts\Activate.ps1

el punto va pegado al slash, solo que no puedo ponerlos juntos DX



estos comandos son de limpieza si algo llega a salir mal, obvio necesitan el entorno virtual activo:

# 1. Desinstalar todo (para empezar limpio)
pip freeze | % { pip uninstall -y $_ }

# 2. Instalar el requirements.txt limpio
pip install -r requirements.txt

son las 15:02 del 18/03/2026 para cuando escribes esto, mombii ahora funciona con edge_tts para soportar más idiomas.

estas son las dependencias usadas. si al correr la instrucción de requirements no se descarga alguno, deben descargarlo individualmente.

alkana             0.0.3
annotated-types    0.7.0
anyio              4.12.1
beautifulsoup4     4.14.3
certifi            2026.2.25
cffi               2.0.0
charset-normalizer 3.4.5
colorama           0.4.6
comtypes           1.4.16
deep-translator    1.11.4
emoji              2.15.0
exceptiongroup     1.3.1
filelock           3.25.0
fsspec             2026.2.0
h11                0.16.0
h2                 4.3.0
hpack              4.1.0
httpcore           1.0.9
httpx              0.27.2
hyperframe         6.1.0
idna               3.11
Jinja2             3.1.6
keyboard           0.13.5
MarkupSafe         3.0.3
mecab-python3      1.0.12
mpmath             1.3.0
networkx           3.4.2
numpy              2.2.6
ollama             0.6.1
pandas             2.3.3
pip                26.0.1
plac               1.4.5
PyAudio            0.2.14
pycparser          3.0
pydantic           2.12.5
pydantic_core      2.41.5
pypiwin32          223
pytchat            0.5.5
python-dateutil    2.9.0.post0
pyttsx3            2.99
pytz               2026.1.post1
pywin32            311
requests           2.32.5
setuptools         82.0.0
six                1.17.0
sniffio            1.3.1
sounddevice        0.5.5
soundfile          0.13.1
soupsieve          2.8.3
SpeechRecognition  3.14.6
sympy              1.14.0
torch              2.10.0
tqdm               4.67.3
typing_extensions  4.15.0
typing-inspection  0.4.2
tzdata             2025.3
unidic             1.1.0
urllib3            2.6.3
wasabi             0.10.1
edge-tts

# Support

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/R6R7AH1FA)

## Update

v3.5 Now it also supports for Twitch Streamer

v3.0 Now not only supports Japanese TTS using VoiceVox. But also supports TTS for RU (Russian), EN (English), DE (German), ES (Spanish), FR (French), TT (Tatar), UA (Ukrainian), UZ (Uzbek), XAL (Kalmyk), Indic (Hindi), using Seliro TTS. Change `voicevox_tts` on `run.py` to `seliro_tts`, for detailed information of how to use [Seliro TTS](https://github.com/snakers4/silero-models#text-to-speech)

## AI Waifu Vtuber & Assistant

This project is inspired by shioridotdev and utilizes various technologies such as VoiceVox Engine, DeepL, Whisper OpenAI, Seliro TTS and VtubeStudio to create an AI waifu virtual YouTuber.

![My Remote Image](https://github.com/ardha27/AI-Waifu-Vtuber/blob/master/ss.png?raw=true)

## Demo
 - [Demo](https://www.youtube.com/shorts/_mKVr3ZaM9Q)
 - [Live Test](https://youtu.be/h6UEgJxH1-E?t=1616)
 - [Code Explain](https://youtu.be/qpNG9qrcmrQ)
 - [Clip](https://www.youtube.com/watch?v=qTkESIBd5Qk)

## Technologies Used

 - [VoiceVox Docker](https://hub.docker.com/r/voicevox/voicevox_engine) or [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SociallyIneptWeeb/LanguageLeapAI/blob/main/src/run_voicevox_colab.ipynb)
 - [DeepL](https://www.deepl.com/fr/account/summary)
 - [Deeplx](https://github.com/OwO-Network/DeepLX)
 - [Whisper OpenAI](https://platform.openai.com/account/api-keys)
 - [Seliro TTS](https://github.com/snakers4/silero-models#text-to-speech)
 - [VB-Cable](https://vb-audio.com/Cable/)
 - VtubeStudio


## Installation

1. Install the dependencies

```
pip install -r requirements.txt
```

2. Create config.py and store your Openai API key

```
api_key = 'yourapikey'
```

3. Change the owner name

```
owner_name = "Ardha"
```

if you want to use it for livestream, create a list of users that you want to blacklist on `run.py`

```
blacklist = ["Nightbot", "streamelements"]
```

4. Change the lore or identity of your assistant. Change the txt file at `characterConfig\Pina\identity.txt`

5. If you want to stream on Twitch you need to change the config file at `utils/twitch_config.py`. Get your token from [Here](https://twitchapps.com/tmi/). Your token should look something like oauth:43rip6j6fgio8n5xly1oum1lph8ikl1 (fake for this tutorial). After you change the config file, you can start the program using Mode - 3
```
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'testing' # You don't need to change this
token = 'oauth:43rip6j6fgio8n5xly1oum1lph8ikl1' # get it from https://twitchapps.com/tmi/.
user = 'ardha27' # Your Twitch username
channel = '#aikohound' # The channel you want to retrieve messages from
```

6. Choose which TTS you want to use, `VoiceVox` or `Silero`. Uncomment and Comment to switch between them

```
# Choose between the available TTS engines
# Japanese TTS
voicevox_tts(tts)

# Silero TTS, Silero TTS can generate English, Russian, French, Hindi, Spanish, German, etc. Uncomment the line below. Make sure the input is in that language
# silero_tts(tts_en, "en", "v3_en", "en_21")
```

If you want to use VoiceVox, you need to run VoiceVox Engine first. You can run them on local using [VoiceVox Docker](https://hub.docker.com/r/voicevox/voicevox_engine) or on Google Colab using [VoiceVox Colab](https://github.com/SociallyIneptWeeb/LanguageLeapAI/blob/main/src/run_voicevox_colab.ipynb). If you use the Colab one, change `voicevox_url` on `utils\TTS.py` using the link you get from Colab.

```
voicevox_url = 'http://localhost:50021'
```

if you want to see the voice list of VoiceVox you can check this [VoiceVox](https://voicevox.hiroshiba.jp) and see the speaker id on `speaker.json` then change it on `utils/TTS.py`. For Seliro Voice sample you can check this [Seliro Samples](https://oobabooga.github.io/silero-samples/index.html)

7. Choose which translator you want to use depends on your use case (optional if you need translation for the answers). Choose between google translate or deeplx. You need to convert the answer to Japanese if you want to use `VoiceVox`, because VoiceVox only accepts input in Japanese. The language answer from OpenAI will depens on your assistant lore language `characterConfig\Pina\identity.txt` and the input language

```
tts = translate_deeplx(text, f"{detect}", "JA")
tts = translate_google(text, f"{detect}", "JA")
```

`DeepLx` is free version of `DeepL` (No API Key Required). You can run [Deeplx](https://github.com/OwO-Network/DeepLX) on docker, or if you want to use the normal version of deepl, you can make the function on `utils\translate.py`. I use `DeepLx` because i can't register on `DeepL` from my country. The translate result from `DeepL` is more accurate and casual than Google Translate. But if you want the simple way, just use Google Translate.

8. If you want to use the audio output from the program as an input for your `Vtubestudio`. You will need to capture your desktop audio using `Virtual Cable` and use it as input on VtubeStudio microphone.

9. If you planning to use this program for live streaming Use `chat.txt` and `output.txt` as an input on OBS Text for Realtime Caption/Subtitles

## FAQ

1. Error Transcribing Audio

```
def transcribe_audio(file):
    global chat_now
    try:
        audio_file= open(file, "rb")
        # Translating the audio to English
        # transcript = openai.Audio.translate("whisper-1", audio_file)
        # Transcribe the audio to detected language
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        chat_now = transcript.text
        print ("Question: " + chat_now)
    except:
        print("Error transcribing audio")
        return

    result = owner_name + " said " + chat_now
    conversation.append({'role': 'user', 'content': result})
    openai_answer()
```

Change this Line of Code to this. This will help you to get more information about the error

```
def transcribe_audio(file):
    global chat_now
    audio_file= open(file, "rb")
    # Translating the audio to English
    # transcript = openai.Audio.translate("whisper-1", audio_file)
    # Transcribe the audio to detected language
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    chat_now = transcript.text
    print ("Question: " + chat_now)


    result = owner_name + " said " + chat_now
    conversation.append({'role': 'user', 'content': result})
    openai_answer()
```

Another option to solve this problem, you can upgrade the OpenAI library to the latest version. Make sure the program capture your voice/sentence, try to hear the `input.wav`

2. Mecab Error

this library is a little bit tricky to install. If you facing this problem, you can just delete and don't use the `katakana_converter` on `utils/TTS.py`. That function is optional, you can run the program without it. Delete this two line on `utils/TTS.py`  

```
from utils.katakana import *
katakana_text = katakana_converter(tts)
```

and just pass the `tts` to next line of the code

```
params_encoded = urllib.parse.urlencode({'text': tts, 'speaker': 46})
```

## Credits

This project is inspired by the work of shioridotdev. Special thanks to the creators of the technologies used in this project including VoiceVox Engine, DeepL, Whisper OpenAI, and VtubeStudio.











