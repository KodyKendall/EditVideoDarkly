#TODO: Here is where we will integrate the claude API so we can easily prompt and get responses from claude. 
#API Key: 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
#Claude documentation
#https://github.com/anthropics/anthropic-sdk-python

import os
# from anthropic import Anthropic
import anthropic

class ClaudeClient:
    def __init__(self, api_key):
        self.client = anthropic.Client(api_key=api_key)
        self.model = "claude-2"  # Use the latest Claude model

    def prompt(self, prompt, max_tokens=1000):
        message = self.client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="claude-3-opus-20240229",
        )
        return message.content

        # message = [
        #     anthropic.Message(role="system", content="You are Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest."),
        #     anthropic.Message(role="user", content=prompt)
        # ]

        # response = self.client.messages.create(
        #     prompt=message,
        #     max_tokens_to_sample=max_tokens,
        #     model=self.model
        # )

        # return response.completion

# Example usage
if __name__ == "__main__":
    api_key = "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"
    claude = ClaudeClient(api_key)

    prompt = "What is the capital of France?"
    response = claude.prompt(prompt)
    print(response)

    import os
from anthropic import Anthropic

client = Anthropic(
    # This is the default and can be omitted
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

