import os
import requests
from bs4 import BeautifulSoup

def search_images_bing(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f"https://www.bing.com/images/search?q={query}&FORM=HDRSC2"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_elements = soup.find_all('a', class_='iusc')

        image_urls = []
        for img in image_elements:
            m = img['m']
            image_url = eval(m)['murl']  # Extract image URL
            image_urls.append(image_url)

        return image_urls
    else:
        print("Failed to retrieve images from Bing.")
        return []

def download_images(image_urls, num_images):
    storage_path = '/storage/emulated/0/Download'  # Change to Download folder
    os.makedirs(storage_path, exist_ok=True)

    for index, url in enumerate(image_urls[:num_images]):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                # Extract file extension from the URL
                file_extension = url.split('.')[-1].split('?')[0]  # Handle URLs with parameters
                file_path = os.path.join(storage_path, f'image_{index + 1}.{file_extension}')  # Save with the original extension
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f'Downloaded: {file_path}')
            else:
                print(f'Failed to download: {url}')
        except Exception as e:
            print(f'Error downloading {url}: {e}')

def main():
    query = input("What is your query? ")
    print(f"Searching images for: {query}")

    bing_images = search_images_bing(query)

    bing_count = len(bing_images)
    print(f"Bing: {bing_count} images found")

    if bing_count > 0:
        num_images = int(input(f"How many images do you want to download (max {bing_count}): "))

        if 0 < num_images <= bing_count:
            print(f"Downloading {num_images} images...")
            download_images(bing_images, num_images)
        else:
            print("Invalid number of images.")
    else:
        print("No images found.")

if __name__ == "__main__":
    main()
