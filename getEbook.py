import os
import time
from urllib.request import urlretrieve
from concurrent.futures import ThreadPoolExecutor


def download_image(url, save_path):
    try:
        # Download the image from the URL and save it to the specified path
        urlretrieve(url, save_path)
        print(f"Downloaded: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        time.sleep(5)
        download_image(url, save_path)


def main():
    name = input("输入书本名字")
    count = int(input("输入书本页数"))
    # Create a directory to save downloaded images
    save_directory = f"files/imgs/{name}"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Create a thread pool with 4 worker threads
    num_threads = 50
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Download each image in parallel using the thread pool
        for i in range(count):
            idx = i + 1
            image_urls = f'https://book.pep.com.cn/{name}/files/mobile/{idx}.jpg'
            file_name = f"{idx}.jpg"
            save_path = os.path.join(save_directory, file_name)
            executor.submit(download_image, image_urls, save_path)

    print("All images downloaded successfully!")


if __name__ == "__main__":
    main()
