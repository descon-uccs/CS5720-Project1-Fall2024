# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 12:06:50 2024

@author: pbrown2
"""

import random
import time
import requests
import re
import matplotlib.pyplot as plt

# Brute-force search algorithm
def search_algorithm(arr, key):
    for i in range(len(arr)):
        if arr[i] == key:
            return i
    return len(arr)

# Function to download and clean text from Project Gutenberg
def download_text(url):
    response = requests.get(url)
    text = response.text

    # Remove headers/footers from the text (Project Gutenberg specific cleaning)
    start_index = re.search(r"\*\*\* START OF THIS PROJECT GUTENBERG", text)
    end_index = re.search(r"\*\*\* END OF THIS PROJECT GUTENBERG", text)
    
    if start_index and end_index:
        text = text[start_index.end():end_index.start()]
    
    # Further cleaning of non-ASCII characters
    text = re.sub(r'[^A-Za-z\s]', '', text)
    
    return text

# Save text to a file
def save_text_to_file(text, filename="english_text.txt"):
    with open(filename, "w") as file:
        file.write(text)

# Function to generate random character arrays from text
def generate_datasets(text, sizes, num_arrays):
    datasets = {}
    text_length = len(text)
    for n in sizes:
        datasets[n] = []
        for _ in range(num_arrays):
            start = random.randint(0, text_length - n - 1)
            datasets[n].append(list(text[start:start+n]))
    return datasets

# Function to run experiments and record runtimes
def run_experiments(datasets, characters):
    results = {char: {'worst': [], 'best': [], 'average': []} for char in characters}

    for char in characters:
        for n, arrays in datasets.items():
            times = []
            for arr in arrays:
                start_time = time.time()
                search_algorithm(arr, char)
                times.append(time.time() - start_time)

            # Record the best, worst, and average runtime
            results[char]['worst'].append(max(times))
            results[char]['best'].append(min(times))
            results[char]['average'].append(sum(times) / len(times))

    return results

# Plotting function
def plot_results(results, sizes, output_name):
    for char, data in results.items():
        plt.figure(figsize=(10, 6))
        plt.plot(sizes, data['worst'], label='Worst case', marker='o')
        plt.plot(sizes, data['best'], label='Best case', marker='o')
        plt.plot(sizes, data['average'], label='Average case', marker='o')
        plt.title(f"Runtime analysis for character: {char}")
        plt.xlabel("Array Size (n)")
        plt.ylabel("Runtime (seconds)")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{output_name}_{char}.pdf")  # Save plot for LaTeX
        plt.close()

# Main execution
if __name__ == "__main__":
    # Download and clean text from Project Gutenberg
    gutenberg_url = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Example: Pride and Prejudice by Jane Austen
    text = download_text(gutenberg_url)
    
    # Save the downloaded text to a file
    save_text_to_file(text, "english_text.txt")

    # Dataset sizes and characters to test
    sizes = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    num_arrays_per_size = 50
    test_characters = ['e', 'm', 'Q', '%']

    # Generate datasets
    datasets = generate_datasets(text, sizes, num_arrays_per_size)

    # Run experiments
    results = run_experiments(datasets, test_characters)

    # Plot and save results
    plot_results(results, sizes, "runtime_analysis")
