from api_clients.api_deepseek_r1 import get_deepseek_r1_response
from api_clients.api_mistral_7b import get_mistral_7b_response
from api_clients.api_deepseek_v3 import get_deepseek_v3_response
from api_clients.api_deepseek_r1_distill_llama_70b import get_deepseek_r1_distill_llama_70b_response
from api_clients.api_dolphin_24b import get_dolphin_r1_mistral_24b_response

# Mapping models to API functions
api_functions = {
    "deepseek_r1": get_deepseek_r1_response,
    "mistral_7b": get_mistral_7b_response,
    "deepseek_v3": get_deepseek_v3_response,
    "deepseek_r1_distill_llama_70b": get_deepseek_r1_distill_llama_70b_response,
    "dolphin_r1_mistral_24b": get_dolphin_r1_mistral_24b_response
}

def get_all_model_responses(user_input):
    """
    Returns a dictionary of generators for streaming responses.
    """
    responses = {}

    for model_name, function in api_functions.items():
        try:
            responses[model_name] = function(user_input)  # ✅ Call API generator properly
        except Exception as e:
            responses[model_name] = iter([f"Error: {str(e)}"])  # Handle errors

    return responses
