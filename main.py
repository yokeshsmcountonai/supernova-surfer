# import sys
# from PyQt5.QtCore import *
# from PyQt5.QtGui import QKeySequence
# from PyQt5.QtWidgets import *
# from PyQt5.QtWebKitWidgets import QWebView  
# from PyQt5.QtWebKit import QWebSettings

# class MainWindow(QMainWindow):
#     def __init__(self, fullscreen=False):
#         super(MainWindow, self).__init__()

#         self.tabs = QTabWidget()
#         self.tabs.setTabsClosable(True)
#         self.tabs.setMovable(True)
#         self.tabs.tabCloseRequested.connect(self.close_tab)
#         self.setCentralWidget(self.tabs)
         
#         self.resize(1920,1080)
#         # self.resize(2560, 1440)  # QHD (2K)
#         # self.resize(3200, 1800)  # QHD+
#         # self.resize(3440, 1440)  # UltraWide QHD
#         # self.resize(3840, 1600)  # UltraWide 4K
#         # self.resize(3840, 2160)  # 4K UHD
#         # self.resize(5120, 2160)  # UltraWide 5K
#         # self.resize(5120, 2880)  # 5K
#         # self.resize(6016, 3384)  # 6K (Apple Pro Display XDR)
#         # self.resize(7680, 4320)  # 8K UHD
#         self.setMouseTracking(True)
#         self.tabs.setMouseTracking(True)

#         self.disable_cache_and_history()
#         self.create_shortcuts()

#         # Navigation Toolbar
#         self.navbar = QToolBar()
#         self.addToolBar(Qt.TopToolBarArea, self.navbar)
#         self.navbar.setMovable(False)
#         self.navbar.setHidden(fullscreen)

#         # New Tab Button
#         new_tab_btn = QAction("+", self)
#         new_tab_btn.triggered.connect(lambda: self.add_new_tab())
#         self.navbar.addAction(new_tab_btn)

#         # Back Button
#         back_btn = QAction("Back", self)
#         back_btn.triggered.connect(lambda: self.current_browser().back())
#         self.navbar.addAction(back_btn)

#         # Forward Button
#         forward_btn = QAction("Forward", self)
#         forward_btn.triggered.connect(lambda: self.current_browser().forward())
#         self.navbar.addAction(forward_btn)

#         # Reload Button
#         reload_btn = QAction("Reload", self)
#         reload_btn.triggered.connect(lambda: self.current_browser().reload())
#         self.navbar.addAction(reload_btn)

#         # Home Button
#         home_btn = QAction("Home", self)
#         home_btn.triggered.connect(self.navigate_home)
#         self.navbar.addAction(home_btn)

#         # URL Bar
#         self.url_bar = QLineEdit()
#         self.url_bar.returnPressed.connect(self.navigate_to_url)
#         self.url_bar.installEventFilter(self)
#         # self.navbar.addWidget(self.url_bar)
#         nav_layout = QHBoxLayout()
#         nav_layout.addWidget(self.url_bar)
#         nav_container = QWidget()
#         nav_container.setLayout(nav_layout)
#         self.navbar.addWidget(nav_container)


#         # Maximize Button
#         self.maximize_btn = QAction("Maximize", self)
#         self.maximize_btn.triggered.connect(self.toggle_maximize_restore)
#         self.navbar.addAction(self.maximize_btn)

#         # Fullscreen Button
#         fullscreen_btn = QAction("Full Screen", self)
#         fullscreen_btn.triggered.connect(self.toggle_fullscreen)
#         self.navbar.addAction(fullscreen_btn)

#         # Close Browser Button
#         close_btn = QAction("Close", self)
#         close_btn.triggered.connect(self.close_browser)
#         self.navbar.addAction(close_btn)

#         # Open Home Tab
#         self.add_new_tab(QUrl("http://127.0.0.1:8005"), "Home")

#         if fullscreen:
#             self.showFullScreen()
#         else:
#             self.showMaximized()

#         self.is_fullscreen = fullscreen
#         self.is_maximized = True

#     def create_shortcuts(self):
#         shortcuts = {
#             "Ctrl+T": lambda: self.add_new_tab(),
#             "Ctrl+W": lambda: self.close_tab(self.tabs.currentIndex()),
#             "Ctrl+Tab": self.next_tab,
#             "Ctrl+Shift+Tab": self.previous_tab,
#             "Alt+Left": lambda: self.current_browser().back(),
#             "Alt+Right": lambda: self.current_browser().forward(),
#             "Ctrl+R": lambda: self.current_browser().reload(),
#             "Alt+Home": self.navigate_home,
#             "Ctrl+Q": self.close_browser,
#             "F11": self.toggle_maximize_restore,
#             "Ctrl+F": self.toggle_fullscreen,
#         }
        
