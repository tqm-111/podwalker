import openai
from gtts import gTTS
from pydub import AudioSegment
import random
import os
from dotenv import load_dotenv

load_dotenv()

#Generate answers from GPT3.5
openai.api_key = os.getenv("OPENAI_API")

text_content = ""

def chat_with_openai(text, words, lang="English"):
    global text_content 
    text_content = text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"A host of the podcast channel shortly welcomes audiences to the podcast, then talks about the topic '{text}' in at least {words} words. The whole podcast is in the language {lang}"},
            {"role": "user", "content": text}
        ],
        # max_tokens = token
    )

    response_text = response['choices'][0]['message']['content']

    return response_text


#Convert the test response to speech by gTTS
def text_to_speech(text, langu):

  #Choose the language
  match langu:
    case "English":
      langu = "en"

    case "Japanese":
      langu = "ja"

    case "Spanish":
      langu = "es"

    case "Vietnamese":
      langu = "vi"

    case "German":
      langu = "de"

    case _:
      langu = "en"

  gtts_object = gTTS(text = text,
     lang = langu,
     slow = False)

  gtts_object.save("gtts.mp3")


#Concatinate audio files
def merge_mp3_files():

    mood = random.randint(0,4)

    match mood:
        case 0:
          intro = AudioSegment.from_mp3(os.path.join(os.getcwd(), "static", "music", "Intro1.mp3"))
        case 1:
          intro = AudioSegment.from_mp3(os.path.join(os.getcwd(), "static", "music", "Intro2.mp3"))
        case 2:
          intro = AudioSegment.from_mp3(os.path.join(os.getcwd(), "static", "music", "Intro3.mp3"))
        case 3:
          intro = AudioSegment.from_mp3(os.path.join(os.getcwd(), "static", "music", "Intro4.mp3"))
        case 4:
          intro = AudioSegment.from_mp3(os.path.join(os.getcwd(), "static", "music", "Intro5.mp3"))


    mood0 = random.randint(0,4)

    match mood0:
        case 0:
          outro = AudioSegment.from_mp3(os.path.join(os.getcwd(), "static", "music", "Intro1.mp3"))
        case 1:
          outro = AudioSegment.from_mp3(os.path.join(os.getcwd(), "static", "music", "Intro2.mp3"))
        case 2:
          outro = AudioSegment.from_mp3(os.path.join(os.getcwd(), "static", "music", "Intro3.mp3"))
        case 3:
          outro = AudioSegment.from_mp3(os.path.join(os.getcwd(), "static", "music", "Intro4.mp3"))
        case 4:
          outro = AudioSegment.from_mp3(os.path.join(os.getcwd(), "static", "music", "Intro5.mp3"))


    audio2 = AudioSegment.from_mp3('gtts.mp3')
    ads = AudioSegment.from_mp3(os.path.join(os.getcwd(), "static", "music", "SampleAd.mp3"))

    combined_audio = ads + intro + audio2 + outro

    name = text_content + ".mp3"
    path = os.path.join(os.path.join(os.getcwd(), "static", name))
    combined_audio.export(path, format='mp3')