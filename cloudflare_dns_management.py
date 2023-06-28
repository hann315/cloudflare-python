import requests

# Cloudflare API endpoints
LIST_ZONES_URL = "https://api.cloudflare.com/client/v4/zones"
LIST_RECORDS_URL = "https://api.cloudflare.com/client/v4/zones/{}/dns_records"
ADD_RECORD_URL = "https://api.cloudflare.com/client/v4/zones/{}/dns_records"
DELETE_RECORD_URL = "https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}"

# Cloudflare API credentials
API_KEY = "YOUR_CLOUDFLARE_API_KEY"
EMAIL = "YOUR_CLOUDFLARE_EMAIL"

# Function to list all domains with names
def list_domains():
    response = requests.get(LIST_ZONES_URL, headers={"X-Auth-Email": EMAIL, "X-Auth-Key": API_KEY})
    if response.status_code == 200:
        domains = response.json()["result"]
        print("List of domains:")
        for i, domain in enumerate(domains, start=1):
            name = domain["name"]
            print(f"{i}. Domain Name: {name}")
        print()
    else:
        print("Failed to retrieve domain list. Status code:", response.status_code)
        print("Response:", response.text)

# Function to retrieve the domain ID based on the domain name
def get_domain_id(domain_name):
    response = requests.get(LIST_ZONES_URL, headers={"X-Auth-Email": EMAIL, "X-Auth-Key": API_KEY})
    if response.status_code == 200:
        domains = response.json()["result"]
        for domain in domains:
            if domain["name"] == domain_name:
                return domain["id"]
    else:
        print("Failed to retrieve domain list. Status code:", response.status_code)
        print("Response:", response.text)
    return None

# Function to list all DNS records for a specific domain with names
def list_dns_records(domain_name):
    zone_id = get_domain_id(domain_name)
    if zone_id:
        url = LIST_RECORDS_URL.format(zone_id)
        response = requests.get(url, headers={"X-Auth-Email": EMAIL, "X-Auth-Key": API_KEY})
        if response.status_code == 200:
            records = response.json()["result"]
            print()
            print(f"List of DNS records for domain '{domain_name}':")
            for record in records:
                type = record["type"]
                name = record["name"]
                content = record["content"]
                ttl = record["ttl"]
                id = record["id"]

                # Change TTL label to proper value for display
                if ttl == 1:
                    ttl = "Auto"
                elif ttl == 120:
                    ttl = "2 minutes"
                elif ttl == 300:
                    ttl = "5 minutes"
                elif ttl == 600:
                    ttl = "10 minutes"
                elif ttl == 900:
                    ttl = "15 minutes"
                elif ttl == 1800:
                    ttl = "30 minutes"
                elif ttl == 3600:
                    ttl = "1 hour"
                elif ttl == 7200:
                    ttl = "2 hours"
                elif ttl == 18000:
                    ttl = "5 hours"
                elif ttl == 43200:
                    ttl = "12 hours"
                elif ttl == 86400:
                    ttl = "1 day"

                print()
                print(f"Name: {name}")
                print(f"Type: {type}")
                print(f"IP Address: {content}")
                print(f"TTL: {ttl}")
                print(f"ID: {id}")
                print()
        else:
            print("Failed to retrieve DNS records. Status code:", response.status_code)
            print("Response:", response.text)
    else:
        print(f"Domain '{domain_name}' not found.")

