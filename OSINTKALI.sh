import requests
import whois
import socket
import geocoder
import json
import os

def get_ip_info(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        return {"error": f"IP Info Error: {str(e)}"}

def get_whois_info(domain):
    try:
        return whois.whois(domain)
    except Exception as e:
        return {"error": f"WHOIS Error: {str(e)}"}

def get_location_info(name):
    try:
        g = geocoder.osm(name)
        return g.json
    except Exception as e:
        return {"error": f"Location Info Error: {str(e)}"}

def save_results_to_file(results):
    try:
        with open('/results.txt', 'w') as f:
            f.write(json.dumps(results, indent=4))
    except Exception as e:
        print(f"Error saving results to file: {str(e)}")

def main():
    results = {}
    
    # Input selection
    print("Select the type of input for OSINT:")
    print("1. IP Address")
    print("2. Person's Name")
    print("3. Email Address")
    print("4. Organization")
    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        ip = input("Enter IP address: ")
        results['IP Information'] = get_ip_info(ip)

    elif choice == '2':
        name = input("Enter person's name: ")
        results['Location Information'] = get_location_info(name)

    elif choice == '3':
        email = input("Enter email address: ")
        domain = email.split('@')[-1]
        results['Email'] = email
        results['WHOIS Information'] = get_whois_info(domain)

    elif choice == '4':
        organization = input("Enter organization: ")
        results['Organization'] = organization
        # You can add more OSINT queries related to the organization here

    else:
        print("Invalid choice. Please select a valid option.")
        return

    # Save results to file
    save_results_to_file(results)
    print("Results saved to /results.txt")

if __name__ == "__main__":
    main()
