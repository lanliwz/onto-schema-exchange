import hashlib
import time
import threading


class PrintOnChangeMixin:
    def on_file_change(self, file_path: str):
        """Called when file content changes."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print("🔄 File content updated:\n")
                print(content)
                print("-" * 40)
        except Exception as e:
            print(f"❗ Error reading file: {e}")

def print_it(file_path: str):
        """Called when file content changes."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print("🔄 File content updated:\n")
                print(content)
                print("-" * 40)
        except Exception as e:
            print(f"❗ Error reading file: {e}")


def get_text(file_path: str) -> str:
    """Called when file content changes."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return content

    except Exception as e:
        print(f"❗ Error reading file: {e}")
        return 'f"❗ Error reading file: {e}'
class FileWatcher:
    def __init__(self, file_path: str, check_interval: float = 1.0):
        self.file_path = file_path
        self.check_interval = check_interval
        self._stop_event = threading.Event()

    def compute_hash(self) -> str:
        hasher = hashlib.md5()
        with open(self.file_path, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()

    def watch(self):
        try:
            last_hash = self.compute_hash()
        except FileNotFoundError:
            print(f"❌ File not found: {self.file_path}")
            return

        print(f"👀 Watching file: {self.file_path}")
        if hasattr(self, 'on_file_change'):
            self.on_file_change(self.file_path)

        while not self._stop_event.is_set():
            try:
                current_hash = self.compute_hash()
                if current_hash != last_hash:
                    last_hash = current_hash
                    if hasattr(self, 'on_file_change'):
                        self.on_file_change(self.file_path)
            except FileNotFoundError:
                print("⚠️ File was deleted or moved!")
                return
            time.sleep(self.check_interval)

    def start(self):
        """Start watching in a separate thread."""
        self._thread = threading.Thread(target=self.watch, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the background watcher thread."""
        self._stop_event.set()
        self._thread.join()


class PrintingFileWatcher(FileWatcher, PrintOnChangeMixin):
    pass

