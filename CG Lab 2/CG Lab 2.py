import math
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk


class CGLab2:

    def __init__(self, root):
        self.root = root
        self.root.title("Формирование изображений")
        self.root.geometry("980x550")

        self.img1 = None 
        self.img2 = None 
        self.tk_img1 = None
        self.tk_img2 = None

        top_frame = tk.Frame(root, pady=10, padx=10)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(top_frame, text="Width 1").grid(
            row=0, column=0, sticky="e", padx=2, pady=2
        )
        self.entry_w1 = tk.Entry(top_frame, width=6)
        self.entry_w1.insert(0, "400")
        self.entry_w1.grid(row=0, column=1, padx=2, pady=2)

        tk.Label(top_frame, text="Height 1").grid(
            row=1, column=0, sticky="e", padx=2, pady=2
        )
        self.entry_h1 = tk.Entry(top_frame, width=6)
        self.entry_h1.insert(0, "400")
        self.entry_h1.grid(row=1, column=1, padx=2, pady=2)

        btn_create = tk.Button(top_frame, text="Создать 1", command=self.create_canvas)
        
        btn_create.grid(row=0, column=2, rowspan=2, padx=5, pady=2)

        btn_open = tk.Button(top_frame, text="Открыть 2", command=self.open_image)
        btn_open.grid(row=0, column=3, rowspan=2, padx=5, pady=2)

        self.lbl_w2 = tk.Label(top_frame, text="Width 2:  -")
        self.lbl_w2.grid(row=0, column=4, sticky="w", padx=5)
        self.lbl_h2 = tk.Label(top_frame, text="Height 2: -")
        self.lbl_h2.grid(row=1, column=4, sticky="w", padx=5)

        tk.Label(top_frame, text="x1").grid(row=0, column=5, sticky="e", padx=2)
        self.entry_x1 = tk.Entry(top_frame, width=6)
        self.entry_x1.insert(0, "0")
        self.entry_x1.grid(row=0, column=6, padx=2)

        tk.Label(top_frame, text="y1").grid(row=1, column=5, sticky="e", padx=2)
        self.entry_y1 = tk.Entry(top_frame, width=6)
        self.entry_y1.insert(0, "0")
        self.entry_y1.grid(row=1, column=6, padx=2)

        tk.Label(top_frame, text="Wf").grid(row=0, column=7, sticky="e", padx=2)
        self.entry_wf = tk.Entry(top_frame, width=6)
        self.entry_wf.insert(0, "120")
        self.entry_wf.grid(row=0, column=8, padx=2)

        tk.Label(top_frame, text="Hf").grid(row=1, column=7, sticky="e", padx=2)
        self.entry_hf = tk.Entry(top_frame, width=6)
        self.entry_hf.insert(0, "60")
        self.entry_hf.grid(row=1, column=8, padx=2)

        tk.Label(top_frame, text="x2").grid(
            row=0, column=9, sticky="e", padx=2
        )
        self.entry_x2 = tk.Entry(top_frame, width=6)
        self.entry_x2.insert(0, "0") 
        self.entry_x2.grid(row=0, column=10, padx=2)

        tk.Label(top_frame, text="y2").grid(
            row=1, column=9, sticky="e", padx=2
        )
        self.entry_y2 = tk.Entry(top_frame, width=6)
        self.entry_y2.insert(0, "0")
        self.entry_y2.grid(row=1, column=10, padx=2)

        btn_copy = tk.Button(
            top_frame, text="Перенести", command=self.copy_fragment
        )
        btn_copy.grid(row=0, column=11, padx=5, pady=2)

        btn_coords = tk.Button(
            top_frame, text="Координаты", command=self.draw_axes
        )
        btn_coords.grid(row=0, column=12, padx=5, pady=2)

        btn_save = tk.Button(
            top_frame, text="Сохранить", command=self.save_image
        )
        btn_save.grid(row=0, column=13, padx=5, pady=2)

        btn_graph = tk.Button(
            top_frame, text="x*sin(x)", command=self.draw_graph
        )
        btn_graph.grid(row=1, column=12, padx=5, pady=2)

        view_frame = tk.Frame(root, pady=10)
        view_frame.pack(expand=True, fill=tk.BOTH)

        self.lbl_img1 = tk.Label(
            view_frame, bd=1, relief="solid", bg="white"
        )
        self.lbl_img1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)

        self.lbl_img2 = tk.Label(
            view_frame, bd=1, relief="solid", bg="white"
        )
        self.lbl_img2.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=10)

    def create_canvas(self):
            w = int(self.entry_w1.get())
            h = int(self.entry_h1.get())
            self.img1 = Image.new("RGB", (w, h), color="white")
            self.update_display(1)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.bmp *.jpeg")])
        if file_path:
            self.img2 = Image.open(file_path).convert("RGB")
            w, h = self.img2.size
            self.lbl_w2.config(text=f"Width 2: {w}")
            self.lbl_h2.config(text=f"Height 2: {h}")
            self.update_display(2)

    def copy_fragment(self):
        if not self.img1 or not self.img2:
            return

        x1 = int(self.entry_x1.get())
        y1 = int(self.entry_y1.get())
        wf = int(self.entry_wf.get())  
        hf = int(self.entry_hf.get())
        x2 = int(self.entry_x2.get())
        y2 = int(self.entry_y2.get())

        w1, h1 = self.img1.size
        w2, h2 = self.img2.size

        pixels1 = self.img1.load()
        pixels2 = self.img2.load()

        for py in range(hf):
            for px in range(wf):
                src_x = x1 + px
                src_y = y1 + py

                dst_x = x2 + px
                dst_y = y2 + py

                if 0 <= src_x < w2 and 0 <= src_y < h2:
                    if 0 <= dst_x < w1 and 0 <= dst_y < h1:
                        pixels1[dst_x, dst_y] = pixels2[src_x, src_y]

        draw = ImageDraw.Draw(self.img1)
        draw.rectangle([x2, y2, x2 + wf - 1, y2 + hf - 1], outline="red", width=2)

        self.update_display(1)

    def draw_axes(self):
        if not self.img1:
            messagebox.showwarning("Предупреждение", "Сначала создайте Холст 1!")
            return

        draw = ImageDraw.Draw(self.img1)
        w, h = self.img1.size

        draw.line([(20, h - 10), (20, 10)], fill="black", width=1)
        draw.polygon([(17, 15), (20, 5), (23, 15)], fill="black")

        center_y = h // 2
        draw.line([(10, center_y), (w - 10, center_y)], fill="black", width=1)
        draw.polygon(
            [(w - 15, center_y - 3), (w - 5, center_y), (w - 15, center_y + 3)],
            fill="black",
        )

        draw.text((5, center_y + 5), "0", fill="black")
        draw.text((w - 15, center_y + 10), "x", fill="black")
        draw.text((25, 5), "y", fill="black")

        self.update_display(1)

    def draw_graph(self):
        if not self.img1:
            messagebox.showwarning("Предупреждение", "Сначала создайте Холст 1!")
            return

        draw = ImageDraw.Draw(self.img1)
        w, h = self.img1.size

        center_x = 20
        center_y = h // 2

        scale_x = 0.1
        scale_y = 50.0

        points = []
        for px in range(1, w - 30):
            x = px * scale_x

            y = x * math.sin(x)

            draw_x = center_x + px
            draw_y = center_y - int(y * scale_y)

            points.append((draw_x, draw_y))

        if len(points) > 1:
            draw.line(points, fill="green", width=2)

        self.update_display(1)

    def save_image(self):
        if not self.img1:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if file_path:
            self.img1.save(file_path)

    def update_display(self, target):
        if target == 1 and self.img1:
            preview = self.img1.copy()
            preview.thumbnail((400, 400))
            self.tk_img1 = ImageTk.PhotoImage(preview)
            self.lbl_img1.config(image=self.tk_img1)
        elif target == 2 and self.img2:
            preview = self.img2.copy()
            preview.thumbnail((400, 400))
            self.tk_img2 = ImageTk.PhotoImage(preview)
            self.lbl_img2.config(image=self.tk_img2)


if __name__ == "__main__":
    root = tk.Tk()
    app = CGLab2(root)
    root.mainloop()