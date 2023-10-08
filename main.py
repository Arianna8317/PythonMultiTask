import requests, os, time, argparse, aiohttp
import threading, asyncio
from multiprocessing import Process
from pathlib import Path

images = []

urls = ['https://www.google.ru/',
'https://gb.ru/',
'https://ya.ru/',
'https://www.python.org/',
'https://habr.com/ru/all/',
]
with open("images.txt") as f:
    for image in f.readlines():
        images.append(image.strip())

image_path = Path("./images")        

def download(url):
    start_time = time.time()
    response = requests.get(url, stream = True)
    filename = image_path.joinpath(os.path.basename(url))
    with open(filename, "wb") as f:
        f.write(response.content)
        print(f"Downloaded {url} in {time.time()-start_time:.2f} seconds")

async def asinc_download(url):
    start_time = time.time()
    response = await asyncio.get_event_loop().run_in_executor(None,
                                                requests.get, url, {"stream":True})
    filename = image_path.joinpath(os.path.basename(url))
    with open(filename, "wb") as file: 
        file.write(response.content)
    print(f"Downloaded asinc {url} in {time.time() - start_time:.2f} seconds")  

def download_images_threading(urls):
    threads = []
    start_time = time.time()
    for url in urls:
        thread = threading.Thread(target=download, args=[url])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()  

    print(f"Downloaded by threads {url} in {time.time() - start_time:.2f} seconds")  

def download_images_multiprocessing(urls):   
    processes = []
    start_time = time.time()
    for url in urls:
        process = Process(target=download, args=(url,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    print(f"Downloaded by multiprocesses {url} in {time.time() - start_time:.2f} seconds")  

async def download_images_asyncio(urls):
    tasks = []
    start_time = time.time()
    for url in urls:
        task = asyncio.ensure_future(asinc_download(url))
        tasks.append(task)
    await asyncio.gather(*tasks) 
    print(f"Downloaded by asyncio {url} in {time.time() - start_time:.2f} seconds")     

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Загрузка картинок по URL")
    parser.add_argument(
        "--urls",
        default=images,
        nargs="+",
        help="укажите список URL картинок",

    )

    args = parser.parse_args()
    urls = args.urls
    if not urls:
        urls = images
    """print(f"Downloaded  {len(urls)} images by threading")
    download_images_threading(urls)
    print(f"Downloaded  {len(urls)} images by multiprocessing")
    download_images_multiprocessing(urls)"""
    print(f"Downloaded  {len(urls)} images asincronically")
    asyncio.run(download_images_asyncio(urls))




