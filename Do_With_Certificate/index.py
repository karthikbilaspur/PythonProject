import pandas as pd

def read_certificates(file_path):
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None
    except pd.errors.EmptyDataError:
        print("No data in the file. Please check the file contents.")
        return None
    except pd.errors.ParserError:
        print("Error parsing the file. Please check the file format.")
        return None

def search_certificates(df, search_term):
    return df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]

def add_certificate(df, file_path, name, no, email, tenure):
    new_row = pd.DataFrame([[name, no, email, tenure]], columns=['Name', 'No', 'Email', 'Tenure'])
    df = pd.concat([df, new_row])
    df.to_csv(file_path, index=False)

def update_certificate(df, file_path, index, name, no, email, tenure):
    df.loc[index, 'Name'] = name
    df.loc[index, 'No'] = no
    df.loc[index, 'Email'] = email
    df.loc[index, 'Tenure'] = tenure
    df.to_csv(file_path, index=False)

def delete_certificate(df, file_path, index):
    df.drop(index, inplace=True)
    df.to_csv(file_path, index=False)

def main():
    file_path = 'certificates.csv'
    df = read_certificates(file_path)
    
    while True:
        print("\nOptions:")
        print("1. Read certificates")
        print("2. Search certificates")
        print("3. Add certificate")
        print("4. Update certificate")
        print("5. Delete certificate")
        print("6. Quit")
        
        option = input("Choose an option: ")
        
        if option == "1":
            print(df)
        elif option == "2":
            search_term = input("Enter search term: ")
            print(search_certificates(df, search_term))
        elif option == "3":
            name = input("Enter name: ")
            no = input("Enter no: ")
            email = input("Enter email: ")
            tenure = input("Enter tenure: ")
            add_certificate(df, file_path, name, no, email, tenure)
            df = read_certificates(file_path)
        elif option == "4":
            index = int(input("Enter index: "))
            name = input("Enter name: ")
            no = input("Enter no: ")
            email = input("Enter email: ")
            tenure = input("Enter tenure: ")
            update_certificate(df, file_path, index, name, no, email, tenure)
            df = read_certificates(file_path)
        elif option == "5":
            index = int(input("Enter index: "))
            delete_certificate(df, file_path, index)
            df = read_certificates(file_path)
        elif option == "6":
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()