#         for shortcut, function in shortcuts.items():
#             QShortcut(QKeySequence(shortcut), self).activated.connect(function)

#     def disable_cache_and_history(self):
#         pass

#     def add_new_tab(self, qurl=QUrl("http://127.0.0.1:8005"), label="New Tab"):
#         browser = QWebView()
#         browser.setUrl(qurl)
#         index = self.tabs.addTab(browser, label)
#         self.tabs.setCurrentIndex(index)
        
#         # Update Tab Title When Page Loads
#         browser.titleChanged.connect(lambda: self.update_tab_title(index, browser))
#         browser.urlChanged.connect(lambda q, b=browser: self.update_url(q, b))

#     def update_tab_title(self, index, browser):
#         title = browser.page().mainFrame().title()
#         self.tabs.setTabText(index, title if title else "Loading...")

#     def current_browser(self):
#         return self.tabs.currentWidget()

#     def close_tab(self, index):
#         if self.tabs.count() > 1:
#             self.tabs.removeTab(index)
#         else:
#             self.close_browser()  

#     def navigate_home(self):
#         self.current_browser().setUrl(QUrl("http://127.0.0.1:8005"))

#     def navigate_to_url(self):
#         url = self.url_bar.text()
#         self.current_browser().setUrl(QUrl(url))

#     def update_url(self, q, browser):
#         if browser == self.current_browser():
#             self.url_bar.setText(q.toString())

#     def close_browser(self):
#         self.close()

#     def next_tab(self):
#         index = self.tabs.currentIndex()
#         self.tabs.setCurrentIndex((index + 1) % self.tabs.count())

#     def previous_tab(self):
#         index = self.tabs.currentIndex()
#         self.tabs.setCurrentIndex((index - 1) % self.tabs.count())

#     def eventFilter(self, obj, event):
#         if obj == self.url_bar and event.type() == QEvent.FocusIn:
#             self.show_virtual_keyboard()
#         return super().eventFilter(obj, event)

#     def toggle_maximize_restore(self):
#         if self.is_maximized:
#             self.showNormal()
#             self.maximize_btn.setText("Maximize")
#         else:
#             self.showMaximized()
#             self.maximize_btn.setText("Restore")
#         self.is_maximized = not self.is_maximized

#     def toggle_fullscreen(self):
#         if self.is_fullscreen:
#             self.showNormal()
#             self.navbar.show()
#         else:
#             self.showFullScreen()
#             self.navbar.hide()
#         self.is_fullscreen = not self.is_fullscreen

#     def mouseMoveEvent(self, event):
#         if self.is_fullscreen:
#             if event.pos().y() < 40:  # If mouse is near the top (40px threshold)
#                 self.navbar.show()
#             else:
#                 QTimer.singleShot(1000, self.navbar.hide)  # Hide after 1s if not near the top
#         super().mouseMoveEvent(event)

#     def show_virtual_keyboard(self):
#         QProcess.startDetached("onboard")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     QApplication.setAttribute(Qt.AA_SynthesizeTouchForUnhandledMouseEvents)
#     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
#     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
#     QApplication.setApplicationName("Supernova Surfer")
#     fullscreen = "--fullscreen" in sys.argv  
#     window = MainWindow(fullscreen)
#     app.exec_()



import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import QWebView  
from PyQt5.QtWebKit import QWebSettings
import subprocess

