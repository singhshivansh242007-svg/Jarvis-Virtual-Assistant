import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from google import genai
import pywhatkit

r = sr.Recognizer()

newsapi = "1e748ba3c9134d749cdf7e4ea560a619"
weatherapi = "ef0bdbf93aa4c75c52c75b15ce18e8d7"

engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 140)

client = genai.Client(api_key="AQ.Ab8RN6KmAfEEpGy3AkrlcpC2hJBynkg6jpPuIWNCI3jqVlVbLw")  # move outside


def speak(text):
    engine.say(text)
    engine.runAndWait()


def aiprocess(command):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=command
    )
    return response.text


def processCommand(c):

    c = c.lower()

    # OPEN WEBSITE
    if c.startswith("open "):
        website = c.replace("open ", "").strip()
        speak(f"Opening {website}")
        webbrowser.open(f"https://www.{website}.com")

    # PLAY SONG
    elif "play" in c:
        qu = c.replace("play", "").strip()
        speak(f"Playing {qu}")
        pywhatkit.playonyt(qu)

    # NEWS
    elif "news" in c:
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        )

        if r.status_code == 200:
            articles = r.json().get("articles", [])
            for article in articles[:5]:
                speak(article["title"])

    # WEATHER
    elif "weather in" in c:
        city = c.replace("weather in", "").strip()

        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherapi}&units=metric"
        )

        if r.status_code == 200:
            data = r.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]

            speak(f"{city} has {temp} degree Celsius with {desc}")
        else:
            speak("City not found")

    elif "exit" in c:
        speak("Goodbye Sir")
        exit()

    else:
        speak("Thinking...")
        output = aiprocess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                word = r.recognize_google(audio)

            print("You said:", word)

            if "jarvis" in word.lower():
                print("Wake word detected!")
                speak("Yes Sir")

                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error:", e)