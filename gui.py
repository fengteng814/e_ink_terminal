import tkinter as tk
from tkinter import scrolledtext
from tkinter import font as tkfont
from tkinter import messagebox
from message_queue import message_queue
import weixin_sender  # 引入发送微信消息的模块
from homework_records import homework_records, HomeworkRecord
import time


def run_gui():
    global homework_records

    root = tk.Tk()
    root.title("作业管理")
    root.geometry("500x400")

    # 设置自定义字体
    custom_font = tkfont.Font(family="Arial", size=14, weight="bold")

    # 添加标题标签
    title_label = tk.Label(root, text="作业\nHomework", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    # 添加更新时间标签
    update_time_label = tk.Label(root, text="", font=("Helvetica", 10))
    update_time_label.pack(pady=5)   

    # 创建一个框架用于放置复选框和文本区域
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # 创建一个垂直滚动条
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 创建一个框架用于放置复选框
    checkbox_frame = tk.Frame(frame)
    checkbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 创建一个滚动文本区域
    text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=custom_font, fg="blue", bg="lightyellow", state='disabled', yscrollcommand=scrollbar.set, spacing3=10)
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar.config(command=text_area.yview)

    # 保存复选框和作业内容的列表
    checkboxes = []

    def update_gui():
        nonlocal checkboxes

        while not message_queue.empty():
            user_id, content = message_queue.get()

            # 清空文本区域和复选框记录
            text_area.config(state='normal')
            text_area.delete(1.0, tk.END)

            for checkbox in checkboxes:
                checkbox[0].destroy()
            checkboxes.clear()

            # 准备显示文本
            homework_records.clear()  # 清空记录
            for line in content.splitlines():
                record = HomeworkRecord(line)
                homework_records.append(record)

                var = tk.IntVar(value=int(record.completed))  # 设置初始值

                # 创建复选框
                checkbox = tk.Checkbutton(checkbox_frame, variable=var, pady=2.9,
                                           command=lambda var=var, record=record: on_checkbox_click(var, record))
                checkbox.pack(anchor='w')  # 左对齐
                checkboxes.append((checkbox, var))  # 保存复选框和变量的元组

                # 在文本区域显示作业内容
                text_area.insert(tk.END, f"{record.content}\n")

            # 更新时间标签
            current_time = time.strftime("%A %H:%M", time.localtime())
            update_time_label.config(text=f"更新时间: {current_time}")
            
            # 使文本区域不可编辑
            text_area.config(state='disabled')

            # 自动滚动到最新消息
            text_area.yview(tk.END)

        root.after(1000, update_gui)  # 每秒检查一次

    def on_checkbox_click(var, record):
        record.completed = var.get() == 1  # 切换完成状态
        if record.completed:  # 复选框被勾选
            weixin_sender.send_message("op0im6mAyuSX3VSALrBo1bQhlsPs", f"{record.content} 完成了")
            messagebox.showinfo("完成", f"已标记为完成：{record.content}")
        else:  # 复选框被取消勾选
            weixin_sender.send_message("op0im6mAyuSX3VSALrBo1bQhlsPs", f"{record.content} 未完成")

    update_gui()
    root.mainloop()

if __name__ == "__main__":
    run_gui()

