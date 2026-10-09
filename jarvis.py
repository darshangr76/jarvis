import ollama
import subprocess
import webbrowser
from datetime import datetime
from anyrobo import Personality

# ---------- CONFIG ----------
MODEL = "qwen2.5-coder:3b"
VOICE = "Samantha"
SPEAK_REPLIES = True

# ---------- PERSONALITY ----------
p = Personality.builtin("jarvis")
messages = [{"role": "system", "content": p.system_prompt}]
print(f"Loaded: {p.name} ({p.tone}) - voice: {p.voice}")


# ---------- ACTIONS ----------
def run_action(user_text):
    clean = user_text.strip()
    while clean.startswith(("You>", "you>", ">", "JARVIS>")):
        if ">" in clean:
            clean = clean.split(">", 1)[-1].strip()
        else:
            clean = clean[1:].strip()
    t = clean.lower()

    if "what time" in t or "the time" in t:
        now = datetime.now().strftime("%I:%M %p").lstrip("0")
        return True, f"The time is {now}, sir."

    if "what date" in t or "today's date" in t or "what day" in t:
        today = datetime.now().strftime("%A, %B %d, %Y")
        return True, f"Today is {today}, sir."

    if t.startswith("open "):
        app = clean[5:].strip()
        try:
            subprocess.run(["open", "-a", app], check=True)
            return True, f"Opening {app}, sir."
        except Exception:
            return True, f"I couldn't find an application named {app}, sir."

    if t.startswith("search ") or t.startswith("google "):
        query = clean.split(" ", 1)[1]
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        return True, f"Searching for {query}, sir."

    if t in ("play music", "play some music", "play a song", "play songs", "play some songs"):
        webbrowser.open("https://music.youtube.com/")
        return True, "Opening YouTube Music for you, sir."

    if t.startswith("play "):
        query = clean[5:].strip()
        if not query:
            webbrowser.open("https://music.youtube.com/")
            return True, "Opening YouTube Music for you, sir."
        webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
        return True, f"Playing {query} on YouTube, sir."

    return False, None


# ---------- SPEAK ----------
def speak(text):
    if not SPEAK_REPLIES:
        return
    try:
        subprocess.run(["say", "-v", VOICE, text], check=False)
    except Exception as e:
        print(f"(voice error: {e})")


# ---------- MAIN LOOP ----------
print(f"\nJARVIS ready (model: {MODEL}). Type 'quit' to exit.\n")

while True:
    user = input("You> ").strip()
    for prefix in ("You> ", "you> ", "> "):
        if user.startswith(prefix):
            user = user[len(prefix):].strip()
    if user.lower() in ("quit", "exit"):
        break
    if not user:
        continue

    handled, reply = run_action(user)

    if not handled:
        messages.append({"role": "user", "content": user})
        try:
            response = ollama.chat(model=MODEL, messages=messages)
            reply = response["message"]["content"]
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            messages.pop()
            reply = f"My apologies, sir. I encountered an error: {e}"

    print(f"JARVIS: {reply}\n")
    speak(reply)
