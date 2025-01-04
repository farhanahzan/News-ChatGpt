import threading
import queue
import requests
import os

q = queue.Queue()
valid_proxies = set()  # Changed to set to avoid duplicates

# Load existing valid proxies if file exists
if os.path.exists('valid_proxies.txt'):
    with open('valid_proxies.txt', 'r') as f:
        valid_proxies.update(f.read().splitlines())

# Read proxies from input file
with open('free-ip.txt', "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        if p.strip() and p not in valid_proxies:  # Only check new proxies
            q.put(p)

def check_proxy():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            response = requests.get("https://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=2)
            if response.status_code == 200:
                valid_proxies.add(proxy)
                print(f"Valid proxy: {proxy}")
        except Exception as e:
            print(f"Invalid proxy: {proxy}")
        q.task_done()

# Create and start multiple threads
thread_count = 10  # You can adjust this number
threads = []
for _ in range(thread_count):
    thread = threading.Thread(target=check_proxy)
    thread.daemon = True
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
q.join()

# Save valid proxies to file
with open('valid_proxies.txt', 'w') as f:
    for proxy in valid_proxies:
        f.write(proxy + '\n')

print(f"Found {len(valid_proxies)} valid proxies. Saved to valid_proxies.txt")