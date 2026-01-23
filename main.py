import subprocess
import os
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib

OPERATOR_SDK_DIR = "/opt/operator-sdk"
OPERATOR_SDK_BIN = "/usr/local/bin/operator-sdk"

class OperatorSDKApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(application_id="com.austincunningham.operatorsdk", **kwargs)

    def do_activate(self):
        # Force dark color scheme to match logo
        style_manager = Adw.StyleManager.get_default()
        style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        
        # The Window
        self.win = Adw.ApplicationWindow(application=self)
        self.win.set_title("Operator SDK Switcher")
        self.win.set_default_size(450, 520)
        
        # Set application icon
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_theme = Gtk.IconTheme.get_for_display(self.win.get_display())
        icon_theme.add_search_path(script_dir)
        
        # Set the window icon (icon file: com.austincunningham.operatorsdk.svg)
        self.win.set_icon_name("com.austincunningham.operatorsdk")
        
        # Apply custom dark theme CSS matching logo background (#1a1a2e)
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            window, .background {
                background-color: #1a1a2e;
            }
            headerbar {
                background-color: #1a1a2e;
                border-bottom: 1px solid #3a3a5c;
                box-shadow: none;
            }
            .card, frame {
                background-color: #252542;
                border-color: #3a3a5c;
            }
            .suggested-action {
                background-color: #CC0000;
                color: white;
            }
            .suggested-action:hover {
                background-color: #ee2222;
            }
            entry {
                background-color: #252542;
                border-color: #3a3a5c;
            }
            dropdown button {
                background-color: #252542;
                border-color: #3a3a5c;
            }
            windowcontrols button {
                color: white;
            }
            windowcontrols button:hover {
                background-color: #CC0000;
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            self.win.get_display(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Create toolbar view with header bar
        toolbar_view = Adw.ToolbarView()
        self.win.set_content(toolbar_view)
        
        # Header bar with close button (draggable by default)
        header_bar = Adw.HeaderBar()
        header_bar.set_show_end_title_buttons(True)  # Shows close button
        header_bar.set_show_start_title_buttons(False)  # Hide left side buttons
        header_bar.set_title_widget(Gtk.Label(label=""))  # Empty title (logo is below)
        toolbar_view.add_top_bar(header_bar)
        
        # Main Layout
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)
        toolbar_view.set_content(box)

        # Logo header
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        header_box.set_halign(Gtk.Align.CENTER)
        
        # Load and display the logo
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, "logo.svg")
        
        if os.path.exists(logo_path):
            logo = Gtk.Picture.new_for_filename(logo_path)
            logo.set_size_request(200, 70)
            logo.set_content_fit(Gtk.ContentFit.CONTAIN)
            header_box.append(logo)
        
        # Subtitle
        subtitle = Gtk.Label(label="Version Manager")
        subtitle.add_css_class("title-4")
        header_box.append(subtitle)
        
        box.append(header_box)

        # Current version section
        current_frame = Gtk.Frame(label="Current Version")
        current_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        current_box.set_margin_top(10)
        current_box.set_margin_bottom(10)
        current_box.set_margin_start(10)
        current_box.set_margin_end(10)
        current_frame.set_child(current_box)
        
        self.current_label = Gtk.Label(label="Checking...")
        self.current_label.set_halign(Gtk.Align.START)
        current_box.append(self.current_label)
        box.append(current_frame)

        # Available versions section
        available_frame = Gtk.Frame(label="Switch to Installed Version")
        available_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        available_box.set_margin_top(10)
        available_box.set_margin_bottom(10)
        available_box.set_margin_start(10)
        available_box.set_margin_end(10)
        available_frame.set_child(available_box)

        # Dropdown for version selection
        self.version_dropdown = Gtk.DropDown()
        available_box.append(self.version_dropdown)

        # Switch button row
        switch_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        switch_btn_box.set_halign(Gtk.Align.END)
        
        self.switch_btn = Gtk.Button(label="Switch")
        self.switch_btn.add_css_class("suggested-action")
        self.switch_btn.connect("clicked", self.run_switch)
        switch_btn_box.append(self.switch_btn)
        available_box.append(switch_btn_box)
        
        box.append(available_frame)

        # Download new version section
        download_frame = Gtk.Frame(label="Download New Version")
        download_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        download_box.set_margin_top(10)
        download_box.set_margin_bottom(10)
        download_box.set_margin_start(10)
        download_box.set_margin_end(10)
        download_frame.set_child(download_box)

        # Entry row
        entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        entry_label = Gtk.Label(label="Version:")
        entry_box.append(entry_label)
        
        self.version_entry = Gtk.Entry()
        self.version_entry.set_placeholder_text("e.g. v1.32.0")
        self.version_entry.set_hexpand(True)
        self.version_entry.connect("activate", self.run_download)  # Enter key triggers download
        entry_box.append(self.version_entry)
        
        download_box.append(entry_box)

        # Download button row
        download_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        download_btn_box.set_halign(Gtk.Align.END)
        
        self.download_btn = Gtk.Button(label="Download & Install")
        self.download_btn.add_css_class("suggested-action")
        self.download_btn.connect("clicked", self.run_download)
        download_btn_box.append(self.download_btn)
        download_box.append(download_btn_box)

        box.append(download_frame)

        # Bottom button row
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)

        # Refresh button
        refresh_btn = Gtk.Button(label="Refresh")
        refresh_btn.connect("clicked", self.refresh_versions)
        button_box.append(refresh_btn)

        box.append(button_box)

        # Status label
        self.status_label = Gtk.Label(label="")
        self.status_label.set_wrap(True)
        box.append(self.status_label)

        # Load initial data
        self.refresh_versions(None)

        self.win.present()

    def get_current_version(self):
        """Get the currently active operator-sdk version from symlink"""
        try:
            if os.path.islink(OPERATOR_SDK_BIN):
                link_target = os.readlink(OPERATOR_SDK_BIN)
                # Extract version from path like /opt/operator-sdk/v1.31.0/operator-sdk
                # The version is the second-to-last part (before the binary name)
                parts = link_target.rstrip('/').split('/')
                if len(parts) >= 2:
                    # Return the parent directory of the binary (the version folder)
                    return parts[-2]
            return "Unknown"
        except Exception as e:
            return f"Error: {e}"

    def get_available_versions(self):
        """List all versions in /opt/operator-sdk/"""
        try:
            if os.path.isdir(OPERATOR_SDK_DIR):
                versions = sorted(os.listdir(OPERATOR_SDK_DIR), reverse=True)
                return [v for v in versions if os.path.isdir(os.path.join(OPERATOR_SDK_DIR, v))]
            return []
        except Exception as e:
            return []

    def refresh_versions(self, button):
        """Refresh the current version and available versions list"""
        # Update current version
        current = self.get_current_version()
        self.current_label.set_text(f"Active: {current}")

        # Update available versions dropdown
        versions = self.get_available_versions()
        if versions:
            string_list = Gtk.StringList.new(versions)
            self.version_dropdown.set_model(string_list)
            
            # Try to select current version in dropdown
            try:
                idx = versions.index(current)
                self.version_dropdown.set_selected(idx)
            except ValueError:
                pass
            
            self.switch_btn.set_sensitive(True)
            self.status_label.set_text(f"Found {len(versions)} installed version(s)")
        else:
            string_list = Gtk.StringList.new(["No versions found"])
            self.version_dropdown.set_model(string_list)
            self.switch_btn.set_sensitive(False)
            self.status_label.set_text(f"No versions found in {OPERATOR_SDK_DIR}")

    def set_buttons_sensitive(self, sensitive):
        """Enable/disable all action buttons"""
        self.switch_btn.set_sensitive(sensitive)
        self.download_btn.set_sensitive(sensitive)
        self.version_entry.set_sensitive(sensitive)

    def run_switch(self, button):
        """Switch to the selected version using the shell script"""
        selected_idx = self.version_dropdown.get_selected()
        model = self.version_dropdown.get_model()
        
        if model and selected_idx != Gtk.INVALID_LIST_POSITION:
            version = model.get_string(selected_idx)
            
            if version and version != "No versions found":
                self.status_label.set_text(f"Switching to {version}...")
                self.set_buttons_sensitive(False)
                
                # Get the directory of this script for the shell script path
                script_dir = os.path.dirname(os.path.abspath(__file__))
                script_path = os.path.join(script_dir, "choperator-sdk.sh")
                
                # Run with pkexec for password prompt
                command = ["pkexec", script_path, version]
                
                try:
                    process = subprocess.Popen(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    # Use GLib to check process completion without blocking
                    GLib.timeout_add(500, self.check_process, process, version, "switch")
                except Exception as e:
                    self.status_label.set_text(f"Error: {e}")
                    self.set_buttons_sensitive(True)

    def run_download(self, widget):
        """Download and install a new version"""
        version = self.version_entry.get_text().strip()
        
        if not version:
            self.status_label.set_text("Please enter a version (e.g. v1.32.0)")
            return
        
        # Ensure version starts with 'v'
        if not version.startswith('v'):
            version = 'v' + version
        
        self.status_label.set_text(f"Downloading {version}... (this may take a moment)")
        self.set_buttons_sensitive(False)
        
        # Get the directory of this script for the shell script path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "choperator-sdk.sh")
        
        # Run with pkexec for password prompt
        # Use -d flag for direct download (non-interactive)
        command = ["pkexec", script_path, "-d", version]
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # Use GLib to check process completion without blocking
            GLib.timeout_add(500, self.check_process, process, version, "download")
        except Exception as e:
            self.status_label.set_text(f"Error: {e}")
            self.set_buttons_sensitive(True)

    def check_process(self, process, version, action):
        """Check if the subprocess has completed"""
        poll = process.poll()
        if poll is None:
            # Still running, check again later
            return True
        else:
            # Process finished
            if poll == 0:
                if action == "download":
                    self.status_label.set_text(f"Successfully downloaded and switched to {version}")
                else:
                    self.status_label.set_text(f"Successfully switched to {version}")
                self.version_entry.set_text("")
            else:
                stderr = process.stderr.read().decode() if process.stderr else ""
                if action == "download":
                    self.status_label.set_text(f"Download failed - check version exists on GitHub")
                else:
                    self.status_label.set_text(f"Switch failed (code {poll})")
            
            self.refresh_versions(None)
            self.set_buttons_sensitive(True)
            return False

app = OperatorSDKApp()
app.run(None)
