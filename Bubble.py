from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock
import random

class Renderer(Window):
    def __init__(self):
        super().__init__(width=1000, height=600, caption="Bubble sort")
        self.batch = Batch()
        self.bar_width = 4   # ความกว้างต่อ Bars
        self.spacing = 2     # ระยะห่างระหว่าง Bars
        self.bars = []
        self.num_bars = 100  # จำนวน Bars
        self.bar_color = (135, 206, 235)  # สี Bars

        # สร้างความสูง Bars แบบ Random
        self.heights = [random.randint(10, 500) for _ in range(self.num_bars)]
        self.create_bars()

    def create_bars(self):
        # ล้าง Bars ที่มีอยู่
        self.bars.clear()

        # คำนวณตำแหน่งเริ่มต้น Bars
        x = self.spacing
        for height in self.heights:
            bar = Rectangle(x, 0, self.bar_width, height, batch=self.batch, color=self.bar_color)
            self.bars.append(bar)
            x += self.bar_width + self.spacing

    def bubble_sort(self):
        n = len(self.heights)
        for i in range(n-1):
            for j in range(0, n-i-1):
                if self.heights[j] > self.heights[j+1]:
                    # สลับความสูงของ Bars
                    self.heights[j], self.heights[j+1] = self.heights[j+1], self.heights[j]
                    # สร้างความสูง Bars
                    self.create_bars()
                    return

    def on_update(self, dt):
        self.bubble_sort()

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == "__main__":
    renderer = Renderer()
    clock.schedule_interval(renderer.on_update, 1 / 60.0)  # ใช้ 60 เฟรมต่อวิ
    run()
