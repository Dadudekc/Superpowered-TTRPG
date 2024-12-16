# dm_interface.py
import subprocess
import openai  # If using OpenAI's API
import os

def send_prompt_to_dm(prompt: str, dm_option: str = 'mistral') -> str:
    """
    Sends a prompt to the chosen DM backend and returns the response.
    
    Parameters:
    - prompt (str): The prompt to send to the DM.
    - dm_option (str): 'openai' or 'mistral' to choose the DM backend.
    
    Returns:
    - response (str): The DM's response.
    """
    if dm_option == 'openai':
        return send_prompt_to_chatgpt(prompt)
    elif dm_option == 'mistral':
        return send_prompt_to_mistral(prompt)
    else:
        return "Invalid DM option selected."

def send_prompt_to_chatgpt(prompt: str) -> str:
    """
    Sends a prompt to OpenAI's ChatGPT and returns the response.
    """
    # Ensure you have set your OpenAI API key in environment variables or replace 'YOUR_API_KEY' with your key.
    openai.api_key = os.getenv('OPENAI_API_KEY')  # It's safer to use environment variables.
    try:
        response = openai.Completion.create(
            engine="gpt-4",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("Error communicating with OpenAI's ChatGPT:", e)
        return "An error occurred while communicating with the OpenAI DM."

def send_prompt_to_mistral(prompt: str) -> str:
    """
    Sends a prompt to Mistral 7B running locally via Ollama Run and returns the response.
    """
    try:
        # Use the exact model name as shown in "ollama list"
        model_name = "mistral:latest"
        print(f"Running: ollama run {model_name} \"{prompt}\"")  # Debugging log
        
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error communicating with Mistral 7B via Ollama Run:", e)
        print("Output:", e.output)
        return "An error occurred while communicating with the local DM."

