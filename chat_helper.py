import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def send_message(prompt):
    # Send the query to ChatGPT and read back the response
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7
    ).choices[0].text

    return response