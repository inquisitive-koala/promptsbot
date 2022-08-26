import discord

helpstring = "**$prompts please**: 2 characters and 2 prompts.\n" + \
	"**$prompts <number of characters> <number of prompts>**: " + \
	"Customize the number of characters and prompts, up to 10 for both.\n" + \
	"* Any other command starting with the word '**$prompts** ': " + \
	"Generates this help message."

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')


def FormattedPrompts(n_char, n_prompts):
	return "%i characters and %i prompts" % (n_char, n_prompts)

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

		if n_char < 1 or n_prompts < 1:
			return 'Number of characters and prompts must be 1 or more.'

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