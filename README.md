# SpotifAI
This web app uses OpenAI's GPT-3 model (used in ChatGPT) and SpotiPy to recommend songs based on user's favorite song, and creates a Spotify playlist full of multiple curated songs. Requires OpenAI key to use.

# Tech Stack/Libraries Used

**Flask**

- Flask is used to render the web page and handle requests, such as getting the song from the user. 

**OpenAI GPT-3**

- SpotifAI uses OpenAI's GPT-3 model, specifically the DaVinci 3 engine. This is used to identify the mood of the song, by breaking it up into a list of one word tags. DaVinci 3 is also used to match those tags with specific songs from it's training data. 

**SpotiPy**

- SpotiPY, a python library for the Spotify Web API, is used to pull song links from Spotify, and also verify that the songs that GPT-3 picks are real and available on Spotify. This ensures that even if the user types a song that doesn't exist, a real playlist is still returned.
