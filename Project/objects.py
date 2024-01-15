def draw_triangle(canvas, x, y, small_side, scale_factor, color, direction="up"):
    """
    Draw a triangle on the given canvas.

    Parameters:
    - canvas (tk.Canvas): The Tkinter canvas where the triangle will be drawn.
    - x (float): The x-coordinate of the triangle's top vertex.
    - y (float): The y-coordinate of the triangle's top vertex.
    - small_side (float): The length of the smaller side of the triangle.
    - scale_factor (float): The scale factor to determine the length of the longer side.
    - color (str): The fill color of the triangle.
    - direction (str, optional): The direction in which the triangle points, either "up" or "down". Defaults to "up".

    Returns:
    None
    """

    x1, y1 = x, y
    if direction == "up":
        x2, y2 = x - small_side / 2, y + small_side * scale_factor
        x3, y3 = x + small_side / 2, y + small_side * scale_factor
    else:
        x2, y2 = x - small_side / 2, y - small_side * scale_factor
        x3, y3 = x + small_side / 2, y - small_side * scale_factor

    canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, outline="black")