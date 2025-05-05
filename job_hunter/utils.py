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

def chat_with_gpt(user_id, user_input):
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

    # Benutzerprofil auslesen
    try:
        p_info = PInfo.objects.get(user=user)
        user_profile = f"User: {user.first_name} {user.last_name}, Email: {user.email}, Background: {p_info.background}"
    except PInfo.DoesNotExist:
        user_profile = "User information is unavailable."

    # Letzte 5 Nachrichten holen
    recent_logs = ChatLog.objects.filter(user=user).order_by('-created_at')[:5]
    chat_history = "\n".join([
        f"YOU: {log.user_input}\nCHAT GPT: {log.assistant_response}"
        for log in reversed(recent_logs)
    ])

    # Systemnachricht + aktuelle Eingabe
    messages = [
        {"role": "system", "content": f"""
            You are a helpful assistant. Always remember the user's details:
            {user_profile}
            Previous conversations:
            {chat_history}
        """},
        {"role": "user", "content": user_input}
    ]

    # OpenAI-Request
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=1.0,
            max_tokens=1000,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        return f"Error while contacting OpenAI: {str(e)}"

    # Speichern
    ChatLog.objects.create(
        user=user,
        user_input=user_input,
        assistant_response=reply
    )

    return reply
