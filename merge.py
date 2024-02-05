from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock
import random

class Renderer(Window):
    def __init__(self):
        super().__init__(width=1000, height=600, caption="Merge sort")
        self.batch = Batch()
        self.bar_width = 4   # Width of each bar
        self.spacing = 2     # Spacing between bars
        self.bars = []
        self.num_bars = 100  # Number of bars
        self.normal_color = (135, 206, 235)  # Sky blue color for the bars
        self.merge_color = (255, 0, 0)  # Red color for the merging bar

        # Generate random heights for bars
        self.heights = [random.randint(10, 500) for _ in range(self.num_bars)]
        self.create_bars()

        self.sorting_generator = self.merge_sort(self.heights)

    def create_bars(self):
        # Clear existing bars
        self.bars.clear()

        # Calculate initial positions for bars
        x = self.spacing
        for height in self.heights:
            bar = Rectangle(x, 0, self.bar_width, height, batch=self.batch, color=self.normal_color)
            self.bars.append(bar)
            x += self.bar_width + self.spacing

    def merge_sort(self, arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]

            yield from self.merge_sort(left_half)
            yield from self.merge_sort(right_half)

            i = j = k = 0
            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    arr[k] = left_half[i]
                    i += 1
                else:
                    arr[k] = right_half[j]
                    j += 1
                k += 1
                yield arr

            while i < len(left_half):
                arr[k] = left_half[i]
                i += 1
                k += 1
                yield arr

            while j < len(right_half):
                arr[k] = right_half[j]
                j += 1
                k += 1
                yield arr

            # Highlight the merging bar
            merge_index = k - 1
            self.bars[merge_index].color = self.merge_color
            yield arr

            # Reset color of all bars
            for b in self.bars:
                b.color = self.normal_color

    def on_update(self, dt):
        try:
            next(self.sorting_generator)
            self.create_bars()
        except StopIteration:
            clock.unschedule(self.on_update)

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == "__main__":
    renderer = Renderer()
    clock.schedule_interval(renderer.on_update, 1 / 20.0)  # Update at 20 Hz
    run()
