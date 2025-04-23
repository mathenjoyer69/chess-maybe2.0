import tkinter as tk

class MainScreen:
    def __init__(self):
        self.root = tk.Tk()

        self.autoplay_online_bool = tk.BooleanVar(value=False)
        self.analysis = tk.BooleanVar(value=False)
        self.autoplay_bool = tk.BooleanVar(value=False)
        self.custom_board_bool = tk.BooleanVar(value=False)
        self.bot_vs_bot = tk.BooleanVar(value=False)
        self.player_color = tk.BooleanVar(value=False)

        self.create_buttons()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def create_buttons(self):
        tk.Label(self.root, text="check this to be the white pieces").pack()
        tk.Checkbutton(self.root, text="color", variable=self.player_color).pack(pady=5)

        tk.Label(self.root, text="enable bot to move pieces on chess.com").pack()
        tk.Checkbutton(self.root, text="Autoplay Online", variable=self.autoplay_online_bool).pack(pady=5)

        tk.Label(self.root, text="makes the bot play in the analysis mode of chess.com").pack()
        tk.Checkbutton(self.root, text="Analysis", variable=self.analysis).pack(pady=5)

        tk.Label(self.root, text="the bot will play on the pygame screen automatically").pack()
        tk.Checkbutton(self.root, text="Autoplay", variable=self.autoplay_bool).pack(pady=5)

        tk.Label(self.root, text="click this to create a custom board").pack()
        tk.Checkbutton(self.root, text="custom Board", variable=self.custom_board_bool).pack(pady=5)

        tk.Label(self.root, text="click this if you want the bot to play against it self(it doesnt work yet)").pack()
        tk.Checkbutton(self.root, text="bot vs bot", variable=self.bot_vs_bot).pack(pady=5)

    def on_close(self):
        self.autoplay_online_bool = self.autoplay_online_bool.get()
        self.analysis = self.analysis.get()
        self.autoplay_bool = self.autoplay_bool.get()
        self.custom_board_bool = self.custom_board_bool.get()
        self.bot_vs_bot = self.bot_vs_bot.get()
        self.player_color = self.player_color.get()

        self.settings = {'autoplay_online_bool':self.autoplay_online_bool, 'analysis':self.analysis, 'autoplay_bool':self.autoplay_bool,
                         'custom_board_bool':self.custom_board_bool, 'bot_vs_bot':self.bot_vs_bot, 'player_color':self.player_color}

        self.root.destroy()
