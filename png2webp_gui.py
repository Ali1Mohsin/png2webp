import os
import threading
import subprocess
import platform
import gc
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image

# 禁用 Pillow 像素限制以处理大图
Image.MAX_IMAGE_PIXELS = None


class ModernConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("PNG to WebP Converter v1.0")
        self.root.geometry("650x390")
        self.root.resizable(False, False)
        self.style = ttk.Style(theme="flatly")

        # 变量初始化
        self.input_path = ttk.StringVar()
        self.output_path = ttk.StringVar()
        self.selected_files = []
        self.quality = ttk.IntVar(value=80)
        self.suffix = ttk.StringVar(value="")
        self.is_lossless = ttk.BooleanVar(value=False)
        self.auto_open = ttk.BooleanVar(value=True)

        self.setup_ui()

    def update_quality_label(self, val):
        """核心修复：手动将滑块值取整并更新 IntVar"""
        rounded_val = int(float(val))
        self.quality.set(rounded_val)

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20 10 20 5")
        main_frame.pack(fill=X)

        # --- 路径设置 ---
        path_group = ttk.LabelFrame(main_frame, text="路径设置")
        path_group.pack(fill=X, pady=5)
        path_inner = ttk.Frame(path_group, padding=10)
        path_inner.pack(fill=X, expand=YES)

        ttk.Label(path_inner, text="输入路径:").grid(row=0, column=0, sticky=W, pady=5)
        ttk.Entry(path_inner, textvariable=self.input_path, width=45).grid(row=0, column=1, padx=(10, 5))

        btn_fm = ttk.Frame(path_inner)
        btn_fm.grid(row=0, column=2, sticky=EW)
        ttk.Button(btn_fm, text="文件", bootstyle=(INFO, OUTLINE), command=self.select_files, width=6).pack(side=LEFT,
                                                                                                            padx=2)
        ttk.Button(btn_fm, text="目录", bootstyle=(INFO, OUTLINE), command=self.select_folder, width=6).pack(side=LEFT,
                                                                                                             padx=2)

        ttk.Label(path_inner, text="输出目录:").grid(row=1, column=0, sticky=W, pady=5)
        ttk.Entry(path_inner, textvariable=self.output_path, width=45).grid(row=1, column=1, padx=(10, 5))

        out_btn_fm = ttk.Frame(path_inner)
        out_btn_fm.grid(row=1, column=2, sticky=EW)
        # 修正颜色：与上方一致
        ttk.Button(out_btn_fm, text="浏览", bootstyle=(INFO, OUTLINE), command=self.select_output_dir).pack(fill=X,
                                                                                                            padx=2)

        path_inner.grid_columnconfigure(1, weight=1)

        # --- 转换参数 ---
        param_group = ttk.LabelFrame(main_frame, text="转换参数调节")
        param_group.pack(fill=X, pady=5)

        param_inner = ttk.Frame(param_group, padding=10)
        param_inner.pack(fill=X, expand=YES)

        ttk.Label(param_inner, text="压缩质量:").grid(row=0, column=0, sticky=W)
        # 核心修复：移除不支持的 resolution，改用 command 实时取整
        self.q_scale = ttk.Scale(
            param_inner, from_=1, to=100,
            bootstyle=INFO,
            command=self.update_quality_label
        )
        self.q_scale.set(80)  # 设置初始值
        self.q_scale.grid(row=0, column=1, sticky=EW, padx=10, pady=5)
        ttk.Label(param_inner, textvariable=self.quality).grid(row=0, column=2)

        ttk.Label(param_inner, text="文件名后缀:").grid(row=1, column=0, sticky=W)
        ttk.Entry(param_inner, textvariable=self.suffix, width=15).grid(row=1, column=1, sticky=W, padx=10)
        ttk.Label(param_inner, text="(例如: _min)", font=("TkDefaultFont", 9), foreground="gray").grid(row=1, column=1,
                                                                                                       padx=(130, 0),
                                                                                                       sticky=W)

        param_inner.grid_columnconfigure(1, weight=1)

        # 选项
        opt_frame = ttk.Frame(main_frame)
        opt_frame.pack(fill=X, pady=2, padx=20)
        ttk.Checkbutton(opt_frame, text="无损模式 (巨图慎选)", variable=self.is_lossless,
                        bootstyle="round-toggle").pack(side=LEFT, padx=5)
        ttk.Checkbutton(opt_frame, text="完成后打开文件夹", variable=self.auto_open, bootstyle="round-toggle").pack(
            side=LEFT, padx=30)

        # --- 进度执行 ---
        self.progress = ttk.Progressbar(main_frame, bootstyle=SUCCESS, mode=DETERMINATE)
        self.progress.pack(fill=X, pady=2, padx=20)
        self.status_label = ttk.Label(main_frame, text="等待操作...", font=("TkDefaultFont", 8))
        self.status_label.pack(pady=1)

        self.start_btn = ttk.Button(main_frame, text="Start Conversion Task", bootstyle=SUCCESS,
                                    command=self.start_thread, width=30)
        self.start_btn.pack(pady=(2, 10))

    # --- 逻辑处理 ---
    def select_files(self):
        files = filedialog.askopenfilenames(title="选择 PNG 图片", filetypes=[("PNG图片", "*.png")])
        if files:
            self.selected_files = list(files)
            self.input_path.set(f"已选择 {len(files)} 个文件")
            if not self.output_path.get(): self.output_path.set(os.path.dirname(files[0]))

    def select_folder(self):
        path = filedialog.askdirectory(title="选择输入文件夹")
        if path:
            self.selected_files = []
            self.input_path.set(path)
            if not self.output_path.get(): self.output_path.set(path)

    def select_output_dir(self):
        path = filedialog.askdirectory(title="选择输出文件夹")
        if path: self.output_path.set(path)

    def start_thread(self):
        if not self.input_path.get() or not self.output_path.get():
            messagebox.showwarning("提示", "请先选择输入和输出目录")
            return
        threading.Thread(target=self.process, daemon=True).start()

    def process(self):
        in_val = self.input_path.get()
        out_dir = self.output_path.get()
        tasks = self.selected_files if self.selected_files else [os.path.join(in_val, f) for f in os.listdir(in_val) if
                                                                 f.lower().endswith('.png')]

        if not tasks:
            messagebox.showinfo("提示", "未找到可处理的图片")
            return
        if not os.path.exists(out_dir): os.makedirs(out_dir)

        self.start_btn.config(state=DISABLED)
        total = len(tasks)
        success = 0
        for i, file_path in enumerate(tasks):
            try:
                img = Image.open(file_path)
                save_params = {"format": "WEBP", "lossless": self.is_lossless.get(), "quality": self.quality.get(),
                               "method": 0}
                img.save(os.path.join(out_dir,
                                      f"{os.path.splitext(os.path.basename(file_path))[0]}{self.suffix.get()}.webp"),
                         **save_params)
                img.close()
                success += 1
                self.progress['value'] = ((i + 1) / total) * 100
                self.status_label.config(text=f"进度: {i + 1}/{total} - {os.path.basename(file_path)}")
                self.root.update_idletasks()
                gc.collect()
            except Exception as e:
                print(f"Error: {e}")

        self.start_btn.config(state=NORMAL)
        self.status_label.config(text="转换完成！")
        if self.auto_open.get(): self.open_folder(out_dir)
        messagebox.showinfo("成功", f"任务已完成！\n成功: {success} 张")

    def open_folder(self, path):
        sys_type = platform.system()
        if sys_type == "Windows":
            os.startfile(path)
        else:
            subprocess.Popen(["open" if sys_type == "Darwin" else "xdg-open", path])


if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = ModernConverter(root)
    root.mainloop()