import tkinter as tk


class ScreenProtector:
    def __init__(self):
        pass

    def run(self):
        """Create a fullscreen window with text area and close button"""

        root = tk.Tk()
        root.title("Fullscreen Window")

        root.attributes("-fullscreen", True)
        root.configure(bg="white")
        
        # Make window stay on top
        root.attributes("-topmost", True)
        
        # Remove window decorations
        root.overrideredirect(True)

        def exit_fullscreen(event=None):
            root.attributes("-fullscreen", False)
            root.quit()

        # root.bind("<Escape>", exit_fullscreen)
        
        # Block Alt+Tab and other system keys
        root.bind("<Alt_L>", lambda e: "break")
        root.bind("<Alt_R>", lambda e: "break")
        root.bind("<Control_L>", lambda e: "break")
        root.bind("<Control_R>", lambda e: "break")
        root.bind("<Tab>", lambda e: "break")
        root.bind("<Alt-KeyPress>", lambda e: "break")
        root.bind("<Alt-Tab>", lambda e: "break")
        root.bind("<Alt-F4>", lambda e: "break")
        root.bind("<Control-Escape>", lambda e: "break")
        root.bind("<Escape>", lambda e: "break")
        root.bind("<Super_L>", lambda e: "break")  # Left Windows key
        root.bind("<Super_R>", lambda e: "break")  # Right Windows key

        n_session = 2

        text1 = tk.Label(
            root,
            text=f"You have {n_session} left for today",
            font=("Arial", 16),
            bg='white'
        )
        text1.pack(pady=(100, 20))
        
        text2 = tk.Label(
            root,
            text="This text cannot be edited.",
            font=("Arial", 14),
            bg='white'
        )
        text2.pack(pady=20)
        
        text3 = tk.Label(
            root,
            text="Press Escape or click Close to exit.",
            font=("Arial", 12),
            bg='white'
        )
        text3.pack(pady=20)

        def close_window():
            root.destroy()

        close_button = tk.Button(
            root,
            text="Close",
            command=close_window,
            font=("Arial", 14),
            bg="red",
            fg="white",
            height=2,
            width=15,
        )
        close_button.pack(pady=20)

        root.mainloop()