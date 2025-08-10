import dns.resolver

def dns_verifier(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        for rdata in answers:
            print(f"{domain} {record_type} record: {rdata}")
    except dns.resolver.NoAnswer:
        print(f"No {record_type} record found for {domain}")
    except dns.resolver.NXDOMAIN:
        print(f"Domain {domain} does not exist")
    except dns.resolver.YXDOMAIN:
        print(f"Domain {domain} is too long")
    except Exception as e:
        print(f"Error: {e}")

def get_record_types():
    record_types = ["A", "MX", "NS", "SOA", "TXT", "PTR", "CNAME"]
    return record_types

def main():
    print("DNS Verifier Tool")
    print("------------------")

    domain = input("Enter domain: ")
    print("Available record types:")
    record_types = get_record_types()
    for i, record_type in enumerate(record_types):
        print(f"{i+1}. {record_type}")

    choice = input("Enter the number of the record type (or 'all' for all record types): ")
    if choice.lower() == "all":
        for record_type in record_types:
            print(f"\nVerifying {record_type} records...")
            dns_verifier(domain, record_type)
    else:
        try:
            choice = int(choice)
            if 1 <= choice <= len(record_types):
                record_type = record_types[choice - 1]
                dns_verifier(domain, record_type)
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid input")

if __name__ == "__main__":
    main()