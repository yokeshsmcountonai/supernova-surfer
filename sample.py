import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import QWebView  
from PyQt5.QtWebKit import QWebSettings
import subprocess

class MainWindow(QMainWindow):
    def __init__(self, fullscreen=False):
        super(MainWindow, self).__init__()

        # Initialize fullscreen state BEFORE calling add_new_tab()
        self.is_fullscreen = fullscreen  
        self.is_maximized = True  

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
        self.tabs.setTabBarAutoHide(True)
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

        self.setup_navbar()

        # Open Home Tab
        self.add_new_tab(QUrl("http://127.0.0.1:8005"), "Home")

        if fullscreen:
            self.showFullScreen()
        else:
            self.showMaximized()

    def setup_navbar(self):
        """ Sets up the navigation toolbar buttons and URL bar. """
        new_tab_btn = QAction("+", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        self.navbar.addAction(new_tab_btn)

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
        self.url_bar.installEventFilter(self)
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.url_bar)
        nav_container = QWidget()
        nav_container.setLayout(nav_layout)
        self.navbar.addWidget(nav_container)

        maximize_btn = QAction("Maximize", self)
        maximize_btn.triggered.connect(self.toggle_maximize_restore)
        self.navbar.addAction(maximize_btn)

        fullscreen_btn = QAction("Full Screen", self)
        fullscreen_btn.triggered.connect(self.toggle_fullscreen)
        self.navbar.addAction(fullscreen_btn)

        close_btn = QAction("Close", self)
        close_btn.triggered.connect(self.close_browser)
        self.navbar.addAction(close_btn)

    def create_shortcuts(self):
        """ Sets up keyboard shortcuts for navigation. """
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
        }
        
        for shortcut, function in shortcuts.items():
            QShortcut(QKeySequence(shortcut), self).activated.connect(function)

    def disable_cache_and_history(self):
        pass

    def add_new_tab(self, qurl=QUrl("http://127.0.0.1:8005"), label="New Tab"):
        """ Adds a new tab to the browser. """
        browser = QWebView()
        browser.setUrl(qurl)
        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)
        
        if self.is_fullscreen:
            self.tabs.setTabBarAutoHide(False)
            self.tabs.tabBar().hide()
        
        browser.titleChanged.connect(lambda: self.update_tab_title(index, browser))
        browser.urlChanged.connect(lambda q, b=browser: self.update_url(q, b))

    def update_tab_title(self, index, browser):
        title = browser.page().mainFrame().title()
        self.tabs.setTabText(index, title if title else "Loading...")

    def current_browser(self):
        return self.tabs.currentWidget()

    def close_tab(self, index):
        """ Closes a tab, or exits the browser if it's the last one. """
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close_browser()  

    def navigate_home(self):
        """ Navigates the current tab to the home URL. """
        self.current_browser().setUrl(QUrl("http://127.0.0.1:8005"))

    def navigate_to_url(self):
        """ Navigates the current tab to the entered URL. """
        url = self.url_bar.text()
        self.current_browser().setUrl(QUrl(url))

    def update_url(self, q, browser):
        """ Updates the URL bar when navigation occurs. """
        if browser == self.current_browser():
            self.url_bar.setText(q.toString())

    def close_browser(self):
        """ Closes the browser and restarts it after 10 seconds. """
        self.close()
        print("Last tab closed. Restarting in 10 seconds...")
        time.sleep(10)
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit() 

    def next_tab(self):
        """ Switches to the next tab. """
        index = self.tabs.currentIndex()
        self.tabs.setCurrentIndex((index + 1) % self.tabs.count())

    def previous_tab(self):
        """ Switches to the previous tab. """
        index = self.tabs.currentIndex()
        self.tabs.setCurrentIndex((index - 1) % self.tabs.count())

    def eventFilter(self, obj, event):
        if obj == self.url_bar and event.type() == QEvent.FocusIn:
            self.show_virtual_keyboard()
        return super().eventFilter(obj, event)

    def toggle_maximize_restore(self):
        """ Toggles between maximized and normal window states. """
        if self.is_maximized:
            self.showNormal()
        else:
            self.showMaximized()
        self.is_maximized = not self.is_maximized

    def toggle_fullscreen(self):
        """ Toggles fullscreen mode and hides/shows the navbar and tab bar. """
        if self.is_fullscreen:
            self.showNormal()
            self.navbar.show()
            self.tabs.setTabBarAutoHide(True)
            self.tabs.tabBar().show()
        else:
            self.showFullScreen()
            self.navbar.hide()
            self.tabs.setTabBarAutoHide(False)
            self.tabs.tabBar().hide()
        self.is_fullscreen = not self.is_fullscreen

    def mouseMoveEvent(self, event):
        """ Shows navbar when the mouse moves near the top in fullscreen mode. """
        if self.is_fullscreen:
            if event.pos().y() < 40:
                self.navbar.show()
            else:
                QTimer.singleShot(1000, self.navbar.hide)
        super().mouseMoveEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setAttribute(Qt.AA_SynthesizeTouchForUnhandledMouseEvents)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setApplicationName("Supernova Surfer")

    window = MainWindow(fullscreen=True)  
    app.exec_()


it is consuming more cpu usage how can i manage it what will be the reason