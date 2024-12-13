import aiohttp
import asyncio
import argparse
import re
import sys
import signal
from urllib.parse import quote
from colorama import Fore, Style

CHARACTERS = ["<", ">", "'", "/", "(", ";", ")", "{", ":", "}", "\\", "=", "$", "`", "|"]
KEYWORD = "lforef74710l"
MAX_CONCURRENT_REQUESTS = 15  

def is_valid_url(url):
    return re.match(r'https?://[^\s]+', url) is not None

def has_parameters(url):
    return '?' in url

async def fetch_html(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
    except Exception:
        return None

async def check_url(session, url, encode):
    parsed_url = re.split(r'(\?.*)', url)
    base_url = parsed_url[0]
    params = parsed_url[1][1:].split('&') if len(parsed_url) > 1 else []

    for param in params:
        param_name, param_value = param.split('=', 1) if '=' in param else (param, '')
        reflected_characters = []

        for char in CHARACTERS:
            modified_param_value = f"{KEYWORD}{quote(char) if encode else char}"
            modified_url = f"{base_url}?{param_name}={modified_param_value}"
            html = await fetch_html(session, modified_url)

            if html and modified_param_value in html:
                reflected_characters.append(char)

        if reflected_characters:
            print(f"{url} ===> [{Fore.MAGENTA}{param_name}{Fore.RESET}] [{Fore.LIGHTGREEN_EX}UNFILTERED{Fore.RESET}] [{Fore.RED} {' '.join(reflected_characters)}{Fore.RESET}]")

async def main(input_file, output_file=None, encode=False):
    with open(input_file, 'r') as f:
        urls = set(line.strip() for line in f if line.strip())

    valid_urls = [url for url in urls if is_valid_url(url) and has_parameters(url)]

    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)  

        async def limited_check_url(url):
            async with semaphore:
                await check_url(session, url, encode)

        tasks = [limited_check_url(url) for url in valid_urls]
        await asyncio.gather(*tasks)

    if output_file:
        with open(output_file, 'w') as f:
            for url in valid_urls:
                f.write(url + '\n')

def signal_handler(sig, frame):
    print(Fore.YELLOW + "[+] CTRL+C DETECTED. GRACEFUL SHUTTING DOWN." + Style.RESET_ALL)
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='Input file containing URLs with parameters')
    parser.add_argument('-o', '--output', help='Output file to save results (optional)')
    parser.add_argument('-e', '--encode', action='store_true', help='Encode characters before sending')
    args = parser.parse_args()
    asyncio.run(main(args.input, args.output, args.encode))
