import asyncio
import edge_tts
import pygame
import os

# ჭადრაკის ასოების ქართული ტრანსლიტერაცია
LETTERS_GEO = {
    'a': 'ა', 'b': 'ბ', 'c': 'გ', 'd': 'დ',
    'e': 'ე', 'f': 'ვ', 'g': 'ზ', 'h': 'თ'
}

def move_to_georgian(move_str):
    from_sq = move_str[:2]
    to_sq = move_str[2:4]
    from_geo = f"{LETTERS_GEO.get(from_sq[0], from_sq[0])} {from_sq[1]}"
    to_geo = f"{LETTERS_GEO.get(to_sq[0], to_sq[0])} {to_sq[1]}"
    return f"{from_geo}-დან {to_geo}-ზე"

async def _generate_audio(text, output_file):
    # ka-GE-EkaNeural არის Microsoft-ის ქართული ხმა
    # ka-GE-GiorgiNeural
    communicate = edge_tts.Communicate(text, "ka-GE-EkaNeural")
    await communicate.save(output_file)

def speak_georgian(text):
    print(f"🔊 რობოტი ამბობს: {text}")
    file_path = "temp_voice.mp3"
    
    # აუდიოს გენერირება
    asyncio.run(_generate_audio(text, file_path))

    # დაკვრა pygame-ით
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    if os.path.exists(file_path):
        os.remove(file_path)



# --- ტესტირება ---
if __name__ == "__main__":
    speak_georgian("თამაში დაიწყო, ველოდები თქვენს სვლას")
    
    move_text = move_to_georgian("g2g4")
    speak_georgian(f"თქვენ ითამაშეთ {move_text}")