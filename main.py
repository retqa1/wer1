
import inspect, io, sys, colorama
from colorama import Fore, Style


class Inspector:
    __slots__ = ("module", "stream")  # лише дві змінні

    def __init__(self, module=colorama, stream=None):
        self.module, self.stream = module, stream or sys.stdout

    def _p(self, title, *data):
        print(f"{Fore.CYAN}{title}{Style.RESET_ALL}", *data, file=self.stream)

    def run(self):
        m, pub = self.module, lambda o: [n for n in dir(o) if not n.startswith("_")]
        cls = m.AnsiToWin32
        self._p("Версія / файл:", m.__version__, m.__file__)
        self._p("Атрибути:", pub(m))
        self._p("Fore / Style:", pub(m.Fore), pub(m.Style))
        self._p("Коди (str):", repr(m.Fore.RED), repr(m.Style.RESET_ALL))
        self._p("Cursor:", {n: getattr(m.Cursor, n)(2) for n in ("UP", "DOWN", "FORWARD", "BACK")},
                repr(m.Cursor.POS(5, 10)))
        self._p("Функції:", {n: str(inspect.signature(getattr(m, n))) for n in
                             ("init", "deinit", "reinit", "just_fix_windows_console", "colorama_text")})
        self._p("AnsiToWin32:", inspect.signature(cls.__init__), [n for n in pub(cls) if callable(getattr(cls, n))])
        for strip in (False, True):
            buf = io.StringIO()
            cls(buf, strip=strip).write(f"{m.Fore.RED}текст{m.Style.RESET_ALL}")
            self._p(f"strip={strip}:", repr(buf.getvalue()))
        w = cls(io.StringIO())
        self._p("Не-tty (авто):", f"strip={w.strip}, convert={w.convert}")
        self._p("Windows-шар:", m.win32.windll, m.winterm.WinTerm)


if __name__ == "__main__":
    with colorama.colorama_text():
        Inspector().run()
