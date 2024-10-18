import tkinter as tk
import subprocess
from tkinter import messagebox
from datetime import datetime, timedelta

class ShutdownApp:
    def __init__(self, window):
        self.window = window
        self.window.title("定时关机工具")
        self.window.geometry("240x320")  # 调整窗口大小以适应新按钮 长*宽

        self.create_widgets()
        self.update_current_time()

    def create_widgets(self):
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)

        self.current_time_label = tk.Label(frame, text="")
        self.current_time_label.grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(frame, text="设置关机时间:").grid(row=1, column=0, pady=5)

        tk.Label(frame, text="小时 (0-23):").grid(row=2, column=0, pady=5)
        self.hours_entry = tk.Entry(frame, width=10)
        self.hours_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="分钟 (0-59):").grid(row=3, column=0, pady=5)
        self.minutes_entry = tk.Entry(frame, width=10)
        self.minutes_entry.grid(row=3, column=1, pady=5)

        tk.Label(frame, text="秒 (0-59):").grid(row=4, column=0, pady=5)
        self.seconds_entry = tk.Entry(frame, width=10)
        self.seconds_entry.grid(row=4, column=1, pady=5)

        self.shutdown_time_label = tk.Label(frame, text="关机时间: 尚未设置")
        self.shutdown_time_label.grid(row=5, column=0, columnspan=2, pady=5)

        tk.Button(frame, text="设置关机", command=self.schedule_shutdown).grid(row=6, column=0, pady=5)
        tk.Button(frame, text="取消关机", command=self.cancel_shutdown).grid(row=6, column=1, pady=5)

        # 新增立即关机按钮
        tk.Button(frame, text="立即关机", command=self.immediate_shutdown).grid(row=7, column=0, columnspan=2, pady=5)

    def update_current_time(self):
        self.current_time_label.config(
            text=f"当前时间: {datetime.now().strftime('%H:%M:%S')}")
        self.window.after(1000, self.update_current_time)

    def schedule_shutdown(self):
        try:
            hours = int(self.hours_entry.get())
            minutes = int(self.minutes_entry.get())
            seconds = int(self.seconds_entry.get())

            if not (0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60):
                raise ValueError("时间输入无效，请检查输入格式。")

            current_time = datetime.now()
            target_time = current_time.replace(hour=hours, minute=minutes, second=seconds)

            if target_time <= current_time:
                target_time += timedelta(days=1)

            delta = target_time - current_time
            total_seconds = int(delta.total_seconds())

            self.shutdown_time_label.config(
                text=f"关机时间: {target_time.strftime('%H:%M:%S')}")

            subprocess.run(["shutdown", "-s", "-t", str(total_seconds)], check=True)
            messagebox.showinfo("成功", f"电脑将在 {total_seconds} 秒后关机。")

        except ValueError as e:
            messagebox.showerror("错误", str(e))
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"无法设置关机：{e}")

    def cancel_shutdown(self):
        try:
            subprocess.run(["shutdown", "-a"], check=True)
            self.shutdown_time_label.config(text="关机时间: 已取消")
            messagebox.showinfo("成功", "已取消关机计划。")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"无法取消关机：{e}")

    def immediate_shutdown(self):
        try:
            subprocess.run(["shutdown", "-s", "-t", "0"], check=True)
            messagebox.showinfo("成功", "电脑将在立即关机。")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"无法立即关机：{e}")

def main():
    """
    程序的主入口函数。
    
    Args:
        无
    
    Returns:
        无
    
    """
    window = tk.Tk()
    app = ShutdownApp(window)
    window.mainloop()

if __name__ == "__main__":
    main()