# Function to add a DNS record
def add_dns_record():
    domain_name = input("Enter the domain name where you want to add the DNS record: ")
    zone_id = get_domain_id(domain_name)
    if zone_id:
        record_name = input("Enter the name of the DNS record (e.g., example.com or subdomain.example.com): ")
        print()
        
        # Provide options for DNS record type
        print("DNS record types:")
        print("1. A")
        print("2. AAAA")
        print("3. CNAME")
        print("4. MX")
        print("5. TXT")
        print("6. SRV")
        print("7. NS")
        print("8. SOA")
        print("9. PTR")
        
        # Prompt the user for the DNS record type until a valid choice is entered
        while True:
            record_type_choice = input("Enter the number corresponding to the DNS record type: ")
            
            # Map the choice to the actual DNS record type
            record_type_mapping = {
                "1": "A",
                "2": "AAAA",
                "3": "CNAME",
                "4": "MX",
                "5": "TXT",
                "6": "SRV",
                "7": "NS",
                "8": "SOA",
                "9": "PTR"
            }
            record_type = record_type_mapping.get(record_type_choice)
            
            if record_type:
                break
            else:
                print("Invalid DNS record type. Please try again.")
                print()
        
        print()
        record_content = input("Enter the content for the DNS record (e.g., IP address or target value): ")
        
        # Provide options for proxy status
        print()
        print("Proxy status options:")
        print("1. DNS Only")
        print("2. Proxied")
        
        # Prompt the user for the proxy status until a valid choice is entered
        while True:
            proxy_status_choice = input("Enter the number corresponding to the Proxy Status: ")
            
            # Map the choice to the actual proxy status
            proxy_status_mapping = {
                "1": "DNS only",
                "2": "Proxied"
            }
            proxy_status = proxy_status_mapping.get(proxy_status_choice)
            
            if proxy_status:
                break
            else:
                print("Invalid Proxy Status. Please try again.")
                print()
        
        # Set TTL to "auto" if proxy status is "Proxied"
        if proxy_status == "Proxied":
            record_ttl = "1"
        else:
            # Provide options for TTL
            ttl_options = {
                "1": 60,            # 1 minute
                "2": 120,           # 2 minutes
                "3": 300,           # 5 minutes
                "4": 600,           # 10 minutes
                "5": 900,           # 15 minutes
                "6": 1800,          # 30 minutes
                "7": 3600,          # 1 hour
                "8": 7200,          # 2 hours
                "9": 18000,         # 5 hours
                "10": 43200,        # 12 hours
                "11": 86400         # 1 day
            }
            
            while True:
                print()
                print("TTL options (in seconds):")
                print("1. 1 minute")
                print("2. 2 minutes")
                print("3. 5 minutes")
                print("4. 10 minutes")
                print("5. 15 minutes")
                print("6. 30 minutes")
                print("7. 1 hour")
                print("8. 2 hours")
                print("9. 5 hours")
                print("10. 12 hours")
                print("11. 1 day")
                ttl_choice = input("Enter the number corresponding to the TTL option: ")
                
                record_ttl = ttl_options.get(ttl_choice)
                
                if record_ttl:
                    break
                else:
                    print("Invalid TTL option. Please try again.")
        
        data = {
            "type": record_type,
            "name": record_name,
            "content": record_content,
            "ttl": record_ttl,
            "proxied": proxy_status == "Proxied"
        }

        url = ADD_RECORD_URL.format(zone_id)
        response = requests.post(url, headers={"X-Auth-Email": EMAIL, "X-Auth-Key": API_KEY, "Content-Type": "application/json"}, json=data)
        if response.status_code == 200:
            print()
            print("DNS record added successfully.")
        else:
            print()
            print("Failed to add DNS record. Status code:", response.status_code)
            print("Response:", response.text)
    else:
        print()
        print(f"Domain '{domain_name}' not found.")


# Function to delete a DNS record by name
def delete_dns_record(domain_name):
    zone_id = get_domain_id(domain_name)
    if zone_id:
        list_dns_records(domain_name)
        record_name = input("Enter the name of the DNS record you want to delete: ")
        print()
        url = LIST_RECORDS_URL.format(zone_id)
        response = requests.get(url, headers={"X-Auth-Email": EMAIL, "X-Auth-Key": API_KEY})
        if response.status_code == 200:
            records = response.json()["result"]
            matching_records = [record for record in records if record["name"] == record_name]
            if matching_records:
                if len(matching_records) > 1:
                    print(f"Found multiple DNS records with name '{record_name}'. Please provide the record ID to delete.")
                    print()
                    record_id = input("Enter the record ID: ")
                    print()
                    confirm = input(f"Are you sure you want to delete DNS record '{record_name}' with ID '{record_id}'? (y/n): ")
                    if confirm.lower() == "y":
                        delete_url = DELETE_RECORD_URL.format(zone_id, record_id)
                        delete_response = requests.delete(delete_url, headers={"X-Auth-Email": EMAIL, "X-Auth-Key": API_KEY})
                        if delete_response.status_code == 200:
                            print()
                            print("DNS record deleted successfully.")
                        else:
                            print()
                            print("Failed to delete DNS record. Status code:", delete_response.status_code)
                            print("Response:", delete_response.text)
                    else:
                        print()
                        print("DNS record deletion canceled.")
                else:
                    record_id = matching_records[0]["id"]
                    print(f"Found DNS record with name '{record_name}' and ID '{record_id}'.")
                    print()
                    confirm = input(f"Are you sure you want to delete DNS record '{record_name}'? (y/n): ")
                    if confirm.lower() == "y":
                        delete_url = DELETE_RECORD_URL.format(zone_id, record_id)
                        delete_response = requests.delete(delete_url, headers={"X-Auth-Email": EMAIL, "X-Auth-Key": API_KEY})
                        if delete_response.status_code == 200:
                            print()
                            print("DNS record deleted successfully.")
                        else:
                            print()
                            print("Failed to delete DNS record. Status code:", delete_response.status_code)
                            print("Response:", delete_response.text)
                    else:
                        print()
                        print("DNS record deletion canceled.")
            else:
                print()
                print(f"No DNS record found with name '{record_name}'.")
        else:
            print()
            print("Failed to retrieve DNS records. Status code:", response.status_code)
            print("Response:", response.text)
    else:
        print()
        print(f"Domain '{domain_name}' not found.")

