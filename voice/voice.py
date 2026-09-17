import pyttsx3

# ინიციალიზაცია (Windows-ზე ავტომატურად იყენებს SAPI5-ს)
engine = pyttsx3.init()

# ხმის სიჩქარის რეგულირება (სტანდარტული 200-ია, 160 უფრო ბუნებრივია)
engine.setProperty('rate', 160)

# ხმის ხმისსიმაღლე (0.0-დან 1.0-მდე)
engine.setProperty('volume', 1.0)

# ტექსტის გახმოვანება
engine.say("Move detected. Pawn from g2 to g4.")
engine.runAndWait()