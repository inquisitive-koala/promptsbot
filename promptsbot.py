import discord
import random

# Global variables
helpstring = "**$prompts please**: 2 characters and 2 prompts.\n" + \
	"**$prompts <number of characters> <number of prompts>**: " + \
	"Customize the number of characters and prompts, up to 10 for both.\n" + \
	"* Any other command starting with the word '**$prompts** ': " + \
	"Generates this help message.\n\n" + \
	"Note that repeated characters/prompts are possible."

characters = open('dcmk_characters.txt').readlines()
characters = [c.strip() for c in characters]
prompts = open('prompts.txt').readlines()
prompts = [p.strip() for p in prompts]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')

def SelectFromList(lst, n):
	# To do: eliminate the possibility of duplicates.
	return random.choices(lst, k=n)

def FormattedPrompts(n_char, n_prompts):
	selected_chars = SelectFromList(characters, n_char)
	selected_prompts = SelectFromList(prompts, n_prompts)

	formatted = ''
	if selected_chars:
		formatted += '**Characters:**\n'
		for c in selected_chars:
			formatted += f'{c}\n'

	if selected_chars and selected_prompts:
		formatted = formatted + '\n'

	if selected_prompts:
		formatted += "**Prompts:**\n"
		for p in selected_prompts:
			formatted += f'{p}\n'

	return formatted

def FormattedPromptsTest():
	FormattedPrompts(1, 1)
	FormattedPrompts(0, 1)
	FormattedPrompts(2, 2)
	FormattedPrompts(4, 4)
	FormattedPrompts(10, 10)

def PromptsOrError(tokens):
	"""Returns the response string, or an error message"""
	if len(tokens) == 2 and tokens[1] == 'please':
		return FormattedPrompts(2, 2)
	elif len(tokens) == 3:
		try:
			n_char = int(tokens[1])
			n_prompts = int(tokens[2])
		except:
			return 'Number of characters and prompts must be numerals and whole numbers.'

		if n_char < 0 or n_prompts < 0:
			return 'Number of characters and prompts must be 0 or more.'

		n_char = min(10, n_char)
		n_prompts = min(10, n_prompts)
		return FormattedPrompts(n_char, n_prompts)
	else:
		return helpstring

def PromptsOrErrorTest():
	print(PromptsOrError(['dummy', 'please']))
	print(PromptsOrError(['dummy', '2', '3']))
	print(PromptsOrError(['dummy', '2', '3', '4']))
	print(PromptsOrError(['dummy', '2']))
	print(PromptsOrError(['dummy']))
	print(PromptsOrError(['dummy', 'two', 'three']))
	print(PromptsOrError(['dummy', '3.1', '4']))
	print(PromptsOrError(['dummy', '-1', '0']))
	print(PromptsOrError(['dummy', '0', '1']))
	print(PromptsOrError(['dummy', '100', '100']))

@client.event
async def on_message(message):

	if message.author == client.user:
		return

	# Split on whitespace.
	tokens = message.content.split()
	print('tokens:', tokens)

	if tokens and tokens[0] == '$prompts':
		await message.channel.send(PromptsOrError(tokens), reference=message)


client_token = open('token.txt').read().strip()

client.run(client_token)