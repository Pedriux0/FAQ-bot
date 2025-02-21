import discord
import re
import string
import spacy
import random

# Load spaCy model for Phase 2
nlp = spacy.load("en_core_web_sm")  # Load English model

def load_FAQ_data(filename):
    """
    Load FAQ data from a file, where each entry consists of a question, pattern, alternate question,
    and its corresponding answer. The data is stored in a list as tuples.
    """
    faq_data = []  # List to store the entries of the data
    try:
        with open(filename, "r") as file:  # Open the file
            # Read all lines from the file and remove any extra whitespace
            lines = [line.strip() for line in file.readlines() if line.strip()]
            i = 0  # Index to loop through the lines
            while i < len(lines) - 3:  # Ensure we do not go out 4 lines per entry
                question = lines[i].strip('"')  # Remove quotes from the question
                pattern = lines[i + 1].strip('"')  # Pattern used to match the user's input
                alt_question = lines[i + 2].strip('"')  # Alternate phrasing of the question
                answer = lines[i + 3]  # The corresponding answer
                faq_data.append((question, pattern, alt_question, answer))  # Add FAQ entry to list
                i += 4  # Move to the next FAQ entry
    except FileNotFoundError:  # If the file is not found
        print(f"Error: The file '{filename}' was not found.")
    return faq_data  # Return the loaded FAQ data

def fixed_string(s):
    """
    Preprocesses a string by converting it to lowercase, removing punctuation,
    and trimming any leading or trailing spaces.
    """
    return s.lower().strip().translate(str.maketrans("", "", string.punctuation))  # Clean up the string

def matching(utterance, faq_data):
    """
    Find the best match for the user's input using fuzzy regex matching.
    Returns the index of the matched FAQ or -1 if no found.
    Theres an issue with this one and i dont know what is it
    """
    utterance_fixed = fixed_string(utterance)  # Clean the user imput
    best_match = None  # Variable to store of the best_match
    best_match_length = float('inf')  # Start with a very large value for comparison

    # Iterate over each FAQ entry to find the best match
    for i, (_, pattern, _, answer) in enumerate(faq_data):
        # Search for the pattern in the user's input (case insensitive)
        if re.search(pattern, utterance_fixed, re.IGNORECASE):
            match_length = abs(len(pattern) - len(utterance_fixed))  # Measure how closely the lengths match
            if match_length < best_match_length:  # Update the best match if the current one is better
                best_match = i
                best_match_length = match_length

    return best_match if best_match is not None else -1  # Return the best match index or -1 if no match is found

def new_response(utterance, intent, faq_data):
    """
    Create a responbse if not found generate a fallback
    """
    if intent != -1:  # If a match is found
        return faq_data[intent][3]  # Return the answer corresponding to the matched FAQ entry
    return handle_unknown_input(utterance)  # If no match is found, handle as unknown input

def handle_unknown_input(utterance):
    """
    Unknown input and handle the fallback
    """
    doc = nlp(utterance)

    # Check if it's a common request for trivia
    if any(token.lemma_ in ["interesting", "fact"] for token in doc):
        return get_random_fact()

    # Check for command-like input
    if doc[0].pos_ == "VERB" and doc[0].dep_ == "ROOT":
        return "I can't do that, but maybe I can help you with something else!"

    # Extract named entities and generate responses accordingly
    entities = {ent.text: ent.label_ for ent in doc.ents}
    if entities:  # If any entities were found
        for entity, label in entities.items():  # Iterate over the found entities
            if label in ["GPE", "LOC"]:  # If the entity is a location
                return f"Sorry, I don’t know but you could try Google Maps. Here’s a link: https://www.google.com/maps/search/{entity.replace(' ', '_')}"
            elif label in ["PERSON", "ORG"]:  # If the entity is a person or organization
                return f"Sorry, I don’t know who they are, but you can search {entity} on Wikipedia: https://en.wikipedia.org/wiki/{entity.replace(' ', '_')}"

    # Default fallback
    return f"Sorry, I don’t know but maybe you could try searching for '{utterance}' on Google."

def get_random_fact():
    """
    Returns a random fun .
    """
    facts = [
        "Did you know that honey never spoils?",
        "There's more computers than persons maybe",
        "Octopuses have three hearts and their blood is blue due to copper-rich hemocyanin!",
        "A day on Venus is longer than a year on Venus!",
        "There's a snake in my boot"
    ]
    return random.choice(facts)  # Randomly select a fun fact from the list

# Load FAQ data from file (questions.txt should be in the same directory or specify full path)
filename = "questions.txt"
faq_data = load_FAQ_data(filename)  # Load FAQ entries from the file

# Discord bot setup
intents = discord.Intents.default()  # Create a new intent object for the bot
intents.message_content = True  #bot can read message content
client = discord.Client(intents=intents)  # Create a new Discord client

@client.event
async def on_ready():
    """ Event that is triggered when the bot is successfully connected and ready. """
    print(f"Welcome my dear bot {client.user}")  # Print bot's name

@client.event
async def on_message(message):
    """ Event that processes incoming messages and generates bot responses. """
    if message.author == client.user:  # Ignore messages sent by the bot itself
        return

    user_input = message.content.strip()  # Get the content of the user's message

    # Handle greetings and goodbyes
    if fixed_string(user_input) == "hello":
        await message.channel.send("Nice to meet you, in what can i help u")  # Send a greeting response
        return
    elif fixed_string(user_input) == "goodbye":
        await message.channel.send("See ya")  # Send a goodbye response
        return

    # Match the user's input with the FAQ data
    intent = matching(user_input, faq_data)
    response = new_response(user_input, intent, faq_data)  # Generate
    await message.channel.send(response)  # Send the response to the user

# Run the bot with the token obtained from a file
with open("bot_token.txt") as file:
    token = file.read().strip()  # Read the token from the file
client.run(token)  # Run the bot using the token
