import sys
import os
import shutil


class Filer:
    def __init__(self, filename: str, folder: str = "res") -> None:
        assert folder in {"res", "data"}, "err: incorrect folder"
        if folder == "res":
            assert filename in {"def.txt", "README.txt"}, \
                "err: incorrect filename"
        else:
            assert filename in {"scr.txt", "usr.txt"}, \
                "err: incorrect filename"

        self.filename = filename
        self.folder = folder
    
    def initialize(self) -> None:
        assert self.folder == "data", "err: trying to overwrite res"

        if self.filename == "scr.txt":
            try:
                with open(self.get_path(force = True), "w") as f:
                    f.write("\n".join("0/0" for _ in range(12)))
            except:
                sys.stderr.write("ERROR: failed to initialite scr.txt\n")
                sys.stderr.flush()
        else:
            try:
                shutil.copy(self.get_path(filename = "def.txt", folder = "res"),
                            self.get_path(force = True))
            except:
                sys.stderr.write("ERROR: failed to initialize usr.txt\n")
    
    def get_path(self, filename: str | None = None,
                 folder: str | None = None, force: bool = False) -> str:
        if filename is None:
            filename = self.filename
        if folder is None:
            folder = self.folder

        if filename != self.filename or folder != self.folder:
            assert folder in {"res", "data"}, "err: incorrect folder"
            if folder == "res":
                assert filename in {"def.txt", "README.txt"}, \
                    "err: incorrect filename"
            else:
                assert filename in {"scr.txt", "usr.txt"}, \
                    "err: incorrect filename"
        
        if folder == "data":
            app_dir = os.path.join(os.environ["LOCALAPPDATA"], "pb111")
            data_dir = os.path.join(app_dir, "data")
            filepath = os.path.join(data_dir, filename)
            if not force and not os.path.exists(filepath):
                self.initialize()
            return filepath
        
        if hasattr(sys, "_MEIPASS"):
            basepath = sys._MEIPASS
        else:
            basepath = os.path.abspath(".")
        return os.path.join(os.path.join(basepath, "res"), filename)
    
    def get_content(self) -> str:
        try:
            with open(self.get_path(), "r") as f:
                return f.read().rstrip()
        except:
            sys.stderr.write(f"ERROR: failed to read from {self.filename}\n")
            sys.stderr.flush()

    def save_content(self, content: str) -> None:
        try:
            with open(self.get_path(), "w") as f:
                f.write(content.rstrip())
        except:
            sys.stderr.write(f"ERROR: failed to write into {self.filename}\n")
            sys.stderr.flush()
    
    def reset(self) -> None:
        assert self.folder == "data", "err: trying to overwrite res"

        if self.filename == "scr.txt":
            try:
                with open(self.get_path(force = True), "w") as f:
                    f.write("\n".join("0/0" for _ in range(12)))
            except:
                sys.stderr.write("ERROR: failed to reset scr.txt\n")
                sys.stderr.flush()
        else:
            try:
                shutil.copy(self.get_path(filename = "def.txt", folder = "res"),
                            self.get_path(force = True))
            except:
                sys.stderr.write("ERROR: failed to reset usr.txt\n")
