import openai
from dotenv import load_dotenv
import os

# Function to generate application letter using OpenAI


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
                 ALSO WENN DIE FIRMA ENGLISCH SCHREIBT, SCHREIBST DU ACUH IN ENGLISH!!! Denk daran! Falls in der Auschreibung ein Ansprechpartner genannt wurde, dann sprich diesen auch in der Grußzeile an.
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
