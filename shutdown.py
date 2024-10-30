import tkinter as tk
import subprocess
from tkinter import messagebox
from datetime import datetime, timedelta
import threading
import time

class ShutdownApp:
    def __init__(self, window):
        self.window = window
        self.window.title("定时关机工具")
        self.window.geometry("240x360")  # 调整窗口大小以适应新按钮

        self.create_widgets()
        self.update_current_time()
        self.shutdown_scheduled = False
        self.shutdown_thread = None

    def create_widgets(self):
        """
        创建窗口小部件。
    
        Args:
            无
    
        Returns:
            无
    
        """
        # 创建一个Frame容器，用于放置所有小部件
        frame = tk.Frame(self.window, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)

        # 创建一个Label小部件，用于显示当前时间
        self.current_time_label = tk.Label(frame, text="")
        self.current_time_label.grid(row=0, column=0, columnspan=2, pady=5)  # 在第一行跨两列显示

        # 创建一个Label小部件，用于显示“设置关机时间:”
        tk.Label(frame, text="设置关机时间:").grid(row=1, column=0, pady=5)  # 在第二行第一列显示

        # 创建一个Label小部件，用于显示“小时 (0-23):”
        tk.Label(frame, text="小时 (0-23):").grid(row=2, column=0, pady=5)  # 在第三行第一列显示
        # 创建一个Entry小部件，用于输入小时数
        self.hours_entry = tk.Entry(frame, width=10)
        self.hours_entry.grid(row=2, column=1, pady=5)  # 在第三行第二列显示

        # 创建一个Label小部件，用于显示“分钟 (0-59):”
        tk.Label(frame, text="分钟 (0-59):").grid(row=3, column=0, pady=5)  # 在第四行第一列显示
        # 创建一个Entry小部件，用于输入分钟数
        self.minutes_entry = tk.Entry(frame, width=10)
        self.minutes_entry.grid(row=3, column=1, pady=5)  # 在第四行第二列显示

        # 创建一个Label小部件，用于显示“秒 (0-59):”
        tk.Label(frame, text="秒 (0-59):").grid(row=4, column=0, pady=5)  # 在第五行第一列显示
        # 创建一个Entry小部件，用于输入秒数
        self.seconds_entry = tk.Entry(frame, width=10)
        self.seconds_entry.grid(row=4, column=1, pady=5)  # 在第五行第二列显示

        # 创建一个Label小部件，用于显示关机时间
        self.shutdown_time_label = tk.Label(frame, text="关机时间: 尚未设置")
        self.shutdown_time_label.grid(row=5, column=0, columnspan=2, pady=5)  # 在第六行跨两列显示

        # 创建一个Button小部件，用于设置关机时间
        tk.Button(frame, text="设置关机", command=self.schedule_shutdown).grid(row=6, column=0, pady=5)  # 在第七行第一列显示
        # 创建一个Button小部件，用于取消关机计划
        tk.Button(frame, text="取消关机", command=self.cancel_shutdown).grid(row=6, column=1, pady=5)  # 在第七行第二列显示

        # 新增立即关机按钮
        tk.Button(frame, text="立即关机", command=self.immediate_shutdown).grid(row=7, column=0, pady=5)  # 在第八行第一列显示

        # 新增获取定时时间按钮
        tk.Button(frame, text="获取定时时间", command=self.get_remaining_time).grid(row=7, column=1, pady=5)  # 在第八行第二列显示

        # 新增一个Label小部件，用于显示离定时关机还有多久
        self.remaining_time_label = tk.Label(frame, text="离关机还有: 尚未设置")
        self.remaining_time_label.grid(row=8, column=0, columnspan=2, pady=5)  # 在第九行跨两列显示

    def update_current_time(self):
        """
        更新当前时间。
        
        Args:
            无
        
        Returns:
            无
        
        """
        self.current_time_label.config(
            text=f"当前时间: {datetime.now().strftime('%H:%M:%S')}")
        self.window.after(1000, self.update_current_time)

    def schedule_shutdown(self):
        """
        安排电脑在指定时间关机。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        Raises:
            ValueError: 如果输入的时间无效（即小时不在0-23之间，分钟或秒不在0-59之间）。
            subprocess.CalledProcessError: 如果无法执行关机命令。
        
        """
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

            self.shutdown_scheduled = True
            self.shutdown_thread = threading.Thread(target=self.update_remaining_time, args=(total_seconds,))
            self.shutdown_thread.start()

        except ValueError as e:
            messagebox.showerror("错误", str(e))
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"无法设置关机：{e}")

    def cancel_shutdown(self):
        """
        取消关机计划。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        Raises:
            subprocess.CalledProcessError: 如果取消关机计划失败，则抛出此异常。
        
        """
        try:
            subprocess.run(["shutdown", "-a"], check=True)
            self.shutdown_time_label.config(text="关机时间: 已取消")
            self.remaining_time_label.config(text="离关机还有: 已取消")
            messagebox.showinfo("成功", "已取消关机计划。")
            self.shutdown_scheduled = False
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"无法取消关机：{e}")

    def immediate_shutdown(self):
        try:
            subprocess.run(["shutdown", "-s", "-t", "0"], check=True)
            messagebox.showinfo("成功", "电脑将在立即关机。")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"无法立即关机：{e}")

    def get_remaining_time(self):
        """
        获取并显示离定时关机还有多久。
        
        Args:
            无参数。
        
        Returns:
            无返回值。
        
        """
        if self.shutdown_scheduled:
            self.shutdown_thread.join()
        else:
            messagebox.showinfo("提示", "尚未设置关机时间。")

    def update_remaining_time(self, total_seconds):
        """
        更新离定时关机还有多久。
        
        Args:
            total_seconds (int): 总秒数。
        
        Returns:
            无返回值。
        
        """
        while total_seconds > 0:
            self.remaining_time_label.config(text=f"离关机还有: {total_seconds} 秒")
            total_seconds -= 1
            self.window.update()
            time.sleep(1)

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
