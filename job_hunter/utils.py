import openai
from dotenv import load_dotenv
import os
from job_hunter.models import ChatLog, PInfo 
from django.contrib.auth import get_user_model


User = get_user_model()


def generate_application_letter(
    name, p_info, position, comp_name, comp_desc, offer
):
    try:
        # Load environment variables from .env file
        load_dotenv()

        # Conversation history and the initial system message
        system_role = f"You are here to help the user to find a job"  # Define system role here
        messages = [
            {"role": "system", "content": system_role},
            {
                "role": "user",
                "content": f"""
                Erstelle ein Anschreiben im Namen von: '{name}' - '{p_info}' als Bewerbung auf die
                 Stelle als {position} Bei folgendem Arbeitgeber: '{comp_name} - {comp_desc}'. 
                 Dies ist das Stellenangebot: {offer}. Halte dich bei der Erstellung des Anschreibens
                 an die SPRACHE, IN DER DIE AUSSCHREIBUNG UND DIE ARBEITGEBERBESCHREIBUNG VERFASST WURDE (WICHTIG!!!!).
                 ALSO WENN DIE FIRMA ENGLISCH SCHREIBT, SCHREIBST DU AUCH IN ENGLISH!!! Denk daran! Falls in der Auschreibung ein Ansprechpartner genannt wurde, dann sprich diesen auch in der Grußzeile an.
                 """,
            },
        ]

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=1.0,
            max_tokens=1000,
        )

        letter = response.choices[0].message.content
        return letter
    except Exception as e:
        print(
            "OpenAI Error",
            f"Failed to generate application letter.\nError: {e}",
        )
        return None

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

import tiktoken
from django.db.models import Q

def count_tokens(text, model="gpt-4"):
    tokenizer = tiktoken.encoding_for_model(model)
    return len(tokenizer.encode(text))

def chat_with_gpt(user_id, user_input, model="gpt-4", max_input_tokens=7000):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return "Error: User not found."

    # Sonderfall: MIND-Befehl
    if user_input.strip().startswith("MIND"):
        reminder = user_input[len("MIND"):].strip()
        ChatLog.objects.create(
            user=user,
            user_input=f"MIND: {reminder}",
            assistant_response=f"I will remember this: {reminder}"
        )
        return f"I will remember this: {reminder}"

    # Profiltext
    try:
        p_info = PInfo.objects.get(user=user)
        profile = f"Name: {user.first_name} {user.last_name}\nEmail: {user.email}\nBackground: {p_info.background}"
    except PInfo.DoesNotExist:
        profile = "No profile available."

    profile_tokens = count_tokens(profile)

    # Alle gespeicherten MIND-Einträge sammeln
    mind_logs = ChatLog.objects.filter(user=user, user_input__startswith="MIND:").order_by('created_at')
    mind_text = "\n".join(log.user_input[5:] for log in mind_logs)
    mind_tokens = count_tokens(mind_text)

    # Token-Budget nach Abzug von Profil, MINDs und prompt-Spielraum
    reserved_for_prompt = 1000  # bleibt für aktuelle Nachricht + GPT-Antwort
    remaining_tokens = max_input_tokens - (profile_tokens + mind_tokens + reserved_for_prompt)

    # Chatverlauf (nur so viel wie ins Budget passt)
    chat_history = []
    total_history_tokens = 0
    logs = ChatLog.objects.filter(user=user).exclude(user_input__startswith="MIND").order_by('-created_at')

    for log in logs:
        pair = f"U: {log.user_input}\nA: {log.assistant_response}"
        tokens = count_tokens(pair)
        if total_history_tokens + tokens > remaining_tokens:
            break
        chat_history.insert(0, pair)  # Älteste zuerst
        total_history_tokens += tokens

    # Nachrichten an GPT
    system_prompt = f"""
You are a helpful assistant. Here is user information:

{profile}

Known reminders:
{mind_text}

Recent chat history:
{'\n'.join(chat_history)}
    """

    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": user_input.strip()}
    ]

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=1.0,
            max_tokens=1000,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        return f"Error while contacting OpenAI: {str(e)}"

    ChatLog.objects.create(
        user=user,
        user_input=user_input,
        assistant_response=reply
    )

    return reply
