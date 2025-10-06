import getpass
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
from datetime import datetime
import json
import os

# Xpaths
xLinkedin = {
    'xEmail': '//input[@name="session_key"]',
    'xPass': '//input[@name="session_password"]',
    'xLogin': '//button[contains(.,"Sign in")]',
    'xProfile': '//div[@data-control-name="identity_welcome_message"]',
    'xCertName': '//input[@placeholder="Ex: Microsoft certified network associate security"]',
    'xCertOrg': '//input[@placeholder="Ex: Microsoft"]',
    'xCredId': '//input[@id="single-line-text-form-component-profileEditFormElement-CERTIFICATION-profileCertification-ACoAADI-i-oBZzsiExXBGep7oC4p5cgLkd4v7kE-1-licenseNumber"]',
    'xCredUrl': '//input[@id="single-line-text-form-component-profileEditFormElement-CERTIFICATION-profileCertification-ACoAADI-i-oBZzsiExXBGep7oC4p5cgLkd4v7kE-1-url"]',
    'xSave': '//button[contains(.,"Save")]'
}


class Certificate:
    def __init__(self, name, issuer, date):
        self.name = name
        self.issuer = issuer
        self.date = date


class CertificateManager:
    def __init__(self):
        self.certificates = []
        self.load_certificates()

    def add_certificate(self, name, issuer, date):
        new_certificate = Certificate(name, issuer, date)
        self.certificates.append(new_certificate)
        self.save_certificates()
        print(f"Certificate '{name}' added successfully.")

    def delete_certificate(self, name):
        for certificate in self.certificates:
            if certificate.name == name:
                self.certificates.remove(certificate)
                self.save_certificates()
                print(f"Certificate '{name}' deleted successfully.")
                return
        print(f"Certificate '{name}' not found.")

    def view_certificates(self):
        if not self.certificates:
            print("No certificates found.")
        else:
            certificate_data = []
            for certificate in self.certificates:
                certificate_data.append({
                    "Name": certificate.name,
                    "Issuer": certificate.issuer,
                    "Date": certificate.date
                })
            df = pd.DataFrame(certificate_data)
            print(df)

    def save_certificates(self):
        certificate_data = []
        for certificate in self.certificates:
            certificate_data.append({
                "name": certificate.name,
                "issuer": certificate.issuer,
                "date": certificate.date
            })
        with open("certificates.json", "w") as f:
            json.dump(certificate_data, f)

    def load_certificates(self):
        if os.path.exists("certificates.json"):
            with open("certificates.json", "r") as f:
                certificate_data = json.load(f)
            for data in certificate_data:
                self.certificates.append(Certificate(data["name"], data["issuer"], data["date"]))

    def add_to_linkedin(self):
        email = input('Enter your linkedin email: ')
        password = getpass.getpass('Password: ')

        opt = webdriver.ChromeOptions()
        opt.add_argument('--disable-gpu')
        opt.add_argument('--headless')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=opt)
        driver.get('https://linkedin.com')

        emailField = driver.find_element(By.XPATH, xLinkedin['xEmail'])
        emailField.send_keys(email)
        passwordField = driver.find_element(By.XPATH, xLinkedin['xPass'])
        passwordField.send_keys(password)

        submitBtn = driver.find_element(By.XPATH, xLinkedin['xLogin'])
        submitBtn.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, xLinkedin['xProfile'])))

        for certificate in self.certificates:
            currentUrl = driver.current_url
            driver.get(currentUrl+'edit/forms/certification/new/')
            nameInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, xLinkedin['xCertName'])))
            nameInput.send_keys(certificate.name)
            sleep(1)
            orgInput = driver.find_element(By.XPATH, xLinkedin['xCertOrg'])
            orgInput.send_keys(certificate.issuer)
            sleep(3)
            orgInput.send_keys(Keys.ARROW_DOWN + Keys.ENTER)
            credIdInput = driver.find_element(By.XPATH, xLinkedin['xCredId'])
            credIdInput.send_keys("N/A")
            credUrlInput = driver.find_element(By.XPATH, xLinkedin['xCredUrl'])
            credUrlInput.send_keys("N/A")
            driver.find_element(By.XPATH, xLinkedin['xSave']).click()
            print(f"Added {certificate.name} to LinkedIn")
        driver.close()


def main():
    manager = CertificateManager()

    while True:
        print("LinkedIn Certificate Manager")
        print("1. Add Certificate")
        print("2. Delete Certificate")
        print("3. View Certificates")
        print("4. Add Certificates to LinkedIn")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter certificate name: ")
            issuer = input("Enter certificate issuer: ")
            date = input("Enter certificate date (YYYY-MM-DD): ")
            try:
                datetime.strptime(date, "%Y-%m-%d")
                manager.add_certificate(name, issuer, date)
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        elif choice == "2":
            name = input("Enter certificate name: ")
            manager.delete_certificate(name)
        elif choice == "3":
            manager.view_certificates()
        elif choice == "4":
            manager.add_to_linkedin()
        elif choice == "5":
            break
        else:
            print("Invalid option. Please choose a valid option.")


if __name__ == "__main__":
    main()