def update_dns_record(domain_name):
    zone_id = get_domain_id(domain_name)
    if zone_id:
        list_dns_records(domain_name)
        record_name = input("Enter the name of the DNS record you want to update: ")
        url = LIST_RECORDS_URL.format(zone_id)
        response = requests.get(url, headers={"X-Auth-Email": EMAIL, "X-Auth-Key": API_KEY})
        if response.status_code == 200:
            records = response.json()["result"]
            matching_records = [record for record in records if record["name"] == record_name]
            if matching_records:
                if len(matching_records) > 1:
                    print(f"Found multiple DNS records with name '{record_name}'. Please provide the record ID to update.")
                    record_id = input("Enter the record ID: ")
                else:
                    record_id = matching_records[0]["id"]
                    print(f"Found DNS record with name '{record_name}' and ID '{record_id}'.")

                print()
                print("DNS record types:")
                print("1. A")
                print("2. AAAA")
                print("3. CNAME")
                print("4. MX")
                print("5. TXT")
                print("6. SRV")
                print("7. NS")
                print("8. SOA")
                print("9. PTR")

                record_type = input("Enter the new type of DNS record (1-9): ")
                record_type_mapping = {
                    "1": "A",
                    "2": "AAAA",
                    "3": "CNAME",
                    "4": "MX",
                    "5": "TXT",
                    "6": "SRV",
                    "7": "NS",
                    "8": "SOA",
                    "9": "PTR"
                }

                print()
                record_content = input("Enter the new content for the DNS record (e.g., IP address or target value): ")

                # Provide options for proxy status
                print()
                print("Proxy status options:")
                print("1. DNS Only")
                print("2. Proxied")

                # Prompt the user for the proxy status until a valid choice is entered
                while True:
                    proxy_status_choice = input("Enter the number corresponding to the Proxy Status: ")

                    # Map the choice to the actual proxy status
                    proxy_status_mapping = {
                        "1": "DNS only",
                        "2": "Proxied"
                    }
                    proxy_status = proxy_status_mapping.get(proxy_status_choice)

                    if proxy_status:
                        break
                    else:
                        print("Invalid Proxy Status. Please try again.")
                
                if proxy_status == "Proxied":
                    # Set TTL to Auto for Proxied records
                    record_ttl = 1
                else:
                    print()
                    print("TTL options:")
                    print("1. 1 minute")
                    print("2. 2 minutes")
                    print("3. 5 minutes")
                    print("4. 10 minutes")
                    print("5. 15 minutes")
                    print("6. 30 minutes")
                    print("7. 1 hour")
                    print("8. 2 hours")
                    print("9. 5 hours")
                    print("10. 12 hours")
                    print("11. 1 day")
                    
                    # Prompt the user for the TTL option until a valid choice is entered
                    while True:
                        ttl_choice = input("Enter the number corresponding to the TTL option: ")
                        ttl_mapping = {
                            "1": 60,              # 1 minute
                            "2": 120,             # 2 minutes
                            "3": 300,             # 5 minutes
                            "4": 600,             # 10 minutes
                            "5": 900,             # 15 minutes
                            "6": 1800,            # 30 minutes
                            "7": 3600,            # 1 hour
                            "8": 7200,            # 2 hours
                            "9": 18000,           # 5 hours
                            "10": 43200,          # 12 hours
                            "11": 86400           # 1 day
                        }
                        record_ttl = ttl_mapping.get(ttl_choice)
                        if record_ttl:
                            break
                        else:
                            print("Invalid TTL option. Please try again.")

                data = {
                    "type": record_type_mapping.get(record_type),
                    "name": record_name,
                    "content": record_content,
                    "ttl": record_ttl,
                    "proxied": proxy_status == "Proxied"
                }

                update_url = DELETE_RECORD_URL.format(zone_id, record_id)
                update_response = requests.put(update_url, headers={"X-Auth-Email": EMAIL, "X-Auth-Key": API_KEY, "Content-Type": "application/json"}, json=data)
                if update_response.status_code == 200:
                    print()
                    print("DNS record updated successfully.")
                else:
                    print()
                    print("Failed to update DNS record. Status code:", update_response.status_code)
                    print("Response:", update_response.text)
            else:
                print()
                print(f"No DNS record found with name '{record_name}'.")
        else:
            print()
            print("Failed to retrieve DNS records. Status code:", response.status_code)
            print("Response:", response.text)
    else:
        print()
        print(f"No domain found with name '{domain_name}'.")

