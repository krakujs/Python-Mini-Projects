#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import threading

url = "https://freetestdata.com/wp-content/uploads/2022/02/Free_Test_Data_15MB_MP4.mp4"

def download_chunk(start, end, url, filename):
    headers = {"Range": f"bytes={start}-{end}"}
    response = requests.get(url, headers=headers, stream=True)

    with open(filename, "rb+") as file:
        file.seek(start)
        file.write(response.content)

def download_file(url, num_threads=4):
    response = requests.head(url)
    file_size = int(response.headers.get("Content-Length", 0))

    # Calculate the size of each chunk
    chunk_size = file_size 

    threads = []
    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size - 1
        if i == num_threads - 1:
            end = file_size - 1

        filename = f"part{i}"
        thread = threading.Thread(target=download_chunk, args=(start, end, url, filename))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Combine the downloaded chunks into a single file
    with open("output.zip", "wb") as file:
        for i in range(num_threads):
            filename = f"part{i}"
            with open(filename, "rb") as part:
                file.write(part.read())

            # Delete the downloaded chunks
            os.remove(filename)

if __name__ == "__main__":
    download_file(url)


# In[ ]:




