import openai
import requests

# Initialize OpenAI API
def query_openai_model(model_name, question, context):
    openai.api_key = 'openai_api_key'
    
    # Prepare the messages for the chat completion
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question}
    ]

    if context:
        for ctx in context:
            messages.append({"role": "assistant", "content": ctx['text']})

    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
        max_tokens=150
    )

    return response['choices'][0]['message']['content']


def query_replicate_model(model_name, prompt, context):
    # Define the endpoint URL and headers for the API request
    endpoint_url = f'https://api.replicate.com/v1/predictions'
    headers = {
        'Authorization': f'Token api_key_here',
        'Content-Type': 'application/json'
    }

    # Define the payload for the API request
    payload = {
        'version': model_name,
        'input': {
            'prompt': prompt,
            'context': context
        }
    }

    # Make the API request
    response = requests.post(endpoint_url, headers=headers, json=payload)
    response_json = response.json()

    # Extract the model's response from the API response
    model_response = response_json['predictions'][0]['output']
    return model_response
