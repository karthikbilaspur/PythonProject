import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt

# Load the CIFAR-10 dataset
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# Normalize the pixel values
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

# Convert class labels to categorical labels
num_classes = 10
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

# Define the CNN model
def create_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(num_classes, activation='softmax'))
    return model

# Compile the model
def compile_model(model):
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
def train_model(model, x_train, y_train, x_test, y_test):
    batch_size = 128
    epochs = 10

    early_stopping = EarlyStopping(monitor='val_loss', patience=3, min_delta=0.001)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=0.00001)

    history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs,
                        validation_data=(x_test, y_test), callbacks=[early_stopping, reduce_lr])
    return history

# Evaluate the model
def evaluate_model(model, x_test, y_test):
    loss, accuracy = model.evaluate(x_test, y_test)
    return loss, accuracy

# Use the model to classify a new image
def classify_image(model, image):
    image_class = model.predict(image.reshape((1, 32, 32, 3)))
    return image_class.argmax()

# Main function
def main():
    model = create_model()
    compile_model(model)
    history = train_model(model, x_train, y_train, x_test, y_test)
    loss, accuracy = evaluate_model(model, x_test, y_test)
    print(f"Test accuracy: {accuracy:.2f}")

    new_image = x_test[0]
    predicted_class = classify_image(model, new_image)
    print(f"Predicted class: {predicted_class}")

    # Plot training and validation accuracy
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()