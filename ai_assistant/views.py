from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
import os
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
import json

@login_required
def ai_assistant(request):
    # if not request.user.is_pro:
    #     return render(request, 'users/pro_required.html')
    if request.method == "POST":
        
        # OpenAI API Key
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # User input from POST request
        try:
            data = json.loads(request.body)
            user_input = data.get("message", "")
        except json.JSONDecodeError:
            user_input = ""


        # Collect user data from the authenticated CustomUser model
        user = request.user
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": str(user.age),
            "height": str(user.height),
            "gender": str(user.gender),
            "weight": str(user.weight),
            "activity_level": str(user.activity_level),
            "dietary_preferences": str(user.dietary_preferences),
            "allergies": str(user.allergies),
            "medical_conditions": str(user.medical_conditions),
            "goal": str(user.goal),
            "calorie_target": str(user.calorie_target),
        }

        # Prepare messages for GPT
        messages = [
            {"role": "system", "content": "You are an AI assistant that provides personalized nutrition and fitness advice."},
            {"role": "user", "content": f"User details: {user_data}. User query: '{user_input}'"}
        ]
        

        try:
            # Call OpenAI API
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )
            assistant_response = response.choices[0].message.content
            return JsonResponse({"response": assistant_response}, status=200)
        except Exception as e:
            return JsonResponse({"error": f"Error: {str(e)}"}, status=500)

    elif request.method == "GET":
        return render(request, "ai_assistant/chat.html")

    return JsonResponse({"error": "Invalid request method."}, status=400)
