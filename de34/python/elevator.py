import tkinter as tk

class MovingObjectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("動くオブジェクト")
        self.root.geometry("300x300")

        # キャンバス作成
        self.canvas = tk.Canvas(root, width=300, height=250, bg='white')
        self.canvas.pack()

        # 対象オブジェクト（円）
        self.obj = self.canvas.create_oval(130, 100, 170, 140, fill='blue')

        # ボタン
        self.button = tk.Button(root, text="動かす", command=self.toggle_move)
        self.button.pack(pady=10)

        # 動作状態
        self.moving = False
        self.direction = 1  # 1: 下, -1: 上

    def toggle_move(self):
        self.moving = not self.moving
        if self.moving:
            self.button.config(text="止める")
            self.move()
        else:
            self.button.config(text="動かす")

    def move(self):
        if not self.moving:
            return

        # オブジェクトを上下に動かす
        self.canvas.move(self.obj, 0, self.direction * 2)

        # 座標をチェックして方向反転
        x0, y0, x1, y1 = self.canvas.coords(self.obj)
        if y0 <= 0 or y1 >= 250:
            self.direction *= -1

        # 繰り返し呼び出す（20ms後）
        self.root.after(20, self.move)

# 実行部分
if __name__ == "__main__":
    root = tk.Tk()
    app = MovingObjectApp(root)
    root.mainloop()
