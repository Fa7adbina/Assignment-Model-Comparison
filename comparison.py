def compare_responses(responses):
    # Basic comparison function to select the best response
    # For simplicity, we can return the response with the highest length
    best_response = max(responses.values(), key=len)
    return best_response
