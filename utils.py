from urllib.parse import urlparse

def extract_program_id(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.rstrip('/').split('/')
    return path_parts[-1]
