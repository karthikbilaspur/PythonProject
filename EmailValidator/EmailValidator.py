import re
import dns.resolver
import smtplib

class EmailValidator:
    def __init__(self):
        self.regex_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def validate_email_format(self, email):
        if re.match(self.regex_pattern, email):
            return True
        return False

    def validate_email_domain(self, email):
        domain = email.split('@')[1]
        try:
            dns.resolver.resolve(domain, 'MX')
            return True
        except dns.resolver.NoAnswer:
            try:
                dns.resolver.resolve(domain, 'A')
                return True
            except dns.resolver.NoAnswer:
                return False
        except dns.resolver.NXDOMAIN:
            return False

    def validate_email_smtp(self, email):
        domain = email.split('@')[1]
        try:
            records = dns.resolver.resolve(domain, 'MX')
            mx_record = records[0].exchange
            mx_record = str(mx_record)
            server = smtplib.SMTP()
            server.connect(mx_record)
            server.helo(server.local_hostname)
            server.mail('test@example.com')
            code, message = server.rcpt(email)
            server.quit()
            if code == 250:
                return True
            else:
                return False
        except Exception as e:
            return False

    def validate_email(self, email):
        if self.validate_email_format(email) and self.validate_email_domain(email):
            return self.validate_email_smtp(email)
        return False

# Example usage
if __name__ == '__main__':
    email_validator = EmailValidator()
    email = 'example@example.com'
    if email_validator.validate_email(email):
        print(f'{email} is a valid email address.')
    else:
        print(f'{email} is not a valid email address.')