import time
import random
from urllib.parse import urlparse
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OGameSeleniumClient:
    def __init__(self, base_url: str, headless=False):
        self.base_url = base_url.rstrip("/")
        self.headless = headless
        self.driver = None
        self.game_url = None
        self.game_handle = None
        self.delay_range = (1.5, 3.0)

    def login(self, wait_time=100) -> bool:
        print(f"[LOGIN] Uruchamiam przeglądarkę, masz {wait_time} sekund na ręczne zalogowanie i wejście do gry.")
        self._init_driver()
        self.driver.get(self.base_url)
        start = time.time()
        original_handles = set(self.driver.window_handles)

        while time.time() - start < wait_time:
            new_handles = set(self.driver.window_handles) - original_handles
            for h in new_handles:
                if self._check_tab_for_game(h):
                    self.game_handle = h
                    print("[LOGIN] Gra wykryta w nowej karcie.")
                    return True
            if self._check_tab_for_game(self.driver.current_window_handle):
                self.game_handle = self.driver.current_window_handle
                print("[LOGIN] Gra wykryta w bieżącej karcie.")
                return True
            time.sleep(2)

        print("[LOGIN] Nie wykryto gry w czasie oczekiwania.")
        return False

    def _check_tab_for_game(self, handle: str) -> bool:
        try:
            current = self.driver.current_window_handle
            self.driver.switch_to.window(handle)
            url = self.driver.current_url.lower()
            if "page=ingame" in url and "component=" in url:
                self.game_url = self._get_game_base_url(url)
                return True
            return False
        finally:
            try:
                self.driver.switch_to.window(current)
            except:
                pass

    def _get_game_base_url(self, url: str) -> str:
        p = urlparse(url)
        return f"{p.scheme}://{p.netloc}/game/"

    def _init_driver(self):
        opts = uc.ChromeOptions()
        opts.add_argument("--window-size=1280,720")
        opts.add_argument("--start-maximized")
        if self.headless:
            opts.add_argument("--headless=new")
        opts.add_argument("--disable-popup-blocking")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--lang=pl-PL")
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " \
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        opts.add_argument(f"user-agent={ua}")
        self.driver = uc.Chrome(options=opts)
        self.driver.maximize_window()

    def ensure_game_tab(self):
        if self.game_handle and self.game_handle in self.driver.window_handles:
            self.driver.switch_to.window(self.game_handle)
            return
        for h in self.driver.window_handles:
            self.driver.switch_to.window(h)
            if "page=ingame" in self.driver.current_url:
                self.game_handle = h
                return
        raise RuntimeError("Nie znaleziono karty z grą.")

    def fetch_component(self, component: str, params: str = "") -> str:
        self.ensure_game_tab()
        param_part = f"&{params.lstrip('&')}" if params else ""
        url = f"{self.game_url}index.php?page=ingame&component={component}{param_part}"
        self.driver.get(url)
        WebDriverWait(self.driver, 120).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        WebDriverWait(self.driver, 120).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(random.uniform(*self.delay_range))
        return self.driver.page_source

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    def click_js_coordinates(self, x: int, y: int):
        print(f"[CLICK] Klikam w (JS) współrzędne x: {x}, y: {y}")
        self.scroll_to_bottom()
        js = f"""
            (() => {{
                const ev = new MouseEvent('click', {{
                    bubbles: true,
                    cancelable: true,
                    view: window,
                    clientX: {x},
                    clientY: {y}
                }});
                const el = document.elementFromPoint({x}, {y});
                if(el) {{
                    el.dispatchEvent(ev);
                    return true;
                }}
                return false;
            }})();
        """
        res = self.driver.execute_script(js)
        if res:
            print("[CLICK] Kliknięcie wykonane.")
        else:
            print("[CLICK] Nie znaleziono elementu na wskazanej pozycji.")
        time.sleep(1)

    def close(self):
        if self.driver:
            self.driver.quit()
            print("[DRIVER] Przeglądarka zamknięta.")
