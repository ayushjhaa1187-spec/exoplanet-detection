import tensorflow as tf
from tensorflow.keras import layers, models
import logging

log = logging.getLogger(__name__)

class AstroNetModel:
    def __init__(self, global_bins=2001, local_bins=201):
        self.global_bins = global_bins
        self.local_bins = local_bins
        self.model = self._build_model()

    def _build_cnn_branch(self, inputs, num_blocks, block_size, initial_filters, filter_factor, kernel_size, pool_size, pool_strides):
        x = inputs
        for i in range(num_blocks):
            filters = int(initial_filters * (filter_factor ** i))
            for j in range(block_size):
                x = layers.Conv1D(filters, kernel_size, activation='relu', padding='same')(x)
            if pool_size > 1:
                x = layers.MaxPool1D(pool_size=pool_size, strides=pool_strides, padding='same')(x)
        return layers.Flatten()(x)

    def _build_model(self):
        log.info("Building AstroNet model...")
        
        # Global Branch
        global_input = layers.Input(shape=(self.global_bins, 1), name='global_input')
        global_out = self._build_cnn_branch(
            global_input, 
            num_blocks=5, 
            block_size=2, 
            initial_filters=16, 
            filter_factor=2, 
            kernel_size=5, 
            pool_size=5, 
            pool_strides=2
        )
        
        # Local Branch
        local_input = layers.Input(shape=(self.local_bins, 1), name='local_input')
        local_out = self._build_cnn_branch(
            local_input, 
            num_blocks=2, 
            block_size=2, 
            initial_filters=16, 
            filter_factor=2, 
            kernel_size=5, 
            pool_size=7, 
            pool_strides=2
        )
        
        # Combined
        combined = layers.concatenate([global_out, local_out])
        
        # Fully Connected Layers
        x = combined
        for _ in range(4):
            x = layers.Dense(512, activation='relu')(x)
        
        output = layers.Dense(1, activation='sigmoid', name='output')(x)
        
        model = models.Model(inputs=[global_input, local_input], outputs=output)
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def summary(self):
        return self.model.summary()

    def predict(self, global_view, local_view):
        # Reshape for Keras (batch, length, channels)
        global_view = global_view.reshape((1, self.global_bins, 1))
        local_view = local_view.reshape((1, self.local_bins, 1))
        return self.model.predict({'global_input': global_view, 'local_input': local_view})

    def save(self, path):
        """Save model weights."""
        self.model.save(path)
        log.info(f"Model saved to {path}")

    def load(self, path):
        """Load model weights."""
        self.model = models.load_model(path)
        log.info(f"Model loaded from {path}")

class AdvancedAstroNetModel(AstroNetModel):
    """Upgraded model with Attention blocks (inspired by ExoMiner)."""
    
    def _build_cnn_branch(self, inputs, num_blocks, block_size, initial_filters, filter_factor, kernel_size, pool_size, pool_strides):
        x = inputs
        for i in range(num_blocks):
            filters = int(initial_filters * (filter_factor ** i))
            for j in range(block_size):
                x = layers.Conv1D(filters, kernel_size, activation='relu', padding='same')(x)
            
            # Add Attention after each block
            attention_out = layers.MultiHeadAttention(num_heads=2, key_dim=filters // 2)(x, x)
            x = layers.Add()([x, attention_out])
            x = layers.LayerNormalization()(x)

            if pool_size > 1:
                x = layers.MaxPool1D(pool_size=pool_size, strides=pool_strides, padding='same')(x)
        return layers.Flatten()(x)

    def _build_model(self):
        log.info("Building Advanced AstroNet model with Attention...")
        return super()._build_model()
