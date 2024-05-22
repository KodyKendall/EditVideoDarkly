#TODO: Here is where we will integrate the claude API so we can easily prompt and get responses from claude. 
#API Key: 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
#Claude documentation
#https://github.com/anthropics/anthropic-sdk-python

import anthropic

class ClaudeClient:
    def __init__(self, api_key):
        self.client = anthropic.Client(api_key=api_key)
        self.model = "claude-v1"  # Choose the appropriate Claude model version

    def prompt(self, prompt, max_tokens=1000):
        response = self.client.completions.create(
            prompt=f"{anthropic.HUMAN_PROMPT}{prompt}{anthropic.AI_PROMPT}",
            stop_sequences=[anthropic.HUMAN_PROMPT],
            max_tokens_to_sample=max_tokens,
            model=self.model
        )
        return response.completion

# Example usage
if __name__ == "__main__":
    api_key = "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"
    claude = ClaudeClient(api_key)

    prompt = "What is the capital of USA?"
    response = claude.prompt(prompt)
    print(response)