class MainWindow(QMainWindow):
    def __init__(self, fullscreen=False):
        super(MainWindow, self).__init__()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
         
        self.resize(1920, 1080)
        self.setMouseTracking(True)
        self.tabs.setMouseTracking(True)

        self.disable_cache_and_history()
        self.create_shortcuts()

        # Navigation Toolbar
        self.navbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.navbar)
        self.navbar.setMovable(False)
        self.navbar.setHidden(fullscreen)

        self.create_nav_buttons()

        # Open Home Tab
        self.add_new_tab(QUrl("http://127.0.0.1:8005"), "Home")

        if fullscreen:
            self.showFullScreen()
        else:
            self.showMaximized()

        self.is_fullscreen = fullscreen
        self.is_maximized = True

    def create_shortcuts(self):
        shortcuts = {
            "Ctrl+T": lambda: self.add_new_tab(),
            "Ctrl+W": lambda: self.close_tab(self.tabs.currentIndex()),
            "Ctrl+Tab": self.next_tab,
            "Ctrl+Shift+Tab": self.previous_tab,
            "Alt+Left": lambda: self.current_browser().back(),
            "Alt+Right": lambda: self.current_browser().forward(),
            "Ctrl+R": lambda: self.current_browser().reload(),
            "Alt+Home": self.navigate_home,
            "Ctrl+Q": self.close_browser,
            "F11": self.toggle_maximize_restore,
            "Ctrl+F": self.toggle_fullscreen,
            "Escape": self.open_emodeui_js,  # Press Escape to execute emodeui.js
        }
        
        for shortcut, function in shortcuts.items():
            QShortcut(QKeySequence(shortcut), self).activated.connect(function)

    def disable_cache_and_history(self):
        pass

    def create_nav_buttons(self):
        buttons = [
            ("+", self.add_new_tab),
            ("Back", lambda: self.current_browser().back()),
            ("Forward", lambda: self.current_browser().forward()),
            ("Reload", lambda: self.current_browser().reload()),
            ("Home", self.navigate_home),
            ("Maximize", self.toggle_maximize_restore),
            ("Full Screen", self.toggle_fullscreen),
            ("Close", self.close_browser),
        ]

        for text, func in buttons:
            btn = QAction(text, self)
            btn.triggered.connect(func)
            self.navbar.addAction(btn)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.installEventFilter(self)
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.url_bar)
        nav_container = QWidget()
        nav_container.setLayout(nav_layout)
        self.navbar.addWidget(nav_container)

    def add_new_tab(self, qurl=QUrl("http://127.0.0.1:8005"), label="New Tab"):
        browser = QWebView()
        browser.setUrl(qurl)
        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)

        # Update Tab Title When Page Loads
        browser.titleChanged.connect(lambda: self.update_tab_title(index, browser))
        browser.urlChanged.connect(lambda q, b=browser: self.update_url(q, b))

    def update_tab_title(self, index, browser):
        title = browser.page().mainFrame().title()
        self.tabs.setTabText(index, title if title else "Loading...")

    def current_browser(self):
        return self.tabs.currentWidget()

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close_browser()  # Close the browser if it's the last tab

    def navigate_home(self):
        self.current_browser().setUrl(QUrl("http://127.0.0.1:8005"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        self.current_browser().setUrl(QUrl(url))

    def update_url(self, q, browser):
        if browser == self.current_browser():
            self.url_bar.setText(q.toString())

    def close_browser(self):
        self.close()

    def next_tab(self):
        index = self.tabs.currentIndex()
        self.tabs.setCurrentIndex((index + 1) % self.tabs.count())

    def previous_tab(self):
        index = self.tabs.currentIndex()
        self.tabs.setCurrentIndex((index - 1) % self.tabs.count())

    def eventFilter(self, obj, event):
        if obj == self.url_bar and event.type() == QEvent.FocusIn:
            self.show_virtual_keyboard()
        return super().eventFilter(obj, event)

    def toggle_maximize_restore(self):
        if self.is_maximized:
            self.showNormal()
            self.maximize_btn.setText("Maximize")
        else:
            self.showMaximized()
            self.maximize_btn.setText("Restore")
        self.is_maximized = not self.is_maximized

    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.showNormal()
            self.navbar.show()
        else:
            self.showFullScreen()
            self.navbar.hide()
        self.is_fullscreen = not self.is_fullscreen

    def mouseMoveEvent(self, event):
        if self.is_fullscreen:
            if event.pos().y() < 40:  # If mouse is near the top (40px threshold)
                self.navbar.show()
            else:
                QTimer.singleShot(1000, self.navbar.hide)  # Hide after 1s if not near the top
        super().mouseMoveEvent(event)

    def show_virtual_keyboard(self):
        QProcess.startDetached("onboard")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.open_emodeui_js()
        else:
            super().keyPressEvent(event)

    def open_emodeui_js(self):
        js_file = os.path.join(os.getcwd(), "emodeui.js")

        if os.path.exists(js_file):
            try:
                subprocess.Popen(["node", js_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                QMessageBox.information(self, "Execution", "emodeui.js is running!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to execute emodeui.js: {e}")
        else:
            QMessageBox.critical(self, "Error", "emodeui.js not found!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Supernova Surfer")
    fullscreen = "--fullscreen" in sys.argv  
    window = MainWindow(fullscreen)
    app.exec_()
