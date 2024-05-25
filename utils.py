from config import win, font, RED, WHITE

def display_score(score):
    value = font.render(f"Score: {score}", True, WHITE)
    win.blit(value, [0, 0])

def game_over_message():
    msg = font.render("Game Over! Press R to Restart", True, RED)
    win.blit(msg, [win.get_width() // 6, win.get_height() // 3])
