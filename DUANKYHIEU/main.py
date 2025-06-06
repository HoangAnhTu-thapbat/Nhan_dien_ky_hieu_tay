import tkinter as tk
from gui import GestureAppGui
from model import GestureModel

def main():
    window = tk.Tk()
    model = GestureModel("models/hand_gesture_lstm_model.keras")
    app = GestureAppGui(window, "Nhận diện ký hiệu", model)
    window.mainloop()

if __name__ == "__main__":
    main()
