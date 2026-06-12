import tensorflow as tf
from tensorflow.keras import layers, models

class HybridMulticlassModel:
    def __init__(self, global_length=2001, local_length=201, tabular_length=8):
        self.model = self._build_model(global_length, local_length, tabular_length)

    def _build_cnn_branch(self, input_tensor, num_blocks):
        x = input_tensor
        for i in range(num_blocks):
            filters = 16 * (2 ** i)
            x = layers.Conv1D(filters, 5, activation='relu', padding='same')(x)
            x = layers.Conv1D(filters, 5, activation='relu', padding='same')(x)
            x = layers.MaxPooling1D(2)(x)
            
            x_norm = layers.LayerNormalization()(x)
            attention_out = layers.MultiHeadAttention(num_heads=2, key_dim=filters // 2)(x_norm, x_norm)
            x = layers.Add()([x, attention_out])
            x = layers.LayerNormalization()(x)

        return layers.Flatten()(x)

    def _build_model(self, global_length, local_length, tabular_length):
        global_input = layers.Input(shape=(global_length, 1), name='global_input')
        local_input = layers.Input(shape=(local_length, 1), name='local_input')
        tabular_input = layers.Input(shape=(tabular_length,), name='tabular_input')

        global_out = self._build_cnn_branch(global_input, 4)
        local_out = self._build_cnn_branch(local_input, 2)
        
        # Tabular dense
        tab_x = layers.Dense(64, activation='relu')(tabular_input)
        tab_x = layers.LayerNormalization()(tab_x)
        tab_x = layers.Dense(32, activation='relu')(tab_x)

        combined = layers.concatenate([global_out, local_out, tab_x])
        
        x = combined
        for _ in range(3):
            x = layers.Dense(256, activation='relu')(x)
            x = layers.Dropout(0.2)(x)
        
        # 5 Classes: Planet, EB, Blend, Variable, Noise
        output = layers.Dense(5, activation='softmax', name='output')(x)
        
        model = models.Model(inputs=[global_input, local_input, tabular_input], outputs=output)
        opt = tf.keras.optimizers.Adam(learning_rate=1e-4, clipnorm=1.0)
        model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def summary(self):
        return self.model.summary()
