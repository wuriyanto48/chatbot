import tensorflow as tf
import pickle

'''
create tensorflow model
'''
def create_model(num_words, output_length):

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(128, input_shape=(num_words,)))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.Dropout(0.5))

    model.add(tf.keras.layers.Dense(64))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.Dropout(0.5))

    model.add(tf.keras.layers.Dense(output_length))
    model.add(tf.keras.layers.Activation('softmax'))

    # compile model using Stochastic gradient descent
    sgd = tf.keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    return model

'''
create tensorflow model from DNN class
'''
def create_model_from_dnn(num_words, output_length, model_dir, data_dir):

    model = DNN(num_words, output_length, model_dir, data_dir)

    # compile model using Stochastic gradient descent
    sgd = tf.keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    return model

'''
DNN class by extending keras Model
'''
class DNN(tf.keras.Model):
    def __init__(self, word_size, output_length, model_dir, data_dir):

        super(DNN, self).__init__()

        self.model_dir = model_dir
        self.data_dir = data_dir

        # input layer
        self.dense_1 = tf.keras.layers.Dense(128, input_shape=(word_size,))
        self.activation_1 = tf.keras.layers.Activation('relu')
        self.dropout_1 = tf.keras.layers.Dropout(0.5)

        # hidden layer
        self.dense_2 = tf.keras.layers.Dense(64)
        self.activation_2 = tf.keras.layers.Activation('relu')
        self.dropout_2 = tf.keras.layers.Dropout(0.5)

        # output layer
        self.dense_3 = tf.keras.layers.Dense(output_length)
        self.activation_3 = tf.keras.layers.Activation('relu')
    
    def call(self, input_tensor):
        x = self.dense_1(input_tensor)
        x = self.activation_1(x)
        x = self.dropout_1(x)

        x = self.dense_2(x)
        x = self.activation_2(x)
        x = self.dropout_2(x)

        x = self.dense_3(x)
        x = self.activation_3(x)

        return x
    
    '''
    save tensorflow trained model
    '''
    def save(self, tokenizer):
        self.save_weights(self.model_dir, save_format='tf')
        with open(self.data_dir, 'wb') as tp:
            pickle.dump(tokenizer, tp, protocol=pickle.HIGHEST_PROTOCOL)

    '''
    load tensorflow trained model from disk
    '''
    def load(self):
        with open(self.data_dir, 'rb') as tp:
            tokenizer_data = pickle.load(tp)

        model = self.load_weights(self.model_dir)
        return (model, tokenizer_data)