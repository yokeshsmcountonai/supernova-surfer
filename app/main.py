import gi
import sys
import signal
import time
from gi.repository import Gtk, WebKit2, GLib, Gdk

class Browser(Gtk.Window):
    def __init__(self):
        super().__init__(title="Supernova Surfer")
        self.set_default_size(1920, 1080)
        
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        
        self.navbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.setup_navbar()
        
        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)
        self.notebook.set_show_tabs(False)  # Hide tab bar
        self.vbox.pack_start(self.navbar, False, False, 0)
        self.vbox.pack_start(self.notebook, True, True, 0)
        
        self.add_new_tab("http://192.168.0.226:8005", "Home")
        
        self.fullscreen_mode = True
        self.ui_hidden = True
        self.toggle_fullscreen()
        
        self.connect("motion-notify-event", self.on_mouse_move)
        self.connect("destroy", self.on_close)  # Detect window close
        
        signal.signal(signal.SIGINT, self.handle_sigint)
        signal.signal(signal.SIGTERM, self.handle_sigint)
    
    def setup_navbar(self):
        back_btn = Gtk.Button(label="Back")
        back_btn.connect("clicked", lambda _: self.current_browser().go_back())
        
        forward_btn = Gtk.Button(label="Forward")
        forward_btn.connect("clicked", lambda _: self.current_browser().go_forward())
        
        reload_btn = Gtk.Button(label="Reload")
        reload_btn.connect("clicked", lambda _: self.current_browser().reload())
        
        self.url_bar = Gtk.Entry()
        self.url_bar.set_placeholder_text("Enter URL")
        self.url_bar.connect("activate", self.navigate_to_url)
        
        new_tab_btn = Gtk.Button(label="+")
        new_tab_btn.connect("clicked", lambda _: self.add_new_tab())
        
        fullscreen_btn = Gtk.Button(label="Fullscreen")
        fullscreen_btn.connect("clicked", self.toggle_fullscreen)
        
        self.navbar.pack_start(back_btn, False, False, 5)
        self.navbar.pack_start(forward_btn, False, False, 5)
        self.navbar.pack_start(reload_btn, False, False, 5)
        self.navbar.pack_start(self.url_bar, True, True, 5)
        self.navbar.pack_start(new_tab_btn, False, False, 5)
        self.navbar.pack_start(fullscreen_btn, False, False, 5)
    
    def add_new_tab(self, url="http://192.168.0.226:8005", label="New Tab"):
        webview = WebKit2.WebView()
        webview.load_uri(url)
        webview.connect("load-changed", self.update_url_bar)
        
        tab_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        tab_box.pack_start(webview, True, True, 0)
        
        self.notebook.append_page(tab_box)
        self.notebook.set_current_page(-1)
        self.show_all()
    
    def navigate_to_url(self, _):
        url = self.url_bar.get_text()
        if not url.startswith("http"):
            url = "http://" + url
        self.current_browser().load_uri(url)
    
    def toggle_fullscreen(self, _=None):
        if self.fullscreen_mode:
            self.unfullscreen()
            self.navbar.show()
        else:
            self.fullscreen()
            self.navbar.hide()
            self.ui_hidden = True
        self.fullscreen_mode = not self.fullscreen_mode
    
    def update_url_bar(self, webview, event):
        if event == WebKit2.LoadEvent.COMMITTED:
            self.url_bar.set_text(webview.get_uri())
    
    def current_browser(self):
        tab_content = self.notebook.get_nth_page(self.notebook.get_current_page())
        return tab_content.get_children()[0]  # WebView is the only child
    
    def on_mouse_move(self, widget, event):
        if self.fullscreen_mode:
            if event.y < 50 and self.ui_hidden:
                self.navbar.show()
                self.ui_hidden = False
            elif event.y > 80 and not self.ui_hidden:
                self.navbar.hide()
                self.ui_hidden = True
    
    def on_close(self, widget):
        """ Handle window close event and restart after 10 seconds """
        print("Browser closed. Restarting in 10 seconds...")
        Gtk.main_quit()
        time.sleep(10)
        main_loop()
    
    def handle_sigint(self, signum, frame):
        print("SIGINT received. Exiting...")
        Gtk.main_quit()
        sys.exit(0)

def main_loop():
    while True:
        try:
            app = Browser()
            Gtk.main()
        except Exception as e:
            print(f"Browser crashed with error: {e}. Restarting in 10 seconds...")
            time.sleep(10)  # Wait 10 seconds before restarting

if __name__ == "__main__":
    main_loop()
