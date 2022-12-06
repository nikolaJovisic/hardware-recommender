import numpy as np
import tensorflow as tf
from keras import utils
from sklearn.model_selection import train_test_split

COMPONENTS = {0: "motherboards", 1: "processors", 2: "ram"}

def load_configurations():
    names = []
    x = []

    with open(f"../scraper/data/combined_configurations.txt") as file:
        for line in file:
            encoded = list(line[:30].encode())
            if len(encoded) < 30:
                continue
            encoded = np.array(encoded[:30])
            names.append(line[:30])
            x.append(encoded)
    x = np.array(x)

    return names, x

def load_components():
    names = []
    categories = []
    x = []
    y = []

    for key, val in COMPONENTS.items():
        with open(f"../scraper/data/{val}.txt") as file:
            for line in file:
                encoded = list(line[:30].encode())
                if len(encoded) < 30:
                    continue
                encoded = np.array(encoded[:30])
                names.append(line[:30])
                categories.append(val)
                x.append(encoded)
                y.append(key)

    x = np.array(x)
    y = utils.to_categorical(y)
    return names, categories, x, y

def print_predictions_test(predictions, y_test, test_names, test_categories):
    for prediction, label, name, category in zip(
        predictions, y_test, test_names, test_categories
    ):
        print(
            tuple(COMPONENTS.values()),
            "->",
            tuple(map(lambda p: round(p, 2), prediction)),
            tuple(label),
            name,
            category,
        )

def print_predictions_configurations(predictions, test_names):
    for prediction, name in zip(
        predictions, test_names
    ):
        print(
            tuple(COMPONENTS.values()),
            "->",
            tuple(map(lambda p: round(p, 2), prediction)),
            name,
        )

def make_model():
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(30, input_shape=(30,), activation="relu"),
            tf.keras.layers.Dense(50, activation="relu"),
            tf.keras.layers.Dense(100, activation="relu"),
            tf.keras.layers.Dense(50, activation="relu"),
            tf.keras.layers.Dense(3, activation="softmax"),
        ]
    )
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model

def prepare_data():
    names, categories, x, y = load_components()

    data = list(zip(x, names, categories))

    x_train, x_test, y_train, y_test = train_test_split(
        data, y, test_size=0.33, random_state=20, shuffle=True
    )

    x_test = np.array(x_test, dtype="object")
    x_train = np.array(x_train, dtype="object")

    test_names = x_test[:, 1]
    test_categories = x_test[:, 2]

    x_train = np.stack(np.array(x_train[:, 0]))
    x_test = np.stack(np.array(x_test[:, 0]))

    return x_train, x_test, y_train, y_test, test_names, test_categories

def main():
    x_train, x_test, y_train, y_test, test_names, test_categories = prepare_data()
    model = make_model()
    model.fit(x_train, y_train, epochs=300, validation_split=0.33)
    predictions = model.predict(x_test)
    print_predictions_test(predictions, y_test, test_names, test_categories)
    train_loss, train_acc = model.evaluate(x_train, y_train)
    test_loss, test_acc = model.evaluate(x_test, y_test)
    print("Classification accuracy on training set: ", train_acc)
    print("Classification accuracy on test set: ", test_acc)

    names_configurations, x_configurations = load_configurations()
    predictions = model.predict(x_configurations)
    print_predictions_configurations(predictions, names_configurations)

if __name__ == '__main__':
    main()