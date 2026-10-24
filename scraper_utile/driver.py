import random
import time

from selenium import webdriver

import config


def pause(minimum=config.PAUSE[0], maximum=config.PAUSE[1]):
    """Pause aléatoire (3 à 9 secondes par défaut)."""
    time.sleep(random.uniform(minimum, maximum))


def creer_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)
