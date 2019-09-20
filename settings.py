class Settings:
    """A class to store all settings of the game"""
    def __init__(self):
        """Initialize game settings"""
        # Screen settings
        self.scr_width = 1200
        self.scr_height = 800
        self.bg_color = (230, 230, 230)

        # Ship's settings
        self.ship_speed_factor = 1.5
