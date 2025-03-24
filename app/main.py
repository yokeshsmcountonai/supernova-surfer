import atexit
import sys
import time
import signal
import subprocess
from PyQt5.QtCore import Qt, QUrl, QTimer, QEvent
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QLineEdit, QTabWidget, QShortcut
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
# Enable touch events and high-DPI scaling
QApplication.setAttribute(Qt.AA_SynthesizeTouchForUnhandledMouseEvents)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

class MainWindow(QMainWindow):
    def __init__(self, fullscreen=False):
        super(MainWindow, self).__init__()
        
        self.is_fullscreen = fullscreen  
        self.is_maximized = True  
        self.sigint_received = False  
        self.zoom_factor = 1.0  # Default zoom level
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
        self.tabs.setTabBarAutoHide(True)
        
        self.resize(1920, 1080)
        self.setMouseTracking(True)
        self.tabs.setMouseTracking(True)
        self.installEventFilter(self)  # Enable event filtering for hover detection
        
        self.navbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.navbar)
        self.navbar.setMovable(False)
        self.navbar.hide()  # Initially hidden
        self.setup_navbar()
        
        self.create_shortcuts()
        self.add_new_tab(QUrl("http://192.168.0.226:8005"), "Home")
        
        signal.signal(signal.SIGINT, self.handle_sigint)
        signal.signal(signal.SIGTERM, self.handle_sigint)
        
        self.showFullScreen()
       
    def setup_navbar(self):
        """ Sets up the navigation toolbar buttons and URL bar. """
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        self.navbar.addAction(back_btn)
        
        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        self.navbar.addAction(forward_btn)
        
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        self.navbar.addAction(reload_btn)
        
        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        self.navbar.addAction(home_btn)
        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)
        
        new_tab_btn = QAction("+", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        self.navbar.addAction(new_tab_btn)
        
        fullscreen_btn = QAction("Fullscreen", self)
        fullscreen_btn.triggered.connect(self.toggle_fullscreen)
        self.navbar.addAction(fullscreen_btn)
        
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseMove:
            if event.pos().y() < 50 and self.is_fullscreen:
                self.navbar.show()
            elif event.pos().y() > 80 and self.is_fullscreen:
                self.navbar.hide()
        return super().eventFilter(obj, event)
    
    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.current_browser().setUrl(QUrl(url))
    
    # def handle_sigint(self, signum, frame):
    #     print("Ctrl+C detected. Closing browser cleanly.")
    #     self.sigint_received = True
    #     self.close_browser()
    
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close_browser()
    # def handle_sigint(self, signum, frame):
    #     """ Handle Ctrl+C (SIGINT) to stop the application immediately. """
    #     print("Ctrl+C detected. Stopping browser completely.")
    #     self.sigint_received = True
    #     QApplication.quit()  # Quit PyQt application
    #     sys.exit(0)  # Ensure full exit


    def handle_sigint(self, signum, frame):
        """ Handle Ctrl+C to stop the application completely. """
        print("Ctrl+C detected. Stopping browser completely.")

        os.environ["BROWSER_STOPPED"] = "1"  # Set stop flag
        self.sigint_received = True
        QApplication.quit()
        sys.exit(0)

    

    def closeEvent(self, event):
        """ Ensure restart on window close unless manually stopped """
        if self.sigint_received:  
            print("Manual close detected. Exiting...")
            QApplication.quit()
            sys.exit(0)
        else:
            print("Window closed. Restarting in 10 seconds...")
            event.ignore()  # Prevent default close action
            self.close_browser()  # Call custom close logic
    
    
    def close_browser(self):
        """ Closes the browser and schedules a restart unless manually stopped. """
        print("Browser closed. Restarting in 10 seconds...")

        if self.sigint_received:  # Stop restarting if manually closed
            print("Browser stopped manually. Exiting...")
            QApplication.quit()
            sys.exit(0)

        # Delay restart by 10 seconds
        QTimer.singleShot(10000, self.restart_browser)
        print("restarted")
        # Hide the application window but don't exit
        self.hide()


    # def restart_browser(self):
    #     """ Restarts the browser process unless manually stopped. """
    #     if self.sigint_received:  # Double-check before restarting
    #         print("Manual stop detected. Not restarting.")
    #         sys.exit(0)

    #     print("Restarting browser...")
    #     QProcess.startDetached(sys.executable, sys.argv)
    #     sys.exit(0)

    def restart_browser(self):
        """ Restarts the browser process unless manually stopped. """
        
        if os.getenv("BROWSER_STOPPED") == "1":
            print("Manual stop detected. Not restarting.")
            sys.exit(0)

        print("Restarting browser...")
        QProcess.startDetached(sys.executable, sys.argv)
        sys.exit(0)
       
    def create_shortcuts(self):
        shortcuts = {
            "Ctrl+T": lambda: self.add_new_tab(),
            "Ctrl+W": lambda: self.close_tab(self.tabs.currentIndex()),
            "Ctrl+R": lambda: self.current_browser().reload(),
            "F11": self.toggle_fullscreen,
            "Ctrl++": self.increase_zoom,
            "Ctrl+-": self.decrease_zoom,
        }
        
        for shortcut, function in shortcuts.items():
            QShortcut(QKeySequence(shortcut), self).activated.connect(function)
    
    def add_new_tab(self, qurl=QUrl("http://192.168.0.226:8005"), label="New Tab"):
        browser = QWebEngineView()
        browser.setUrl(qurl)
        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)
        browser.setZoomFactor(self.zoom_factor)
    
    def current_browser(self):
        return self.tabs.currentWidget()
    
    def navigate_home(self):
        self.current_browser().setUrl(QUrl("http://192.168.0.226:8005"))
    
    def toggle_fullscreen(self):
        if self.is_fullscreen:
            self.showNormal()
            self.navbar.show()
        else:
            self.showFullScreen()
            self.navbar.hide()
        self.is_fullscreen = not self.is_fullscreen
    
    def increase_zoom(self):
        self.zoom_factor += 0.1
        self.current_browser().setZoomFactor(self.zoom_factor)
    
    def decrease_zoom(self):
        self.zoom_factor = max(0.5, self.zoom_factor - 0.1)
        self.current_browser().setZoomFactor(self.zoom_factor)

    

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Supernova Surfer")
    
    window = MainWindow(fullscreen=True)
    sys.exit(app.exec_())

