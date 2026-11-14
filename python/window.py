import tkinter as tk


def New_Window(
    HEIGHT: int,
    WIDTH: int,
    X: int,
    Y: int,
    Color: str = "#323232",
):
    WINDOW_NAME = tk.Toplevel()
    WINDOW_NAME.update_idletasks()
    WINDOW_NAME.overrideredirect(True)
    WINDOW_NAME.geometry(f"{WIDTH}x{HEIGHT}+{X}+{Y}")
    WINDOW_NAME.configure(bg=Color)
    return WINDOW_NAME


ws = tk.Tk()
ws.withdraw()
screen_height = ws.winfo_screenheight()
screen_width = ws.winfo_screenwidth()
Windows = [
    [tk.Toplevel for _ in range(int(screen_width / 100))]
    for _ in range(int(screen_height / 100))
]
coords = [(1, 1), (2, 1), (2, 3), (3, 1), (3, 3), (2, 2), (1, 3)]

for i in range(int(screen_height / 100)):
    for x in range(int(screen_width / 100)):
        Window = New_Window(100, 100, x * 100, i * 100)
        # pyrefly: ignore [unsupported-operation]
        Windows[i][x] = Window
        if (i, x) in coords:
            # pyrefly: ignore [missing-argument]
            Windows[i][x].configure(bg="#ffffff")
ws.resizable(False, False)
ws.mainloop()
