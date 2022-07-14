from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.backend import clear_session


def build_model(input_shape, verbose=1):
    """
    Builds LSTM model

    input_shape: tuple\t input shape for LSTM
    """
    clear_session()
    model = Sequential()
    model.add(LSTM(200, input_shape=input_shape, return_sequences=True))
    model.add(Dropout(0.6))
    model.add(LSTM(50))
    model.add(Dropout(0.1))
    model.add(Dense(1))

    model.compile(optimizer="adam", loss="mean_squared_error", metrics=["mae"])
    if verbose != 0:
        print(model.summary())
    return model


def fit_model(model, X_train, y_train, X_test, y_test):
    history = model.fit(
        X_train,
        y_train,
        epochs=30,
        batch_size=256,
        validation_data=(X_test, y_test),
        callbacks=[EarlyStopping(patience=3)],
    )
    return history
