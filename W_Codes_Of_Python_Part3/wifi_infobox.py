from bs4 import BeautifulSoup
import requests
from tkinter import *
from tkinter import messagebox

class WikiScraper:
    def __init__(self):
        self.info_dict = {}
        self.root = Tk()
        self.root.title('Wikipedia Infobox')
        self.entry_str = StringVar()

        self.search_label = LabelFrame(self.root, text="Search: ",
                                      font=('Century Schoolbook L', 17))
        self.search_label.pack(pady=10, padx=10)

        self.user_entry = Entry(self.search_label, textvariable=self.entry_str,
                                font=('Century Schoolbook L', 17))
        self.user_entry.pack(pady=10, padx=10)

        self.button_frame = Frame(self.root)
        self.button_frame.pack(pady=10)

        self.submit_bt = Button(self.button_frame, text='Submit',
                                command=self.scrape_wiki, font=('Century Schoolbook L', 17))
        self.submit_bt.grid(row=0, column=0)

    def error_box(self):
        """
        A function to create a pop-up, in case the code errors out
        """
        messagebox.showerror("Error", "Error fetching data")

    def scrape_wiki(self):
        """
        Function scrapes the infobox lying under the right tags and displays 
        the data obtained from it in a new window
        """
        self.info_dict = {}

        # Modifying the user input to make it suitable for the URL
        entry = self.entry_str.get()
        entry = entry.split()
        query = '_'.join([i.capitalize() for i in entry])
        req = requests.get('https://en.wikipedia.org/wiki/'+query)

        # to check for valid URL
        if req.status_code == 200:
            # for parsing through the html text
            soup = BeautifulSoup(req.text, 'html.parser')

            # Finding text within infobox and storing it in a dictionary
            info_table = soup.find('table', {'class': 'infobox'})

            try:
                for tr in info_table.find_all('tr'):
                    try:
                        if tr.find('th'):
                            self.info_dict[tr.find('th').text] = tr.find('td').text
                    except:
                        pass

            except:
                self.error_box()

            # Creating a pop up window to show the results
            self.popup = Toplevel()
            self.popup.title(query)

            r = 1

            for k, v in self.info_dict.items():
                e1 = Label(self.popup, text=k+" : ", bg='cyan4',
                           font=('Arial', 10, 'bold'))
                e1.grid(row=r, column=1, sticky='nsew')

                e2 = Label(self.popup, text=self.info_dict[k], bg="cyan2", font=(
                    'Arial', 10, 'bold'))
                e2.grid(row=r, column=2, sticky='nsew')

                r += 1
                e3 = Label(self.popup, text='', font=('Arial', 10, 'bold'))
                e3.grid(row=r, sticky='s')
                r += 1

            self.entry_str.set("")
            self.info_dict = {}

        else:
            print('Invalid URL')
            self.error_box()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    scraper = WikiScraper()
    scraper.run()