from bs4 import BeautifulSoup
import requests
import tkinter as tk
from tkinter import simpledialog

# Function to perform the web scraping
def scrape_website(url):
    # Send an HTTP GET request to the website
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the website
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract data from the website
        # Example: Extracting all paragraphs
        paragraphs = soup.find_all(['h1','p','h2', 'h3', 'h4', 'h5', 'h6'])
        print("Paragraphs:")
        for para in paragraphs:
            print(para.get_text())


# Function to get URL input from the user
def get_url():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    url = simpledialog.askstring("Input", "Enter the URL of the website to scrape:")
    return url

# Main function
if __name__ == "__main__":
    url = get_url()
    if url:
        scrape_website(url)
    else:
        print("No URL provided.")

