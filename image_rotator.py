import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import numpy as np
import math

class ImageRotatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Rotator")
        self.root.geometry("1000x600")
        self.root.configure(bg='#c0c0c0')
        
        self.style = ttk.Style()
        self.style.configure('.', font=('Courier', 10), background='#c0c0c0')
        self.style.configure('TFrame', background='#c0c0c0')
        self.style.configure('TButton', 
                            font=('Courier', 10, 'bold'),
                            background='#c0c0c0',
                            relief=tk.RAISED,
                            borderwidth=2)
        self.style.configure('TScale', background='#c0c0c0')
        self.style.configure('TLabel', background='#c0c0c0')
        
        self.original_image = None
        self.tk_image = None
        self.rotation_angle = tk.DoubleVar(value=0)
        self.rotation_angle.trace_add("write", self.update_rotation)
        
        self.create_widgets()
        
    def create_widgets(self):
        main_container = tk.Frame(self.root, bg='#c0c0c0', bd=2, relief=tk.SUNKEN)
        main_container.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        
        left_panel = tk.Frame(main_container, width=250, bg='#c0c0c0', bd=2, relief=tk.SUNKEN)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=4, pady=4)
        
        right_panel = tk.Frame(main_container, bg='#c0c0c0', bd=2, relief=tk.SUNKEN)
        right_panel.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=4, pady=4)
        
        self.image_label = tk.Label(right_panel, bg='#c0c0c0')
        self.image_label.pack(expand=True, fill=tk.BOTH, padx=2, pady=2)
        
        title_label = tk.Label(
            left_panel, 
            text="Image Rotator 98",
            font=('Courier', 14, 'bold'),
            bg='#c0c0c0',
            fg='black'
        )
        title_label.pack(pady=(10, 20))
        
        import_btn = tk.Button(
            left_panel, 
            text="Import Image", 
            command=self.load_image,
            font=('Courier', 10, 'bold'),
            bg='#c0c0c0',
            fg='black',
            activebackground='#c0c0c0',
            activeforeground='black',
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=3
        )
        import_btn.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        angle_frame = tk.LabelFrame(
            left_panel, 
            text=" Rotation Angle (radians) ",
            font=('Courier', 9),
            bg='#c0c0c0',
            fg='black',
            bd=2,
            relief=tk.GROOVE
        )
        angle_frame.pack(fill=tk.X, pady=5, padx=5)
        
        self.angle_slider = ttk.Scale(
            angle_frame,
            from_=0,
            to=2*math.pi,
            variable=self.rotation_angle,
            orient=tk.HORIZONTAL
        )
        self.angle_slider.pack(fill=tk.X, pady=5, padx=5)
        
        self.angle_value = tk.Label(
            angle_frame, 
            text="0 rad",
            font=('Courier', 9),
            bg='#c0c0c0',
            fg='black'
        )
        self.angle_value.pack(anchor=tk.W, padx=5)
        
        pi_frame = tk.Frame(angle_frame, bg='#c0c0c0')
        pi_frame.pack(fill=tk.X, pady=(5, 0))
        
        pi_values = {
            "0": 0,
            "π/2": math.pi/2,
            "π": math.pi,
            "3π/2": 3*math.pi/2,
            "2π": 2*math.pi
        }
        
        for label, value in pi_values.items():
            btn = tk.Button(
                pi_frame,
                text=label,
                command=lambda v=value: self.rotation_angle.set(v),
                font=('Courier', 8),
                bg='#c0c0c0',
                fg='black',
                activebackground='#c0c0c0',
                activeforeground='black',
                relief=tk.RAISED,
                bd=2,
                padx=5,
                pady=1
            )
            btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        
        save_btn = tk.Button(
            left_panel, 
            text="Save Rotated Image", 
            command=self.save_image,
            font=('Courier', 10, 'bold'),
            bg='#c0c0c0',
            fg='black',
            activebackground='#c0c0c0',
            activeforeground='black',
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=3,
            state=tk.DISABLED
        )
        save_btn.pack(fill=tk.X, pady=(15, 5), padx=5)
        self.save_btn = save_btn
    
    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.display_image(self.original_image)
                self.save_btn.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {e}")
    
    def display_image(self, image):
        window_width = self.root.winfo_width() - 300
        window_height = self.root.winfo_height() - 20
        
        img_width, img_height = image.size
        ratio = min(window_width/img_width, window_height/img_height)
        new_size = (int(img_width * ratio), int(img_height * ratio))
        
        resized_image = image.resize(new_size, Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=self.tk_image)
    
    def rotate_image_complex(self, image, theta_radians):
        img_array = np.array(image)
        height, width = img_array.shape[:2]
        
        x = np.linspace(-1, 1, width)
        y = np.linspace(-1, 1, height)
        X, Y = np.meshgrid(x, y)
        
        Z = X + 1j * Y
        
        rotation = np.cos(theta_radians) + 1j * np.sin(theta_radians)
        
        Z_rotated = Z * rotation
        
        X_rot = np.real(Z_rotated)
        Y_rot = np.imag(Z_rotated)
        
        X_rot = ((X_rot + 1) * (width - 1) / 2).astype(int)
        Y_rot = ((Y_rot + 1) * (height - 1) / 2).astype(int)
        
        X_rot = np.clip(X_rot, 0, width - 1)
        Y_rot = np.clip(Y_rot, 0, height - 1)
        
        if len(img_array.shape) == 3:
            rotated_img = img_array[Y_rot, X_rot, :]
        else:
            rotated_img = img_array[Y_rot, X_rot]
        
        return Image.fromarray(rotated_img)
    
    def update_rotation(self, *args):
        if self.original_image:
            angle = self.rotation_angle.get()
            if angle == 0:
                display_text = "0 rad"
            elif abs(angle - math.pi) < 0.01:
                display_text = "π rad"
            elif abs(angle - math.pi/2) < 0.01:
                display_text = "π/2 rad"
            elif abs(angle - 3*math.pi/2) < 0.01:
                display_text = "3π/2 rad"
            elif abs(angle - 2*math.pi) < 0.01:
                display_text = "2π rad"
            else:
                display_text = f"{angle:.3f} rad"
            
            self.angle_value.config(text=display_text)
            
            rotated_image = self.rotate_image_complex(self.original_image, angle)
            self.display_image(rotated_image)
    
    def save_image(self):
        if self.original_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    angle = self.rotation_angle.get()
                    rotated_image = self.rotate_image_complex(self.original_image, angle)
                    rotated_image.save(file_path)
                    messagebox.showinfo("Success", "Image saved successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not save image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRotatorApp(root)
    root.mainloop()