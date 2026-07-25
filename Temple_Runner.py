import os
import sys
import json
import random
import math
import subprocess

# ==========================================
# 1. AUTO REQUIREMENTS INSTALLER SYSTEM
# ==========================================
def install_requirements():
    required_packages = ["pygame"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"[*] Package '{package}' missing. Installing automatically...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"[+] '{package}' installed successfully!")
            except Exception as e:
                print(f"[-] Failed to auto-install {package}: {e}")

install_requirements()

import pygame
from tkinter import Tk, filedialog

# ==========================================
# 2. OTA UPDATE & AUTO-RELOAD SYSTEM
# ==========================================
CURRENT_VERSION = "1.0.2"

# Direct Raw Links from your GitHub Repository (Alviff/Temple_Runner)
UPDATE_URL = "https://raw.githubusercontent.com/Alviff/Temple_Runner/main/Version"
SCRIPT_DOWNLOAD_URL = "https://raw.githubusercontent.com/Alviff/Temple_Runner/main/Temple_Runner.py"

def check_for_ota_update():
    print(f"[*] Current Version: v{CURRENT_VERSION}")
    try:
        import urllib.request
        req = urllib.request.Request(UPDATE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            latest_version = data.get("version", CURRENT_VERSION)
            update_script_url = data.get("script_url", SCRIPT_DOWNLOAD_URL)
            
            if latest_version > CURRENT_VERSION:
                return True, latest_version, update_script_url
    except Exception as e:
        print("[!] OTA Server offline or no connection.")
    
    return False, CURRENT_VERSION, SCRIPT_DOWNLOAD_URL

update_available, new_ver, update_url = check_for_ota_update()

def trigger_ota_update_and_restart():
    """Download update from GitHub raw link, close game, replace file & relaunch"""
    print("[*] Downloading update package and restarting...")
    
    updater_code = f"""
import time, subprocess, sys, urllib.request

time.sleep(1)
print("[*] Fetching latest game version from GitHub...")

try:
    url = "{update_url}"
    req = urllib.request.Request(url, headers={{'User-Agent': 'Mozilla/5.0'}})
    with urllib.request.urlopen(req) as response:
        new_code = response.read().decode('utf-8')
    
    # Overwrite current running script file
    with open("{sys.argv[0]}", "w", encoding="utf-8") as f:
        f.write(new_code)
    
    print("[+] Game updated successfully! Relaunching...")
    subprocess.Popen([sys.executable, "{sys.argv[0]}"])
except Exception as e:
    print(f"[-] Update failed: {{e}}")

sys.exit()
"""
    with open("updater_temp.py", "w", encoding="utf-8") as f:
        f.write(updater_code)
    
    subprocess.Popen([sys.executable, "updater_temp.py"])
    pygame.quit()
    sys.exit()

# ==========================================
# 3. GAME INITIALIZATION & SAVE SYSTEM
# ==========================================
pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Temple Escape 2D - v{CURRENT_VERSION}")
clock = pygame.time.Clock()

# Colors
DARK_BG = (43, 29, 12)
GROUND_COLOR = (27, 0, 0)
GRID_COLOR = (62, 39, 35)
GOLD = (255, 215, 0)
RED = (255, 61, 0)
GREEN = (0, 230, 118)
WHITE = (255, 255, 255)
CYAN = (0, 229, 255)
DARK_OVERLAY = (0, 0, 0, 220)
BUTTON_BG = (80, 50, 20)
BUTTON_HOVER = (120, 75, 30)

font_small = pygame.font.SysFont("Consolas", 14, bold=True)
font_medium = pygame.font.SysFont("Consolas", 18, bold=True)
font_large = pygame.font.SysFont("Consolas", 28, bold=True)

SAVE_FILE = "game_save.json"

def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except:
            return {"high_score": 0, "coins": 0, "sound": True}
    return {"high_score": 0, "coins": 0, "sound": True}

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

save_data_dict = load_data()
high_score = save_data_dict.get("high_score", 0)
total_coins = save_data_dict.get("coins", 0)
sound_enabled = save_data_dict.get("sound", True)

# Custom Assets
custom_assets = {"player": None, "monster": None, "obs_low": None}

def select_image(asset_key):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.webp")])
    root.destroy()
    if file_path:
        try:
            img = pygame.image.load(file_path).convert_alpha()
            custom_assets[asset_key] = img
        except Exception as e:
            print("Error loading image:", e)

# Game State
current_scene = "MENU" # "MENU", "SETTINGS", "CREDITS", "PLAYING"
score = 0
game_speed = 6
frame = 0
game_over = False

player = {
    "x": 180, "y": 280, "width": 35, "height": 50, "original_height": 50,
    "dy": 0, "gravity": 0.75, "is_jumping": False, "is_sliding": False, "slide_timer": 0
}

monster = {"x": 40, "y": 250, "width": 70, "height": 80}
obstacles = []
coins = []

def reset_game():
    global score, game_speed, frame, game_over
    score = 0
    game_speed = 6
    frame = 0
    obstacles.clear()
    coins.clear()
    player["y"] = 280
    player["height"] = player["original_height"]
    player["is_jumping"] = False
    player["is_sliding"] = False
    game_over = False

def spawn_obstacle():
    obs_type = "low" if random.random() > 0.5 else "high"
    if obs_type == "low":
        obstacles.append({"x": WIDTH, "y": 290, "w": 35, "h": 40, "type": "low"})
    else:
        obstacles.append({"x": WIDTH, "y": 220, "w": 40, "h": 50, "type": "high"})

def spawn_coin():
    coins.append({"x": WIDTH, "y": 240 if random.random() > 0.5 else 290, "r": 10})

# Menu UI Buttons
btn_play = pygame.Rect(WIDTH // 2 - 100, 140, 200, 40)
btn_settings = pygame.Rect(WIDTH // 2 - 100, 195, 200, 40)
btn_credits = pygame.Rect(WIDTH // 2 - 100, 250, 200, 40)

# Big OTA Update Button (Only visible if update available)
btn_update = pygame.Rect(WIDTH // 2 - 140, 305, 280, 45)

# Gameplay Avatar Buttons
btn_img_player = pygame.Rect(10, 10, 110, 25)
btn_img_monster = pygame.Rect(130, 10, 110, 25)
btn_img_obs = pygame.Rect(250, 10, 110, 25)

# Settings Buttons
btn_sound_toggle = pygame.Rect(WIDTH // 2 - 120, 150, 240, 40)
btn_reset_data = pygame.Rect(WIDTH // 2 - 120, 210, 240, 40)
btn_back = pygame.Rect(20, 20, 90, 30)

# Main Loop
running = True
while running:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_scene == "MENU":
                if btn_play.collidepoint(mouse_pos):
                    reset_game()
                    current_scene = "PLAYING"
                elif btn_settings.collidepoint(mouse_pos):
                    current_scene = "SETTINGS"
                elif btn_credits.collidepoint(mouse_pos):
                    current_scene = "CREDITS"
                elif update_available and btn_update.collidepoint(mouse_pos):
                    trigger_ota_update_and_restart()

            elif current_scene in ["SETTINGS", "CREDITS"]:
                if btn_back.collidepoint(mouse_pos):
                    current_scene = "MENU"
                elif current_scene == "SETTINGS":
                    if btn_sound_toggle.collidepoint(mouse_pos):
                        sound_enabled = not sound_enabled
                        save_data({"high_score": high_score, "coins": total_coins, "sound": sound_enabled})
                    elif btn_reset_data.collidepoint(mouse_pos):
                        high_score = 0
                        total_coins = 0
                        save_data({"high_score": 0, "coins": 0, "sound": sound_enabled})

            elif current_scene == "PLAYING":
                if btn_img_player.collidepoint(mouse_pos):
                    select_image("player")
                elif btn_img_monster.collidepoint(mouse_pos):
                    select_image("monster")
                elif btn_img_obs.collidepoint(mouse_pos):
                    select_image("obs_low")

        if event.type == pygame.KEYDOWN:
            if current_scene == "PLAYING":
                if game_over and event.key == pygame.K_SPACE:
                    reset_game()
                elif not game_over:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and not player["is_jumping"] and not player["is_sliding"]:
                        player["is_jumping"] = True
                        player["dy"] = -14
                    if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and not player["is_jumping"] and not player["is_sliding"]:
                        player["is_sliding"] = True
                        player["height"] = 25
                        player["y"] += 25
                        player["slide_timer"] = 35
                if event.key == pygame.K_ESCAPE:
                    current_scene = "MENU"

    # --- GAMEPLAY UPDATE LOGIC ---
    if current_scene == "PLAYING" and not game_over:
        frame += 1
        score += 1

        if frame % 300 == 0:
            game_speed += 0.5

        current_score = score // 5
        if current_score > high_score:
            high_score = current_score
            save_data({"high_score": high_score, "coins": total_coins, "sound": sound_enabled})

        if player["is_jumping"]:
            player["dy"] += player["gravity"]
            player["y"] += player["dy"]
            if player["y"] >= 280:
                player["y"] = 280
                player["is_jumping"] = False

        if player["is_sliding"]:
            player["slide_timer"] -= 1
            if player["slide_timer"] <= 0:
                player["is_sliding"] = False
                player["y"] -= 25
                player["height"] = player["original_height"]

        if frame % 90 == 0:
            spawn_obstacle()
        if frame % 45 == 0:
            spawn_coin()

        for obs in obstacles[:]:
            obs["x"] -= game_speed
            player_rect = pygame.Rect(player["x"], player["y"], player["width"], player["height"])
            obs_rect = pygame.Rect(obs["x"], obs["y"], obs["w"], obs["h"])

            if player_rect.colliderect(obs_rect):
                game_over = True
                save_data({"high_score": high_score, "coins": total_coins, "sound": sound_enabled})

            if obs["x"] + obs["w"] < 0:
                obstacles.remove(obs)

        for coin in coins[:]:
            coin["x"] -= game_speed
            player_center = (player["x"] + player["width"] // 2, player["y"] + player["height"] // 2)
            dist = math.hypot(player_center[0] - coin["x"], player_center[1] - coin["y"])

            if dist < (player["width"] // 2 + coin["r"]):
                total_coins += 1
                save_data({"high_score": high_score, "coins": total_coins, "sound": sound_enabled})
                coins.remove(coin)
            elif coin["x"] < 0:
                coins.remove(coin)

    # --- RENDERING SCENES ---
    screen.fill(DARK_BG)

    # 1. MAIN MENU SCENE
    if current_scene == "MENU":
        title_txt = font_large.render("TEMPLE ESCAPE 2D", True, GOLD)
        screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 60))

        # Render Play, Settings, Credits Buttons
        for rect, label in [(btn_play, "PLAY"), (btn_settings, "SETTINGS"), (btn_credits, "CREDITS")]:
            color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_BG
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, GOLD, rect, 2, border_radius=8)
            txt = font_medium.render(label, True, WHITE)
            screen.blit(txt, (rect.x + rect.width // 2 - txt.get_width() // 2, rect.y + 10))

        # Render UPDATE BUTTON if available
        if update_available:
            up_color = RED if btn_update.collidepoint(mouse_pos) else CYAN
            pygame.draw.rect(screen, up_color, btn_update, border_radius=10)
            pygame.draw.rect(screen, WHITE, btn_update, 2, border_radius=10)
            up_txt = font_medium.render(f"UPDATE GAME (v{new_ver})", True, (0, 0, 0))
            screen.blit(up_txt, (btn_update.x + btn_update.width // 2 - up_txt.get_width() // 2, btn_update.y + 12))

    # 2. SETTINGS SCENE
    elif current_scene == "SETTINGS":
        title_txt = font_large.render("SETTINGS", True, GOLD)
        screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 50))

        # Sound Toggle Button
        s_color = BUTTON_HOVER if btn_sound_toggle.collidepoint(mouse_pos) else BUTTON_BG
        pygame.draw.rect(screen, s_color, btn_sound_toggle, border_radius=8)
        s_txt = font_medium.render(f"SOUND: {'ON' if sound_enabled else 'OFF'}", True, WHITE)
        screen.blit(s_txt, (btn_sound_toggle.x + btn_sound_toggle.width // 2 - s_txt.get_width() // 2, btn_sound_toggle.y + 10))

        # Reset Progress Button
        r_color = RED if btn_reset_data.collidepoint(mouse_pos) else BUTTON_BG
        pygame.draw.rect(screen, r_color, btn_reset_data, border_radius=8)
        r_txt = font_medium.render("CLEAR SAVE DATA", True, WHITE)
        screen.blit(r_txt, (btn_reset_data.x + btn_reset_data.width // 2 - r_txt.get_width() // 2, btn_reset_data.y + 10))

    # 3. CREDITS SCENE
    elif current_scene == "CREDITS":
        title_txt = font_large.render("GAME CREDITS", True, GOLD)
        screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 60))

        lines = [
            "Developer: Alviff",
            "Built with: Python & Pygame Engine",
            "Auto OTA Updater Connected to GitHub"
        ]
        for idx, line in enumerate(lines):
            txt = font_medium.render(line, True, WHITE)
            screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 140 + idx * 40))

    # Back Button for Settings & Credits
    if current_scene in ["SETTINGS", "CREDITS"]:
        pygame.draw.rect(screen, BUTTON_BG, btn_back, border_radius=5)
        b_txt = font_small.render("< BACK", True, WHITE)
        screen.blit(b_txt, (btn_back.x + 10, btn_back.y + 8))

    # 4. ACTIVE PLAYING SCENE
    elif current_scene == "PLAYING":
        # Draw Ground & Grid
        pygame.draw.rect(screen, GROUND_COLOR, (0, 330, WIDTH, 70))
        for x in range(0, WIDTH, 40):
            grid_x = x - int(frame * game_speed) % 40
            pygame.draw.rect(screen, GRID_COLOR, (grid_x, 330, 40, 70), 2)

        # Draw Monster
        monster_y = monster["y"] + int(math.sin(frame * 0.2) * 5)
        if custom_assets["monster"]:
            scaled_img = pygame.transform.scale(custom_assets["monster"], (monster["width"], monster["height"]))
            screen.blit(scaled_img, (monster["x"], monster_y))
        else:
            pygame.draw.rect(screen, RED, (monster["x"], monster_y, monster["width"], monster["height"]))

        # Draw Player
        if custom_assets["player"]:
            scaled_img = pygame.transform.scale(custom_assets["player"], (player["width"], player["height"]))
            screen.blit(scaled_img, (player["x"], player["y"]))
        else:
            pygame.draw.rect(screen, GREEN, (player["x"], player["y"], player["width"], player["height"]))

        # Draw Obstacles
        for obs in obstacles:
            if obs["type"] == "low" and custom_assets["obs_low"]:
                scaled_img = pygame.transform.scale(custom_assets["obs_low"], (obs["w"], obs["h"]))
                screen.blit(scaled_img, (obs["x"], obs["y"]))
            else:
                pygame.draw.rect(screen, (141, 110, 99) if obs["type"] == "low" else (176, 190, 197), (obs["x"], obs["y"], obs["w"], obs["h"]))

        # Draw Coins
        for coin in coins:
            pygame.draw.circle(screen, GOLD, (int(coin["x"]), int(coin["y"])), coin["r"])

        # Avatar Upload Top Buttons
        pygame.draw.rect(screen, BUTTON_BG, btn_img_player)
        pygame.draw.rect(screen, BUTTON_BG, btn_img_monster)
        pygame.draw.rect(screen, BUTTON_BG, btn_img_obs)

        screen.blit(font_small.render("+ Player Img", True, WHITE), (btn_img_player.x + 5, btn_img_player.y + 5))
        screen.blit(font_small.render("+ Monster Img", True, WHITE), (btn_img_monster.x + 5, btn_img_monster.y + 5))
        screen.blit(font_small.render("+ Obs Img", True, WHITE), (btn_img_obs.x + 5, btn_img_obs.y + 5))

        # Top Right Score Stats
        score_txt = font_small.render(f"SCORE: {score // 5} | BEST: {high_score} | COINS: {total_coins}", True, GOLD)
        screen.blit(score_txt, (WIDTH - 370, 15))

        # Game Over Screen
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(DARK_OVERLAY)
            screen.blit(overlay, (0, 0))

            go_txt = font_large.render("CAUGHT BY MONSTER!", True, RED)
            sc_txt = font_small.render(f"SCORE: {score // 5}  |  BEST: {high_score}  |  TOTAL COINS: {total_coins}", True, GOLD)
            re_txt = font_small.render("PRESS SPACE TO RESTART  |  ESC FOR MENU", True, WHITE)

            screen.blit(go_txt, (WIDTH // 2 - go_txt.get_width() // 2, 140))
            screen.blit(sc_txt, (WIDTH // 2 - sc_txt.get_width() // 2, 200))
            screen.blit(re_txt, (WIDTH // 2 - re_txt.get_width() // 2, 250))

    pygame.display.flip()

pygame.quit()
sys.exit()