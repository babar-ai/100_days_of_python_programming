import requests
import time
import threading

from concurrent.futures import ThreadPoolExecutor


def fetch_url_content(url):
    response = requests.get(url)
    return response.content


def run_fetch_url_with_out_threading():

    urls = [
        'https://en.wikipedia.org/wiki/Thread_(computing)',
        'https://en.wikipedia.org/wiki/Talk:Thread_(computing)'
        'https://en.wikipedia.org/wiki/Python_(programming_language)',
        'https://en.wikipedia.org/wiki/Talk:Python_(programming_language)',
        'https://en.wikipedia.org/wiki/Java_(programming_language)',
        'https://en.wikipedia.org/wiki/Talk:Java_(programming_language)',
        'https://en.wikipedia.org/wiki/C%2B%2B',    
    ]

    start_time  = time.time()

    for url in urls:
        contents = []
        result = fetch_url_content(url)
        contents.append(result)
        print(f"{url} content downloaded")

    end_time = time.time()
    print(f"Time taken without threading: {end_time - start_time}")



def run_fetch_url_with_threading():

    urls = [
        'https://en.wikipedia.org/wiki/Thread_(computing)',
        'https://en.wikipedia.org/wiki/Talk:Thread_(computing)',
        'https://en.wikipedia.org/wiki/Python_(programming_language)',
        'https://en.wikipedia.org/wiki/Talk:Python_(programming_language)',
        'https://en.wikipedia.org/wiki/Java_(programming_language)',
        'https://en.wikipedia.org/wiki/Talk:Java_(programming_language)',
        'https://en.wikipedia.org/wiki/C%2B%2B'
    ]

    start_time  = time.time()
    threads = []

    for url in urls:
        thread = threading.Thread(target=fetch_url_content, args=(url,))  # here target tells the thread which function should this thread execute?
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()                                                  # and here join tells the thread to wait for the other thread to finish before proceeding

    end_time = time.time()
    
    print(f"\n Time taken with threading: {end_time - start_time}")



'''
Important point :

    here we created 7 threads . let suppose we have 100 urls to fetch, then whether we will create 100 threads?  

    the answer is no. because cpu has limited cores , so it can only handle limited number of threads at a time.  

    the number of threads should be less than or equal to the number of cores

    rather we will use 'ThreadPoolExecutor' from concurrent.futures 

    benifits of using 'ThreadPoolExecutor':  
        1. automatic thread management
        2. automatic thread pool
        3. automatic result collection 
        4. automatic exception handling  

'''
def run_fetch_url_with_thread_pool_executor():

    urls = [
        'https://en.wikipedia.org/wiki/Thread_(computing)',
        'https://en.wikipedia.org/wiki/Talk:Thread_(computing)',
        'https://en.wikipedia.org/wiki/Python_(programming_language)',
        'https://en.wikipedia.org/wiki/Talk:Python_(programming_language)',
        'https://en.wikipedia.org/wiki/Java_(programming_language)',
        'https://en.wikipedia.org/wiki/Talk:Java_(programming_language)',
        'https://en.wikipedia.org/wiki/C%2B%2B'
    ]

    start_time  = time.time()

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_url_content, urls)        # Use when you want more control over individual tasks.
        for result in results:
            print(result)

    end_time = time.time()

    print(f"\n Time taken with thread pool executor: {end_time - start_time}")

if __name__ == "__main__":
    
    run_fetch_url_with_out_threading()
    run_fetch_url_with_threading()
    run_fetch_url_with_thread_pool_executor()

'''
Time taken without threading: 7.1705498695373535

Time taken with threading: 2.153687000274658
'''