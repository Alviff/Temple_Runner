Awesome! Great to hear it's working seamlessly now, bro! 🎉

Ekhane shob **Features, Updates & Fixes** er ekta clear breakdown dewa holo:

---

## 🛠️ Fixes & Improvements (Technical Fixes)

1. **SSL Certificate Verification Bypass:**
* **Problem:** Windows ba Python runtime-e GitHub Raw URL load korar shomoy SSL handshake error `[!] OTA Server offline or no connection` dekhaichilo.
* **Fix:** `ssl._create_unverified_context()` add kore SSL block fix kora hoyeche.


2. **Browser User-Agent Headers:**
* **Problem:** GitHub simple Python request-gulo script/bot mone kore block kore dito.
* **Fix:** Request-e **Mozilla / Windows NT User-Agent** header add kora hoyeche, jaate GitHub kono blockage chara `Version` file & `Temple_Runner.py` script fetch korte pare.


3. **Repo-Specific Direct Raw Links Integration:**
* Tumar exact repository (`Alviff/Temple_Runner`) ebong target file names (`Version` & `Temple_Runner.py`) direct code-er bhetor bind kore dewa hoyeche.



---

## 🚀 New Features & Enhancements Added

1. **Main Menu System:**
* Game start korlei direct gameplay-te na giye ekta clean **Main Menu** ashbe (`PLAY`, `SETTINGS`, `CREDITS`).


2. **Dynamic OTA Update Button:**
* GitHub-e `Version` file-e current version er cheye boro version (`1.0.3`+) paile, Main Menu-te auto ekta boro **`UPDATE GAME (vX.X.X)`** button show korbe.


3. **Auto-Restart Update Flow:**
* **`UPDATE GAME`** button-e click korle script background-e `updater_temp.py` banae target script-ta replace korbe, game exit hoye self-relaunch/open hobe!


4. **Settings & Credits Panel:**
* **Settings:** Sound Toggle & Progress Clear Data Option.
* **Credits:** Developer details (`Alviff`) & Engine Info.
