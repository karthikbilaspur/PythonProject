import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup as soup
import requests
import webbrowser
import string
import random

class SignUpForm:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Sign Up Form")

        # Create form fields
        tk.Label(self.window, text="Name").grid(row=0, column=0)
        tk.Label(self.window, text="Toll Amount").grid(row=1, column=0)

        self.name_entry = tk.Entry(self.window)
        self.toll_amount_entry = tk.Entry(self.window)

        self.name_entry.grid(row=0, column=1)
        self.toll_amount_entry.grid(row=1, column=1)

        tk.Button(self.window, text="Generate Credentials", command=self.generate_credentials).grid(row=2, column=1)

    def generate_names(self):
        names = "Mario Speedwagon, Petey Cruiser, Anna Sthesia,  Molive, Anna Mull, Gail Forcewind, Paige Turner, Bob Frapples, Walter Melon, Nick R. Bocker, Barb Ackue, Buck Kinnear, Greta Life, Ira Membrit, Shonda Leer, Brock Lee, Maya Didas, Rick O'Shea, Monty Carlo, Sal Monella, Sue Vaneer, Cliff Hanger, Barb Dwyer, Terry Aki, Cory Ander, Robin Banks, Jimmy Changa, Barry Wine, Wilma Mumduya, Buster Hyman, Poppa Cherry, Zack Lee, Don Stairs, Saul T. Balls, Peter Pants, Hal Appeno, Otto Matic, Moe Fugga, Graham Cracker, Tom Foolery, Al Dente, Bud Wiser, Polly Tech, Holly Graham, Frank N. Stein, Cam L. Toe, Pat Agonia, Tara Zona, Barry Cade, Phil Anthropist, Marvin Gardens, Phil Harmonic, Arty Ficial, Will Power, Donatella Nobatti, Juan Annatoo, Stew Gots, Anna Rexia, Bill Emia, Curt N. Call, Max Emum, Minnie Mum, Bill Yerds, Hap E. Birthday, Matt Innae, Polly Science, Tara Misu, Ed U. Cation, Gerry Atric, Kerry Oaky, Midge Itz, Gabe Lackmen, Mary Christmas, Dan Druff, Jim Nasium, Angie O. Plasty, Ella Vator, Sal Vidge, Bart Ender, Artie Choke, Hans Olo, Marge Arin, Hugh Briss, Gene Poole, Ty Tanic, Manuel Labor, Lynn Guini, Claire Voyant, Peg Leg, Jack E. Sack, Marty Graw, Ash Wednesday, Olive Yu, Gene Jacket, Tom Atoe, Doug Out, Sharon Needles, Beau Tie, Serj Protector, Marcus Down, Warren Peace, Bud Jet, Barney Cull, Marion Gaze, Eric Shun, Mal Practice, Ed Itorial, Rick Shaw, Paul Issy, Ben Effit, Kat E. Gory, Justin Case, Louie Z. Ana, Aaron Ottix, Ty Ballgame, Anne Fibbiyon, Barry Cuda, John Withawind, Joe Thyme, Mary Goround ,Marge Arita, Frank Senbeans, Bill Dabear, Ray Zindaroof, Adam Zapple, Lewis N. Clark, Matt Schtick, Sue Shee, Chris P. Bacon, Doug Lee Duckling, Mason Protesters, Sil Antro, Cal Orie, Sara Bellum, Al Acart, Marv Ellis, Evan Shlee, Terry Bull, Mort Ission, Mark Ette, Ken Tucky, Louis Ville, Colin Oscopy, Fred Attchini, Al Fredo, Penny Tration, Reed Iculous, Chip Zinsalsa, Matt Uhrafact, Jack Dup, Mike Roscope, Lou Sinclark, Faye Daway, Javy Cad,, Tom Ollie, Sam Buca, Phil Anderer, Sam Owen, Mary Achi, Ray Cyst, Curtis E. Flush, Holland Oats, Helen Highwater, Eddy Kitt, Al Toesacks, Sir Kim Scision, Elle Bowdrop, Yu Tube, Ellis Dee, Anna Lytics, Sara Bellum, Penny Trate, Phil Erup, Jenna Side, Mary Nara, Mick Donalds, Amber Alert, Vic Tory, Bobby Pin, Dom Inate, Hugh Miliation, Christian Mingle, Juan Soponatime, Dante Sinferno, Ed Zupp, Sarah Yevo, Jess Thetip, Arthur Itis, Faye Sbook, Carrie R. Pigeon, Rachel Slurs, Ty Pryder, Cole Slaw, Pat Ernity, Deb Utant, Luke Warm, Travis Tee, Clara Fication, Paul Itician, Deb Utant, Moe Thegrass, Carol Sell, Scott Schtape, Cody Pendant, Frank Furter, Barry Dalive, Mort Adella, Ray Diation, Mack Adamia, Farrah Moan, Theo Retical, Eda Torial, Mae Nayse, Bella Ruse, Yuri thra, Tucker Doubt, Cara Larm, Abel Body, Sal Ami, Colin Derr, Cathy Derr, Colin Scopy, Mel Anoma, Adam Up, Lou Zing, Mark Key, Sven Gineer, Mick Rib, Benny Ficial, Genie Inabottle, Gene Therapy, Reggie Stration, Lou Ow, Lance Dorporal, Lou Tenant, Nick Knack, Patty Whack, Reuben Sandwich, Hugo Slavia, Aaron Spacemuseum, Petey Atricks, Dan Delion, Terry Torial, Cal Q. Later, Jen Trification, Indy Nile, Ray Volver, Minnie Strone, Gustav Wind, Paul Samic, Vinny Gret, , oyce Tick, Cliff Diver, Earl E. Riser, Cooke Edoh, Jen Youfelct, Reanne Carnation, Paul Misunday, Chris P. Cream, Gio Metric, Caire Innet, Marsha Mello, Manny Petty, Val Adictorian, Lucy Tania, Jaques Amole"
        names = names.split(", ")
        return random.choices(names)[0]

    def generate_password(self, length: int) -> str:
        letters = string.ascii_letters
        numbers = string.digits
        punctuations = "!#$%&()*+-/<=>?@[]^_{|}~"
        printable = f'{letters}{numbers}{punctuations}'
        printable = list(printable)
        random.shuffle(printable)
        temp_password = ''.join(random.choices(printable, k=length))
        return temp_password

    def generate_email_id_and_link(self):
        headers = {
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
        }
        response = requests.get('https://10minutemail.net/', headers=headers)
        ses = str(response.cookies).split(",")[2].split(" ")[2]
        response = requests.get('https://10minutemail.net/address.api.php?' + ses)
        page_soup = soup(response.content, "html.parser")
        cookies = str(page_soup).split('"')
        permalink = cookies[cookies.index("url") + 2]
        permalink = permalink.replace(
            '\/', "/") + "?key=" + cookies[cookies.index("key") + 2]
        temp_email_id = cookies[cookies.index("mail_get_mail") + 2]
        return temp_email_id, permalink

    def generate_credentials(self):
        name = self.name_entry.get()
        toll_amount = self.toll_amount_entry.get()

        if name and toll_amount:
            try:
                toll_amount = float(toll_amount)
                random_password = self.generate_password(16)
                random_name = self.generate_names()
                temporary_emailID, temp_link = self.generate_email_id_and_link()

                # Display generated credentials
                credentials_window = tk.Toplevel(self.window)
                credentials_window.title("Generated Credentials")

                tk.Label(credentials_window, text="Name:").grid(row=0, column=0)
                tk.Label(credentials_window, text=random_name).grid(row=0, column=1)

                tk.Label(credentials_window, text="Password:").grid(row=1, column=0)
                tk.Label(credentials_window, text=random_password).grid(row=1, column=1)

                tk.Label(credentials_window, text="Email ID:").grid(row=2, column=0)
                tk.Label(credentials_window, text=temporary_emailID).grid(row=2, column=1)

                tk.Label(credentials_window, text="Link:").grid(row=3, column=0)
                tk.Label(credentials_window, text=temp_link).grid(row=3, column=1)

                # Save credentials to file
                with open("credentials.txt", "w") as f:
                    f.write(f"Name: {random_name}\n")
                    f.write(f"Password: {random_password}\n")
                    f.write(f"Email ID: {temporary_emailID}\n")
                    f.write(f"Link: {temp_link}\n")

                messagebox.showinfo("Success", f"Sign up successful! Toll amount: ₹{toll_amount}")
            except ValueError:
                messagebox.showerror("Error", "Invalid toll amount")
        else:
            messagebox.showerror("Error", "Please fill all fields")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    form = SignUpForm()
    form.run()