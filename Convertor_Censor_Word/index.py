from profanity_check import predict, predict_prob

def detect_censor_words(text):
    prediction = predict([text])
    probability = predict_prob([text])
    if prediction[0] == 1:
        print(f"Censor word detected with probability: {probability[0]}")
        return "*****"
    else:
        print("No censor words detected")
        return text

text = input("Enter text to check for censor words: ")
print(detect_censor_words(text))