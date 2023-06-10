import openai

openai.api_key = "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"

completion = openai.ChatCompletion.create(
  model = "gpt-3.5-turbo",
  temperature = 0.8,
  max_tokens = 2000,
  messages = [
    {"role": "system", "content": "You are a funny comedian who tells dad jokes."},
    {"role": "user", "content": "Write a dad joke related to numbers."},
    {"role": "assistant", "content": "Q: How do you make 7 even? A: Take away the s."},
    {"role": "user", "content": "Write one related to programmers."}
  ]
)

print(completion.choices[0].message)