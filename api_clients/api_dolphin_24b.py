import requests
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config.json")
with open(CONFIG_PATH) as f:
    config = json.load(f)

API_KEY = config["api_key"]
BASE_URL = config["base_url"]

def get_dolphin_r1_mistral_24b_response(user_input):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": config["models"]["dolphin_r1_mistral_24b"],
        "messages": [{"role": "user", "content": user_input}],
        "stream": True  # Enable streaming
    }

    response = requests.post(BASE_URL, headers=headers, json=payload, stream=True)

    if response.status_code == 200:
        for line in response.iter_lines():
            if line:  # Skip empty lines
                decoded_line = line.decode("utf-8").strip()
                if not decoded_line:
                    continue  # Skip empty lines

                # Handle control messages (e.g., ": OPENROUTER PROCESSING")
                if decoded_line.startswith(":"):
                    print(f"Control message: {decoded_line}")
                    continue

                # Handle data messages (e.g., "data: {...}")
                if decoded_line.startswith("data:"):
                    try:
                        # Extract JSON data after "data:"
                        json_data = decoded_line[5:].strip()
                        data = json.loads(json_data)

                        # Extract the response content
                        if "choices" in data and len(data["choices"]) > 0:
                            chunk = data["choices"][0].get("delta", {}).get("content", "")
                            if chunk:  # Only yield non-empty chunks
                                yield chunk
                    except (KeyError, json.JSONDecodeError) as e:
                        print(f"Error decoding line: {e}")
                        yield f"Error: Failed to decode API response"
    else:
        yield f"Error: API request failed with status {response.status_code}"