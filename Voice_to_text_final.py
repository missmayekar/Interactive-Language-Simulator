import speech_recognition as sr
import pyttsx3

# Voice mapping per your instruction
VOICE_MAPPING = {
    "en-US": 0,    # Albert
    "hi-IN": 87,   # Lekha
    "fr-FR": 39,   # Flo
    "es-MX": 21    # Eddy
}

LANGUAGE_OPTIONS = {
    "1": ("English", "en-US"),
    "2": ("Hindi", "hi-IN"),
    "3": ("French", "fr-FR"),
    "4": ("Spanish", "es-MX")
}

def speak_text(text, tts_engine):
    tts_engine.say(text)
    tts_engine.runAndWait()

def recognize_user_input(recognizer, microphone, language_code):
    print("🟢 Adjusting for ambient noise... Please wait.")
    recognizer.adjust_for_ambient_noise(microphone, duration=1)

    print("🎤 Please speak now...")
    audio = recognizer.listen(microphone)

    print("🟣 Recognizing...")
    try:
        text = recognizer.recognize_google(audio, language=language_code)
        print(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, could not understand the audio.")
        return "[Unrecognized]"
    except sr.RequestError as e:
        print(f"❌ Could not request results from Google Speech Recognition service; {e}")
        return "[Error]"

def parse_script(script_str):
    """Parse user-pasted script string into list of (role, text) tuples."""
    lines = script_str.strip().split('\n')
    conversation = []
    for line in lines:
        if ':' in line:
            role, text = line.split(':', 1)
            conversation.append((role.strip(), text.strip()))
        else:
            print(f"⚠️ Skipping invalid line (missing colon): {line}")
    return conversation

def main():
    # Step 1: Language selection
    print("\nPlease choose the language for conversation:")
    for key, (lang_name, _) in LANGUAGE_OPTIONS.items():
        print(f"{key}. {lang_name}")

    choice = ""
    while choice not in LANGUAGE_OPTIONS:
        choice = input("\nEnter choice number (1-4): ").strip()

    selected_language_name, language_code = LANGUAGE_OPTIONS[choice]
    print(f"\n✅ You selected: {selected_language_name} ({language_code})")

    # Step 2: Ask for conversation script as single pasted string
    print("\nPlease paste your entire conversation script below.")
    print("Use the format: Role: Text on each line.")
    print("Example:")
    print("User: Hello, I want to buy a shirt.\nNative Speaker: Sure, what size?")
    print("\nPaste your script, then enter an empty line to finish:\n")

    user_lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        user_lines.append(line)

    script_input = "\n".join(user_lines)
    conversation_script = parse_script(script_input)

    if not conversation_script:
        print("❌ No valid conversation lines provided. Exiting.")
        return

    # Initialize recognizer and TTS
    recognizer = sr.Recognizer()
    tts_engine = pyttsx3.init()

    voices = tts_engine.getProperty('voices')
    selected_voice_index = VOICE_MAPPING[language_code]

    if selected_voice_index < len(voices):
        tts_engine.setProperty('voice', voices[selected_voice_index].id)
    else:
        print(f"⚠️ Warning: Voice index {selected_voice_index} not found. Using default voice.")

    transcript_text = ""

    print("\n=== Conversation Start ===")
    with sr.Microphone() as source:
        for role, line in conversation_script:
            if role.lower() == "user":
                print(f"🗣️ Your turn! Expected line: \"{line}\"")
                user_response = recognize_user_input(recognizer, source, language_code)
                transcript_text += f"User: {user_response}\n"
            else:
                print(f"🤖 {role} says: \"{line}\"")
                speak_text(line, tts_engine)
                transcript_text += f"{role}: {line}\n"

    print("\n=== Conversation Transcript ===")
    print(transcript_text)

if __name__ == "__main__":
    main()
