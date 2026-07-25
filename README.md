---

## 🎮 1. Main Menu System (Interactive Interface)

Game shuru hone-i direct gameplay-te na giye ekta modern UI Menu-te niye jabe:

* **PLAY Button:** Click korle game start hobe.
* **SETTINGS Button:** Game sound toggle (On/Off) ebong save data reset korar option thakbe.
* **CREDITS Button:** Game developer, version information ebong tech details show korbe.

---

## 🔄 2. Dynamic "UPDATE GAME" Button

Server-e missing or higher version detected hole Main Menu-te boro kore highlight kora ekta **`UPDATE GAME (vX.X.X)`** button show hobe:

* Normal obosthay aita hidden thakbe.
* **New Update Asle:** Boro Cyan/Red glowing design-e screen-er majhe ashbe jate player-er chokhe pore.

---

## ⚡ 3. One-Click Auto Update & Relaunch

Updater button-e click korle:

1. Game auto-save complete hobe.
2. Background-e ekta updater script launch hoye current **app close hoye jabe**.
3. New files update/overwrite hoye, **game nijai auto re-open (restart) hobe** — kono Manual file setup lagbe na.

---

## 💾 4. Settings & Save State Manager

* **Sound Toggle & Progress Clear:** Settings screen theke score/coins Data Reset ar Sound Preferences change kora jabe, ja `game_save.json`-e persistent update thakbe.
* **In-Game ESC Shortcut:** Gameplay-er majhe `ESC` press korle jekono shomoy Main Menu-te ferot asha jabe.
