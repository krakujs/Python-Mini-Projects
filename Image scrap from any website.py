#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
import threading
import time

# Function to download an image from a URL
def download_image(url, output_dir):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            filename = os.path.join(output_dir, urlparse(url).path.split("/")[-1])
            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
    except:
        print(f"Error downloading {url}")

# Function to scrape image data from a webpage
def scrape_images(url, output_dir, num_threads=4):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    img_urls = [urljoin(url, img.get("src")) for img in soup.find_all("img") if img.get("src")]

    num_images = len(img_urls)
    num_downloaded = 0
    total_size = 0
    start_time = time.time()

    def download_worker():
        nonlocal num_downloaded, total_size
        while img_urls:
            url = img_urls.pop()
            try:
                response = requests.head(url)
                if response.status_code == 200 and response.headers.get("content-type", "").startswith("image/"):
                    total_size += int(response.headers.get("content-length", 0))
                    download_image(url, output_dir)
                    num_downloaded += 1
            except:
                print(f"Error processing {url}")
            print_progress(num_downloaded, num_images, total_size, start_time)

    def print_progress(num_downloaded, num_images, total_size, start_time):
        elapsed_time = time.time() - start_time
        download_rate = total_size / elapsed_time if elapsed_time > 0 else 0
        remaining_time = (num_images - num_downloaded) * (elapsed_time / num_downloaded) if num_downloaded > 0 else 0
        print(f"{num_downloaded}/{num_images} images downloaded ({total_size/1024/1024:.2f} MB) - {download_rate/1024/1024:.2f} MB/s - {remaining_time/60:.2f} min remaining")

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=download_worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    url = input("Enter webpage URL: ")
    output_dir = input("Enter the output directory to save images: ")
    num_threads = int(input("Enter the number of threads to use (default is 4): ") or "4")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    scrape_images(url, output_dir, num_threads)


# In[ ]:




