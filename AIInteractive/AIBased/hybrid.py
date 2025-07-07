import dialogflow
import random

def detect_intent(text, project_id, session_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def chapter_1(project_id, session_id):
    print("You arrive at the planet and begin to scan its surface.")
    print("You discover a strange structure in the center of the planet, emitting a unique energy signature.")
    print("As you approach the structure, in the center of the planet, you're contacted by an unknown entity who claims to be the guardian of the planet.")
    
    choice = input("Do you (A) heed the warning and leave the planet or (B) ignore the warning and investigate the structure further? ")
    
    if choice.lower() == "a":
        branch_1_warning(project_id, session_id)
    elif choice.lower() == "b":
        branch_2_ruins(project_id, session_id)
    else:
        print("Invalid choice. Please try again.")
        chapter_1(project_id, session_id)

def branch_1_warning(project_id, session_id):
    print("You heed the warning and leave the planet.")
    chapter_2_warning(project_id, session_id)

def branch_2_ruins(project_id, session_id):
    print("You ignore the warning and enter the structure.")
    print("You discover ancient ruins filled with strange artifacts and technology.")
    print("As you explore the ruins, you stumble upon a powerful device that could change the course of human history.")
    
    choice = input("Do you (A) activate the device and harness its power or (B) study the device further before making a decision? ")
    
    if choice.lower() == "a":
        branch_2_activate(project_id, session_id)
    elif choice.lower() == "b":
        branch_2_study(project_id, session_id)
    else:
        print("Invalid choice. Please try again.")
        branch_2_ruins(project_id, session_id)

def chapter_2_warning(project_id, session_id):
    print("You encounter a group of hostile aliens who are trying to claim the planet for themselves.")
    choice = input("Do you (A) fight the aliens or (B) flee? ")
    
    if choice.lower() == "a":
        print("You defend yourself and defeat the aliens.")
        user_input = "I defeated the aliens"
        response = detect_intent(user_input, project_id, session_id)
        print("AI:", response.fulfillment_text)
    elif choice.lower() == "b":
        print("You flee the planet and escape the aliens.")
        user_input = "I fled the planet"
        response = detect_intent(user_input, project_id, session_id)
        print("AI:", response.fulfillment_text)
    else:
        print("Invalid choice. Please try again.")
        chapter_2_warning(project_id, session_id)

def branch_2_activate(project_id, session_id):
    print("You activate the device and experience a surge of power.")
    print("However, you also attract the attention of powerful forces that seek to exploit the device's power.")
    user_input = "I activated the device"
    response = detect_intent(user_input, project_id, session_id)
    print("AI:", response.fulfillment_text)

def branch_2_study(project_id, session_id):
    print("You study the device further and gain a deeper understanding of its capabilities and limitations.")
    print("You have to decide whether to use the device or keep it hidden from the rest of the galaxy.")
    user_input = "I studied the device"
    response = detect_intent(user_input, project_id, session_id)
    print("AI:", response.fulfillment_text)

def main():
    project_id = "your-project-id"
    session_id = "your-session-id"
    
    chapter_1(project_id, session_id)

if __name__ == "__main__":
    main()