#!/usr/bin/env python3
import sys
import time
import traceback
import json
import re
from bs4 import BeautifulSoup

from selenium.common.exceptions import WebDriverException

from selenium_client import OGameSeleniumClient


class Parser:
    @staticmethod
    def parse_levels(html: str, prefix: str) -> dict:
        pattern = rf'{prefix}(\d+)"[^>]*data-level="(\d+)"'
        matches = re.findall(pattern, html)
        return {key: int(value) for key, value in matches}

    @staticmethod
    def parse_resources(html: str) -> dict:
        def get_resource(name: str) -> int:
            m = re.search(fr'id="resources_{name}"[^>]*data[-_]raw="(\d+)"', html)
            return int(m.group(1)) if m else 0
        return {
            "metal": get_resource("metal"),
            "crystal": get_resource("crystal"),
            "deuterium": get_resource("deuterium"),
        }

    @staticmethod
    def is_building(html: str) -> bool:
        soup = BeautifulSoup(html, 'html.parser')
        timers = soup.select('span.countdown, span.Timer2, span.timer-countdown')
        for timer in timers:
            style = timer.get('style', '')
            if 'display:none' in style.replace(' ', '').lower():
                continue
            if timer.text.strip():
                return True
        return False


class AI:
    def __init__(self, client: OGameSeleniumClient, config: dict):
        self.client = client
        self.config = config
        self.parser = Parser()
        self.sleep_short = 60  # 1 minuta przerwy
        self.sleep_long = 300  # 5 minut przerwy przy budowie

    def run(self):
        try:
            print("===== Nowy cykl =====")
            if self.any_building():
                print("Trwa budowa lub produkcja. Dłuższa przerwa.")
                time.sleep(self.sleep_long)
                return

            if self.build_category("supplies", "supply"):
                time.sleep(self.sleep_long)
                return

            if self.build_category("facilities", "facility"):
                time.sleep(self.sleep_long)
                return

            if self.build_category("research", "research"):
                time.sleep(self.sleep_long)
                return

            if self.build_category("defenses", "defense"):
                time.sleep(self.sleep_long)
                return

            print("Brak do zrobienia. Krótsza przerwa.")
            time.sleep(self.sleep_short)
        except WebDriverException as e:
            print(f"Błąd WebDriver: {e}")
            time.sleep(self.sleep_long)
        except Exception:
            print("Nieoczekiwany błąd w AI:")
            traceback.print_exc()
            time.sleep(self.sleep_long)

    def any_building(self) -> bool:
        for comp in ["supplies", "facilities", "research", "defenses"]:
            html = self.client.fetch_component(comp)
            if self.parser.is_building(html):
                print(f"Wykryto budowę w {comp}")
                return True
        return False

    def build_category(self, category_name: str, prefix_html: str) -> bool:
        html = self.client.fetch_component(category_name)
        levels = self.parser.parse_levels(html, prefix_html)
        resources = self.parser.parse_resources(html)
        built = False

        for obj_name, target_level in self.config.get("max_levels", {}).items():
            if self.category_prefix(obj_name) != prefix_html:
                continue

            current_level = int(levels.get(self.map_name_to_id(obj_name), 0))

            if current_level >= target_level:
                print(f"{obj_name.title()} jest na poziomie {current_level} — cel {target_level} osiągnięty")
                continue

            cost = self.config.get("costs", {}).get(obj_name, {})
            if not self.can_build(resources, cost):
                print(f"Za mało surowców na {obj_name} (koszt {cost}, masz {resources})")
                continue

            key = obj_name if prefix_html != "supply" else f"{obj_name}_mine"
            coords = self.config.get("click_coordinates", {}).get(key)
            if not coords:
                print(f"Brak współrzędnych kliknięcia dla '{key}' w config.json")
                continue

            print(
                f"Buduję {obj_name} do poziomu {current_level + 1} — klikam '{key}' na współrzędne {coords}"
            )
            self.client.scroll_to_bottom()
            self.client.click_js_coordinates(*coords)
            built = True
            break

        return built

    def category_prefix(self, name: str) -> str:
        mining = ["metal", "crystal", "deuterium"]
        facilities = ["robotics", "nanite_factory", "shipyard"]
        research = ["energy", "combustion", "computer"]
        defense = ["rocket", "laser", "heavy"]

        if name in mining or name.endswith("_mine"):
            return "supply"
        if name in facilities:
            return "facility"
        if name in research:
            return "research"
        if name in defense:
            return "defense"
        return ""

    def map_name_to_id(self, name: str) -> str:
        mapping = {
            "metal": "1",
            "crystal": "2",
            "deuterium": "3",
            "robotics": "14",
            "nanite_factory": "15",
            "shipyard": "21",
            "energy": "113",
            "combustion": "115",
            "computer": "108",
            "rocket": "401",
            "laser": "402",
            "heavy": "403",
        }
        name_clean = name.replace("_mine", "")
        return mapping.get(name_clean)

    def can_build(self, resources: dict, cost: dict) -> bool:
        return all(resources.get(k, 0) >= v for k, v in cost.items())


class Bot:
    def __init__(self, server_url, config_path="config.json"):
        self.server_url = server_url
        self.config_path = config_path
        self.client = None
        self.ai = None
        self.running = True

    def initialize(self) -> bool:
        import json

        try:
            self.client = OGameSeleniumClient(self.server_url)
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
        print("Start głównej pętli bota.")
        while self.running:
            try:
                self.ai.run()
            except KeyboardInterrupt:
                print("Przerwano działanie bota.")
                self.running = False
            except Exception:
                traceback.print_exc()
                time.sleep(30)

        self.shutdown()

    def shutdown(self):
        print("Zamykanie bota...")
        if self.client:
            self.client.close()
        print("Bot zatrzymany.")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Zaawansowany bot OGame")
    parser.add_argument("--server", default="https://s264-pl.ogame.gameforge.com", help="Url serwera")
    parser.add_argument("--config", default="config.json", help="Ścieżka do pliku config.json")
    parser.add_argument("--test", action="store_true", help="Tylko test logowania")
    args = parser.parse_args()

    bot = Bot(args.server, args.config)
    if not bot.initialize():
        sys.exit(1)

    if args.test:
        print("Test logowania zakończony sukcesem.")
        bot.shutdown()
        return

    bot.run()


if __name__ == "__main__":
    import signal

    signal.signal(signal.SIGINT, signal.default_int_handler)
    main()
