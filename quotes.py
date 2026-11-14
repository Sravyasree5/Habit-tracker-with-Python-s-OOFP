import random
motivational_quotes =[
    "Success is a Habit.",
    "It's the small daily habits that determines who you are!",
    "Consistency leads to growth",
    "Believe in Yourself",
    "Unlocking the ultimate glow-up version of me",
    "Another day, another slay!",
    "Getting atleast 1% better every day"
]

def get_motivation():
    """Returns a inspiring quote from the list"""
    return random.choice(motivational_quotes)