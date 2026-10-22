try:
    from rich.console import Console
    from rich.table import Table
except ImportError:
    # Plain-text fallback when rich is not installed
    class Console:
        def print(self, *args, **kwargs):
            if args and hasattr(args[0], "show"):
                args[0].show()
            else:
                print(*args)

    class Table:
        def __init__(self, title=""):
            self.title, self.columns, self.rows = title, [], []

        def add_column(self, name):
            self.columns.append(name)

        def add_row(self, *cells):
            self.rows.append(cells)

        def show(self):
            print(self.title)
            print(" | ".join(self.columns))
            for row in self.rows:
                print(" | ".join(row))
