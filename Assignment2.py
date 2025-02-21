"""
FAQ Bot Program
Author: Juan Naranjo
Date: 20/2/2025

This program loads FAQ data from a file, processes user input with spaCy for linguistic analysis,
and uses fuzzy regex matching to find the best response. It handles greetings, goodbyes, and unknown
queries with appropriate fallback responses.
"""

import discord
import re
import string
import spacy
import random

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

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
    return s.lower().strip().translate(str.maketrans("", "", string.punctuation))  # Clean up string

def matching(utterance, faq_data):
    """
    Find the best match for the user's input using fuzzy regex matching.
    Returns the index of the matched FAQ or -1 if no found.
    Theres an issue with this one and i dont know what is it
    """
    utterance_fixed = fixed_string(utterance)  # Preprocess the user's input
    best_match = None  # Initialize to store the best match index
    best_match_length = float('inf')  # Set a large number for comparison

    # Loop through the FAQ data to find the best match
    for i, (_, pattern, _, answer) in enumerate(faq_data):
        if re.search(pattern, utterance_fixed, re.IGNORECASE):  # Match using regex
            match_length = abs(len(pattern) - len(utterance_fixed))  # Measure match length difference
            if match_length < best_match_length:  # Update best match if current is better
                best_match = i
                best_match_length = match_length

    return best_match if best_match is not None else -1  # Return the matched index or -1 for no match

def new_response(utterance, intent, faq_data):
    """
    Create a responbse if not found generate a fallback
    """
    if intent != -1:  # If a valid match is found
        return faq_data[intent][3]  # Return the answer associated with the matched FAQ entry
    return handle_unknown_input(utterance)  # Fall back to handling unknown input

def handle_unknown_input(utterance):
    """
    Unknown input and handle the fallback using NER
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
    Returns a random fun fact when a trivia request is detected.
    """
    facts = [
        "Did you know that honey never spoils?",
        "There's more computers than persons maybe",
        "Octopuses have three hearts and their blood is blue due to copper-rich hemocyanin!",
        "A day on Venus is longer than a year on Venus!",
        "There's a snake in my boot"
    ]
    return random.choice(facts)  # Return a random fact from the list

def main():
    """
    Implements the main functionality of the FAQ bot, processing user input
    and generating responses based on the FAQ data or fallback strategies.
    """
    # Load the FAQ data from the file
    filename = "questions.txt"  # Replace with your own file name
    faq_data = load_FAQ_data(filename)  # Load the FAQ entries

    if not faq_data:  # If no data was loaded
        print("No FAQ data loaded")
        return

    print("Im the bot of the fourth dimesion tell me what you need to know")
    print()

    while True:
        utterance = input(">>> ").strip()  # Get user input and remove extra spaces

        # Handle greetings and goodbyes
        if fixed_string(utterance) == "hello":
            print("Hello 3 dimensional being")
            continue
        elif fixed_string(utterance) == "goodbye":
            print("Goodbye , Im hungry")
            break  # Exit the loop and end the program

        # Match the user's input to the FAQ data using fuzzy regex
        intent = matching(utterance, faq_data)
        response = new_response(utterance, intent, faq_data)  # Generate a response
        print(response)  # Print the response
        print()  # Add a newline for readability

# Run the program if this file is executed directly
if __name__ == "__main__":
    main()
