import numpy as np
from tensorflow.keras.models import load_model

label_map = {
    0: "A", 1: "B", 2: "C", 3: " ", 4: "D", 5: "Đ", 6: "E", 7: "G",
    8: "H", 9: "Hỏi", 10: "Huyền", 11: "I", 12: "K", 13: "L", 14: "N",
    15: "Móc", 16: "Mũ", 17: "M", 18: "Nặng", 19: "Ngã", 20: "O", 21: "P",
    22: "Q", 23: "R", 24: "S", 25: "Sắc", 26: "T", 27: "Trăng", 28: "U",
    29: "V", 30: "X", 31: "Y"
}

class GestureModel:
    def __init__(self, model_path):
        self.model = load_model(model_path)

    def predict(self, input_data):
        # input_data: numpy array (1, timestep, feature_dim)
        preds = self.model.predict(np.expand_dims(input_data, axis=0))
        class_id = np.argmax(preds[0])
        return label_map.get(class_id, "Unknown")

if __name__ == "__main__":
    gm = GestureModel("models/hand_gesture_lstm_model.keras")
    dummy_input = np.zeros((46, 126))  # mẫu dummy
    print("Dự đoán thử:", gm.predict(dummy_input))