# Main program
print("Cloudflare DNS Management")

while True:
    print()
    print("Options:")
    print("1. List domains")
    print("2. List DNS records for a domain")
    print("3. Add a DNS record")
    print("4. Update a DNS record")
    print("5. Delete a DNS record")
    print("6. Quit")

    print()
    
    choice = input("Enter your choice (1-6): ")
    print()

    if choice == "1":
        list_domains()
        while True:
            print()
            print("Enter 'R' to repeat this option")
            print("Enter 'M' to go back to the main menu")
            print()
            user_choice = input("Enter your choice (R/M): ")
            print()
            if user_choice.lower() == 'r':
                list_domains()
            elif user_choice.lower() == 'm':
                break
            else:
                print()
                print("Invalid choice. Please select 'R' or 'M'.")
    elif choice == "2":
        list_domains()
        domain_name = input("Enter the domain name to list DNS records: ")
        list_dns_records(domain_name)
        while True:
            print()
            print("Enter 'R' to repeat this option")
            print("Enter 'M' to go back to the main menu")
            print()
            user_choice = input("Enter your choice (R/M): ")
            print()
            if user_choice.lower() == 'r':
                list_domains()
                domain_name = input("Enter the domain name to list DNS records: ")
                list_dns_records(domain_name)
            elif user_choice.lower() == 'm':
                break
            else:
                print()
                print("Invalid choice. Please select 'R' or 'M'.")
    elif choice == "3":
        list_domains()
        add_dns_record()
        while True:
            print()
            print("Enter 'R' to repeat this option")
            print("Enter 'M' to go back to the main menu")
            print()
            user_choice = input("Enter your choice (R/M): ")
            print()
            if user_choice.lower() == 'r':
                list_domains()
                add_dns_record()
            elif user_choice.lower() == 'm':
                break
            else:
                print()
                print("Invalid choice. Please select 'R' or 'M'.")
    elif choice == "4":
        list_domains()
        domain_name = input("Enter the domain name to update DNS record: ")
        update_dns_record(domain_name)
        while True:
            print()
            print("Enter 'R' to repeat this option")
            print("Enter 'M' to go back to the main menu")
            print()
            user_choice = input("Enter your choice (R/M): ")
            print()
            if user_choice.lower() == 'r':
                list_domains()
                domain_name = input("Enter the domain name to update DNS record: ")
                update_dns_record(domain_name)
            elif user_choice.lower() == 'm':
                break
            else:
                print()
                print("Invalid choice. Please select 'R' or 'M'.")
    elif choice == "5":
        list_domains()
        domain_name = input("Enter the domain name to delete DNS record: ")
        delete_dns_record(domain_name)
        while True:
            print()
            print("Enter 'R' to repeat this option")
            print("Enter 'M' to go back to the main menu")
            print()
            user_choice = input("Enter your choice (R/M): ")
            print()
            if user_choice.lower() == 'r':
                list_domains()
                domain_name = input("Enter the domain name to delete DNS record: ")
                delete_dns_record(domain_name)
            elif user_choice.lower() == 'm':
                break
            else:
                print()
                print("Invalid choice. Please select 'R' or 'M'.")
    elif choice == "6":
        print("Goodbye!")
        print()
        break
    else:
        print("Invalid choice. Please select a valid option.")
        