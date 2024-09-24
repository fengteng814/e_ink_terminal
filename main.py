# main.py
# 启动脚本，负责启动Flask应用和GUI应用的线程
import threading
import app
import gui

def run_flask():
    # 运行Flask应用
    app.app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)

def run_gui_app():
    # 运行GUI应用
    gui.run_gui()

if __name__ == '__main__':
    # 创建Flask应用线程
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # 设置为守护线程，主线程结束时自动退出
    flask_thread.start()

    # 运行GUI应用（主线程）
    run_gui_app()
