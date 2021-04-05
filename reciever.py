import socket
import tkinter as tk
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk



addr = ("127.0.0.1", 65534)
buf = 512
width = 640
height = 480
code = b'start'
num_of_chunks = width * height * 3 / buf

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(addr)
    # while True:
    chunks = []
    start = False
    while len(chunks) < num_of_chunks:
        chunk, _ = s.recvfrom(buf)
        if start:
            chunks.append(chunk)
        elif chunk.startswith(code):
            start = True

    byte_frame = b''.join(chunks)

    frame = np.frombuffer(
        byte_frame, dtype=np.uint8).reshape(height, width, 3)

    root = tk.Tk()

    img = ImageTk.PhotoImage(image=Image.fromarray(frame))

    canvas = tk.Canvas(root)
    canvas.pack()
    canvas.create_image(20, 20, anchor="nw", image=img)

    root.mainloop()
