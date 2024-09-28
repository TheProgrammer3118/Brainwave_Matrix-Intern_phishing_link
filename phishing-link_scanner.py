import requests
import logging
import joblib
import re
import socket
import urllib3
from urllib.parse import urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(filename='phishing_scanner.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

model = joblib.load('url_classifier_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

SUSPICIOUS_DOMAINS = ['example-suspicious.com', 'phishing-site.com']

def predict_url_safety(url):
    """Predict if a URL is safe or malicious."""
    url_vector = vectorizer.transform([url])
    prediction = model.predict(url_vector)
    return "SAFE" if prediction[0] == 0 else "MALICIOUS"

def is_malicious_url(url):
    """Perform heuristic checks to identify potentially malicious URLs."""
    if len(url) > 75 or re.search(r'login|secure|account|verify|update|confirm|check', url):
        return True
    return False

def domain_exists(domain):
    """Check if a domain exists by resolving it to an IP address."""
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def check_url(url):
    """Check the URL using both machine learning and heuristic methods."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc or parsed_url.path  

   
    if not domain:
        logging.warning("Invalid URL format: {}".format(url))
        return "DANGEROUS ⚠️ (Invalid URL format)"

    # Check if the domain exists
    if not domain_exists(domain):
        logging.warning(f"{url} is likely malicious because the domain does not exist.")
        return f"Website '{url}' is DANGEROUS (domain does not exist)."

  
    if is_malicious_url(url):
        logging.warning(f"{url} is likely malicious based on heuristics.")
        return "DANGEROUS ⚠️"

    # Check for suspicious domains
    if domain in SUSPICIOUS_DOMAINS:
        logging.warning(f"{url} is considered suspicious.")
        return f"Website '{url}' is SUSPICIOUS (proceed with caution) ⚠️."

    # Check HTTPS first
    https_url = f'https://{domain}'
    try:
        response = requests.get(https_url, timeout=5, verify=False)
        if response.status_code == 200:
            return f"Website '{https_url}' is SAFE."
    except requests.exceptions.RequestException:
        logging.warning(f"{https_url} is not reachable.")

    # If HTTPS fails, check HTTP
    http_url = f'http://{domain}'
    try:
        response = requests.get(http_url, timeout=5, verify=False)
        if response.status_code == 200:
            prediction = predict_url_safety(http_url)
            return f"Website '{http_url}' is {prediction.upper()}."
        else:
            logging.warning(f"{http_url} returned a {response.status_code} status code.")
            return f"Website '{http_url}' is MIGHT BE DANGEROUS (HTTP issue) ⚠️."
    except requests.exceptions.RequestException:
        return f"Website '{http_url}' is DANGEROUS (not reachable)."

def get_ip_address(domain):
    """Retrieve the IP address for a given domain."""
    parsed_domain = urlparse(domain).netloc or urlparse(domain).path
    
    if not domain_exists(parsed_domain):
        return f"DNS cannot be recognized for the domain '{parsed_domain}'. It may not exist."
    
    try:
        ip = socket.gethostbyname(parsed_domain)
        return f"The IP address of '{parsed_domain}' is {ip}."
    except socket.gaierror:
        return f"Could not resolve the domain '{parsed_domain}' due to DNS issues."

def main():
    print("Welcome to the Phishing Link Scanner!")

    while True:
        print("\nMenu:")
        print("1. Check if a website is safe or malicious")
        print("2. Get the IP address of a website")
        print("3. Exit")

        choice = input("Choose an option (1-3): ")

        if choice == '1':
            urls_to_check = input("Enter the URLs to check (comma-separated): ")
            for url in [url.strip() for url in urls_to_check.split(',')]:
                result = check_url(url)
                print(result)
                logging.info(result)

        elif choice == '2':
            domain_to_get_ip = input("Enter the website name to get the IP address: ").strip()
            ip_result = get_ip_address(domain_to_get_ip)
            print(ip_result)
            logging.info(ip_result)

        elif choice == '3':
            print("Exiting the scanner. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
