import matplotlib.pyplot as plt
import numpy as np

def bresenham_line(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    x, y = x0, y0
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    if dx > dy:
        error = 2 * dy - dx
        while x != x1:
            points.append((x, y))
            if error >= 0:
                y += sy
                error -= 2 * dx
            error += 2 * dy
            x += sx
    else:
        error = 2 * dx - dy
        while y != y1:
            points.append((x, y))
            if error >= 0:
                x += sx
                error -= 2 * dy
            error += 2 * dx
            y += sy

    points.append((x1, y1))
    return points

# اندازه تصویر
width, height = 20, 12

# نقاط شروع و پایان
x0, y0 = 1, 1
x1, y1 = 18, 8

# گرفتن پیکسل‌های روشن
line_pixels = bresenham_line(x0, y0, x1, y1)

# بوم تصویر
canvas = np.zeros((height, width))
for x, y in line_pixels:
    if 0 <= x < width and 0 <= y < height:
        canvas[y][x] = 1  # سطر=y، ستون=x

# نمایش تصویر
fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(canvas, cmap='Greys', interpolation='none', extent=[0, width, height, 0])

# خط ریاضی اصلی
ax.plot([x0 + 0.5, x1 + 0.5], [y0 + 0.5, y1 + 0.5], color='red', linewidth=1.5, label='Ideal Line')

# پیکسل‌های Bresenham
ax.plot([x + 0.5 for x, y in line_pixels], [y + 0.5 for x, y in line_pixels],
        'bs', markersize=20, label='Bresenham Pixels')

# تنظیمات شبکه
ax.set_xticks(np.arange(0, width, 1))
ax.set_yticks(np.arange(0, height, 1))
ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
ax.set_yticks(np.arange(-0.5, height, 1), minor=True)
ax.grid(which='minor', color='lightgray', linestyle='-', linewidth=0.5)
ax.set_xlim([0, width])
ax.set_ylim([height, 0])
ax.set_aspect('equal')
ax.legend()
plt.title("Bresenham vs. Ideal Line")
plt.show()
