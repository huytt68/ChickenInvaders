class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.ai_game = ai_game
        self.settings = self.ai_game.settings
        self.reset_stats()

        # Start game in an inactive state.
        self.game_active = True

        # High score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.roast = 0
        self.level = 1
        self.ai_game.style_bullet = "flash"
        self.ai_game.bullet_level = 1