import streamlit as st
import pandas as pd
import random

# Markov Chain class
class MarkovChain:
    def __init__(self, n=1):
        self.n = n  # Number of previous words to consider
        self.model = {}

    def train(self, text):
        # Split the text into words
        words = text.split()
        
        # Create n-grams and build the model
        for i in range(len(words) - self.n):
            key = tuple(words[i:i + self.n])  # n-gram as key
            next_word = words[i + self.n]     # next word after the n-gram
            
            if key not in self.model:
                self.model[key] = []
            self.model[key].append(next_word)

    def generate(self, seed, length=50):
        # Generate new lyrics based on the seed
        current_key = tuple(seed.split()[-self.n:])  # Get the last n words
        output = list(current_key)
        
        for _ in range(length):
            if current_key not in self.model:
                # If the key is not found, restart with a random key from the model
                current_key = random.choice(list(self.model.keys()))
                output.extend(list(current_key))
            else:
                next_words = self.model[current_key]
                next_word = random.choice(next_words)  # Randomly choose the next word
                output.append(next_word)
                current_key = tuple(output[-self.n:])  # Update the key
        
        return ' '.join(output)

# Load your dataset
data = pd.read_csv('D:/Dataset/archive/spotify_millsongdata.csv')  # Update with your file path

# Combine all lyrics into a single string (adjust column name as needed)
lyrics = ' '.join(data['text'].dropna().tolist())

# Create and train the Markov Chain model
n = 2  # Use bigrams (2 previous words)
markov_chain = MarkovChain(n)
markov_chain.train(lyrics)

# Streamlit app setup
st.title("Markov Chain Lyrics Generator")
st.write("Enter a seed text, and the model will generate new lyrics based on it.")

# User input for the seed text
seed_text = st.text_input("Enter seed text:", value="I love you")

# Button to generate lyrics
if st.button("Generate Lyrics"):
    generated_lyrics = markov_chain.generate(seed_text, length=50)
    st.write("### Generated Lyrics:")
    st.write(generated_lyrics)
