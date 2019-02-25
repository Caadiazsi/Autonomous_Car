import keras
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam

class DeepQLearning():

    def __init__(self):
        self.memory = []
        self.red = self.RedNeural()
        print(np.argmax(self.red.predict(np.array([[1, 1, 1]]))[0]))

    def RedNeural(self):
        model = Sequential()
        # Input Layer de tamaño 4 (3 sensores), y dos capas ocultas
        model.add(Dense(24, input_dim=3, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(3, activation='linear'))
        model.compile(loss='mse', optimizer=Adam())
        return model

    def recordar(self, estado, accion, recompensa, siguienteEstado, final):
        self.memory.append((estado, accion, recompensa, siguienteEstado, final))

    def aprender(self):
        if len(self.memory) < 1000:
            for estado, accion, recompensa, siguienteEstado, final in self.memory:
                siguienteEstado = np.array([[siguienteEstado[0], siguienteEstado[1], siguienteEstado[2]]])
                estado = np.array([[estado[0], estado[1], estado[2]]])
                target = recompensa
                if not final:
                  target = recompensa + 0.9 * \
                           np.amax(self.red.predict(siguienteEstado)[0])
                target_f = self.red.predict(estado)
                target_f[0][accion] = target
                self.red.fit(estado, target_f, epochs=1, verbose=0)
        else:
            minibatch = random.sample(self.memory, 1000)
            for estado, accion, recompensa, siguienteEstado, final in minibatch:
                siguienteEstado = np.array([[siguienteEstado[0], siguienteEstado[1], siguienteEstado[2]]])
                estado = np.array([[estado[0], estado[1], estado[2]]])
                target = recompensa
                if not final:
                  target = recompensa + 0.9 * \
                           np.amax(self.red.predict(siguienteEstado)[0])
                target_f = self.red.predict(estado)
                target_f[0][accion] = target
                #self.red.train_on_batch (estado, target_f)
                self.red.fit(estado, target_f, epochs=1, verbose=0)

    def actuar(self, state):
        state = np.array([[state[0], state[1], state[2]]])

        act_values = self.red.predict(state)
        return np.argmax(act_values[0])  # returns action

lolo = DeepQLearning()
#C:\Users\Camilo\AppData\Local\Temp\CUDA
