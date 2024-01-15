def draw_triangle(canvas, x, y, small_side, scale_factor, color, direction="up"):
    x1, y1 = x, y
    if direction == "up":
        x2, y2 = x - small_side / 2, y + small_side * scale_factor
        x3, y3 = x + small_side / 2, y + small_side * scale_factor
    else:
        x2, y2 = x - small_side / 2, y - small_side * scale_factor
        x3, y3 = x + small_side / 2, y - small_side * scale_factor

    canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline="black")