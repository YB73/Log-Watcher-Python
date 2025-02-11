import os
import time
import codecs
from typing import Set, Callable
from dataclasses import dataclass
from threading import Thread, Lock

@dataclass
class LogUpdate:
    lines: list[str]
    position: int

class LogWatcher:
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.callbacks: Set[Callable[[str], None]] = set()
        self.running = False
        self.thread: Thread | None = None
        self.lock = Lock()
        self.last_position = 0
        
    def register_callback(self, callback: Callable[[str], None]) -> None:
        with self.lock:
            self.callbacks.add(callback)
            
    def unregister_callback(self, callback: Callable[[str], None]) -> None:
        with self.lock:
            self.callbacks.discard(callback)
    
    def _detect_encoding(self) -> str:
        """Detect the encoding of the log file."""
        try:
            with open(self.log_file, 'rb') as f:
                raw = f.read(4)  # Read first 4 bytes to check BOM
                if raw.startswith(codecs.BOM_UTF16_LE):
                    return 'utf-16-le'
                elif raw.startswith(codecs.BOM_UTF16_BE):
                    return 'utf-16-be'
                elif raw.startswith(codecs.BOM_UTF8):
                    return 'utf-8-sig'
                else:
                    return 'utf-8'
        except FileNotFoundError:
            return 'utf-8'
            
    def get_last_n_lines(self, n: int = 10) -> list[str]:
        try:
            encoding = self._detect_encoding()
            with codecs.open(self.log_file, 'r', encoding=encoding) as f:
                lines = f.readlines()
                return lines[-n:] if len(lines) >= n else lines
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
            
    def _notify_callbacks(self, line: str) -> None:
        with self.lock:
            for callback in self.callbacks:
                try:
                    callback(line)
                except Exception as e:
                    print(f"Error in callback: {e}")
                    
    def _watch_file(self) -> None:
        if not os.path.exists(self.log_file):
            open(self.log_file, 'a').close()
        
        encoding = self._detect_encoding()
        with codecs.open(self.log_file, 'r', encoding=encoding) as f:
            # Skip BOM if present by reading to end
            f.seek(0, 2)
            self.last_position = f.tell()
            
            while self.running:
                current_position = f.tell()
                line = f.readline()
                
                if line:
                    # Strip any remaining BOM characters and whitespace
                    line = line.strip('\ufeff').strip()
                    if line:  # Only notify if line is not empty
                        self._notify_callbacks(line)
                    self.last_position = f.tell()
                else:
                    # No new lines, wait a bit before checking again
                    time.sleep(0.1)
                    f.seek(current_position)
                    
    def start(self) -> None:
        if self.thread is not None:
            return
            
        self.running = True
        self.thread = Thread(target=self._watch_file, daemon=True)
        self.thread.start()
        
    def stop(self) -> None:
        self.running = False
        if self.thread:
            self.thread.join()
            self.thread = None