import smtplib
from tkinter import *
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Initialize the model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('t5-base')
tokenizer = T5Tokenizer.from_pretrained('t5-base')

def generate_template(recipient_name, occasion):
    input_text = f"Generate an email template for {occasion} to {recipient_name}"
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    output = model.generate(input_ids, max_length=100)
    template = tokenizer.decode(output[0], skip_special_tokens=True)
    return template

def suggest_email_body(subject):
    input_text = f"Generate an email body for {subject}"
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    output = model.generate(input_ids, max_length=100)
    body = tokenizer.decode(output[0], skip_special_tokens=True)
    return body

def detect_spam(email_body):
    # Simple spam detection using keyword matching
    spam_keywords = ["buy now", "limited time offer", "click here"]
    for keyword in spam_keywords:
        if keyword in email_body.lower():
            return True
    return False

def send_message():
    address_info = address.get()
    email_body_info = email_body.get("1.0", END)
    sender_info = sender_address.get()
    password_info = password.get()

    if detect_spam(email_body_info):
        print("Spam detected! Email not sent.")
        return

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_info, password_info)
    print("Login successful")
    server.sendmail(sender_info, address_info, email_body_info)
    print("Message sent")

    address_entry.delete(0, END)
    email_body.delete("1.0", END)
    password_entry.delete(0, END)
    sender_address_entry.delete(0, END)

def generate_email_template():
    recipient_name = address.get()
    occasion = "birthday"  # hardcoded for simplicity
    template = generate_template(recipient_name, occasion)
    email_body.delete("1.0", END)
    email_body.insert("1.0", template)

def suggest_email_body_text():
    subject = "Hello"  # hardcoded for simplicity
    body = suggest_email_body(subject)
    email_body.delete("1.0", END)
    email_body.insert("1.0", body)

gui = Tk()
gui.geometry("500x600")
gui.title("Advanced Email Sender App")

heading = Label(text="Advanced Email Sender App", bg="yellow", fg="black", font="10", width="500", height="3")
heading.pack()
gui.configure(background="light blue")

sender_address_field = Label(text="Sender's Email :")
sender_address_field.place(x=15, y=70)

sender_address = StringVar()
sender_address_entry = Entry(textvariable=sender_address, width="30")
sender_address_entry.place(x=15, y=100)

sender_password_field = Label(text="Sender's Password :")
sender_password_field.place(x=15, y=140)

password = StringVar()
password_entry = Entry(textvariable=password, width="30", show="*")
password_entry.place(x=15, y=170)

address_field = Label(text="Recipient Email :")
address_field.place(x=15, y=210)

address = StringVar()
address_entry = Entry(textvariable=address, width="30")
address_entry.place(x=15, y=240)

email_body_field = Label(text="Message :")
email_body_field.place(x=15, y=280)

email_body = Text(width="40", height="10")
email_body.place(x=15, y=310)

button_frame = Frame(gui)
button_frame.place(x=15, y=500)

send_button = Button(button_frame, text="Send Message", command=send_message, width="10", height="2", bg="grey")
send_button.pack(side=LEFT)

template_button = Button(button_frame, text="Generate Template", command=generate_email_template, width="15", height="2", bg="grey")
template_button.pack(side=LEFT)

suggest_button = Button(button_frame, text="Suggest Email Body", command=suggest_email_body_text, width="15", height="2", bg="grey")
suggest_button.pack(side=LEFT)

mainloop()