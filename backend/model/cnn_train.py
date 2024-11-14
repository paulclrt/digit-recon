import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# Charger le dataset MNIST
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normaliser les données
x_train, x_test = x_train / 255.0, x_test / 255.0


# Construire un CNN simple
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),  # Première couche de convolution
    layers.MaxPooling2D((2, 2)),  # Couche de pooling pour réduire la dimension
    layers.Conv2D(64, (3, 3), activation='relu'),  # Deuxième couche de convolution
    layers.MaxPooling2D((2, 2)),  # Deuxième couche de pooling
    layers.Conv2D(64, (3, 3), activation='relu'),  # Troisième couche de convolution

    # Passer à des couches denses
    layers.Flatten(),  # Aplatir la sortie 2D en 1D
    layers.Dense(64, activation='relu'),  # Couche entièrement connectée
    layers.Dense(10, activation='softmax')  # Couche de sortie
])


# Compiler le modèle
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Entraîner le modèle
history = model.fit(x_train, y_train, epochs=5, validation_split=0.1)

# Évaluer le modèle sur les données de test
test_loss, test_acc = model.evaluate(x_test, y_test)
print(f'Précision sur les données de test : {test_acc:.2f}')

# Visualiser l'évolution de la précision et de la perte
plt.plot(history.history['accuracy'], label='Précision d’entraînement')
plt.plot(history.history['val_accuracy'], label='Précision de validation')
plt.xlabel('Épochs')
plt.ylabel('Précision')
plt.legend()
plt.show()

# Sauvegarder le modèle dans un fichier ou un dossier
model.save('mon_cnn_modele.h5')  # Sauvegarde au format HDF5
# OU
# model.save('mon_modele')  # Sauvegarde au format TensorFlow (dossier)
