import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample training data (questions and their intents)
training_data = [
    ("Hi", "greeting"),
    ("Hello", "greeting"),
    ("How are you?", "greeting"),
    ("What's your name?", "name_query"),
    ("Tell me your name", "name_query"),
    ("How Old are you?", "age_query"),
    ("Where are you from?", "location_query"),
    ("Are you married?","martial_status_query"),
    ("Bye", "goodbye"),
    ("Goodbye", "goodbye"),
    ("Thanks", "thanks"),
    ("Thank you", "thanks"),
    ("What time is it?", "time_query"),
    ("Can you tell me the time?", "time_query"),
]

# Training labels (intent categories)
training_labels = [intent for _, intent in training_data]

# Prepare the chatbot responses for intents
responses = {
    "greeting": ["Hello! How can I help you?", "Hi! How can I assist you today?"],
    "name_query": ["I'm your smart assistant!", "My name is Chatbot, your virtual assistant!"],
    "goodbye": ["Goodbye! Have a great day!", "Bye! Take care!"],
    "thanks": ["You're welcome!", "No problem! Happy to help!"],
    "time_query": ["I'm sorry, I can't tell the time right now.", "I don't have access to a clock at the moment."],
    "default": ["I'm not sure how to respond to that.", "Can you please clarify?"],
    "age_query": ["I am 52 Years old."],
    "location_query": ["I am from India."],
    "martial_status_query":["I am Single"],
}

# Preprocess user input
def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenize and convert to lowercase
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    return ' '.join(filtered_tokens)

# Train the intent classifier
def train_classifier(training_data, training_labels):
    vectorizer = TfidfVectorizer()
    training_texts = [preprocess_text(text) for text, _ in training_data]
    training_vectors = vectorizer.fit_transform(training_texts)

    classifier = MultinomialNB()
    classifier.fit(training_vectors, training_labels)

    return vectorizer, classifier

# Predict the intent of the user input
def predict_intent(user_input, vectorizer, classifier):
    preprocessed_input = preprocess_text(user_input)
    input_vector = vectorizer.transform([preprocessed_input])
    intent = classifier.predict(input_vector)[0]
    return intent

# Get the chatbot response based on predicted intent
def get_response(intent):
    return responses.get(intent, responses["default"])[0]

# Main chatbot function
def chatbot():
    vectorizer, classifier = train_classifier(training_data, training_labels)
    print("Smart AI Bot: Hello! How can I assist you today? Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ")

        if user_input.lower() == 'quit':
            print("Smart AI Bot: Goodbye!")
            break

        # Predict intent and get a response
        intent = predict_intent(user_input, vectorizer, classifier)
        response = get_response(intent)
        
        print(f"Smart AI Bot: {response}\n")

# Run the chatbot
if __name__ == "__main__":
    chatbot()
