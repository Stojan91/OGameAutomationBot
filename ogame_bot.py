import sys
import time
import traceback
import json
import random
import re
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from selenium_client import OGameSeleniumClient

class Parser:
    @staticmethod
    def parse_resources(html: str) -> dict:
        def get_res(name):
            m = re.search(fr'id="resources_{name}"[^>]*data[-_]raw="(\d+)"', html)
            return int(m.group(1)) if m else 0
        return {
            "metal": get_res("metal"),
            "crystal": get_res("crystal"),
            "deuterium": get_res("deuterium"),
        }

class AI:
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.parser = Parser()
        self.sleep_short = 60  # Szybka pętla!

    def run(self):
        try:
            print("=== Nowy cykl / Random AI ===")
            categories = [
                # (nazwa_kategorii, prefix_html, lista obiektów w tej kategorii według config)
                ("supplies", "supply", ["metal", "crystal", "deuterium"]),
                ("facilities", "facility", ["robotics", "nanite_factory", "shipyard"]),
                ("research", "research", ["energy", "combustion", "computer"]),
                ("defenses", "defense", ["rocket", "laser", "heavy"]),
            ]
            cat = random.choice(categories)
            self.click_random(cat[0], cat[1], cat[2])
            print(f"Losowo kliknąłem coś w kategorii {cat[0]}")
            time.sleep(self.sleep_short)
        except Exception:
            print("Nieoczekiwany błąd:")
            traceback.print_exc()
            time.sleep(self.sleep_short)

    def click_random(self, category, prefix, objects):
        # Przechodzimy do strony odpowiedniej kategorii i klikamy w losowy budynek z listy
        picked = random.choice(objects)
        key = picked if prefix != "supply" else f"{picked}_mine"
        coords = self.config.get("click_coordinates", {}).get(key)
        if not coords:
            print(f"[AI] Brak współrzędnych do kliknięcia dla '{key}' w config.")
            return
        print(f"[AI] W ({category}) klikam losowo w '{key}' na {coords}")
        self.client.fetch_component(category)
        self.client.scroll_to_bottom()
        self.client.click_js_coordinates(*coords)

class Bot:
    def __init__(self, server, config_path="config.json"):
        self.server = server
        self.config_path = config_path
        self.client = None
        self.ai = None
        self.running = True

    def initialize(self) -> bool:
        try:
            self.client = OGameSeleniumClient(self.server)
            if not self.client.login():
                print("Błąd logowania.")
                return False
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            self.ai = AI(self.client, config)
            print("Bot zainicjowany.")
            return True
        except Exception as e:
            print(f"Błąd inicjalizacji: {e}")
            return False

    def run(self):
        print("Start bota.")
        while self.running:
            try:
                self.ai.run()
            except KeyboardInterrupt:
                print("Przerwano bota.")
                self.running = False
            except Exception:
                traceback.print_exc()
                time.sleep(10)
        self.shutdown()

    def shutdown(self):
        if self.client:
            self.client.close()
        print("Bot zatrzymany.")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Bot OGame random clicker")
    parser.add_argument("--server", default="https://s264-pl.ogame.gameforge.com")
    parser.add_argument("--config", default="config.json")
    args = parser.parse_args()
    bot = Bot(args.server, args.config)
    if not bot.initialize():
        sys.exit(1)
    bot.run()

if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, signal.default_int_handler)
    main()
