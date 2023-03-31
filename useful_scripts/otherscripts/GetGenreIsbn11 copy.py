import pandas as pd
import requests

# Path to the csv file
csv_path = "/Users/vicentesebastiao/Desktop/book-review-dataset/BookRelatedData/BX_Books.csv"

# Read the csv file with the appropriate encoding
df = pd.read_csv(csv_path, encoding='latin-1')

# Extract the list of ISBNs from the 'isbn' column of the dataframe
isbn_list = df['isbn'].tolist() #Create a dictionary to store the genres for each ISBN
genre_dict = {}

# Loop through the ISBNs and retrieve the genre for each book
for isbn in isbn_list:
    # Create a dictionary of parameters to pass to the API
    params = {'q': 'isbn:{}'.format(isbn)}

    # Send a GET request to the API endpoint
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the JSON data from the response
        data = response.json()

        # Get the genre for the book, if available
        genre = data['items'][0]['volumeInfo'].get('categories', [])

        # Add the genre to the dictionary, using the ISBN as the key
        genre_dict[isbn] = genre

# Print the dictionary of genres
print(genre_dict)