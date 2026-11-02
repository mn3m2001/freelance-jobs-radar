"""
Scrapers package
"""

from scrapers.mostaql import MostaqlScraper
from scrapers.kafiil import KafiilScraper
from scrapers.nafezly import NafezlyScraper
from scrapers.khamsat import KhamsatScraper
from scrapers.freelanceyard import FreelanceYardScraper

ALL_SCRAPERS = [
    MostaqlScraper,
    KafiilScraper,
    NafezlyScraper,
    KhamsatScraper,
    FreelanceYardScraper
]
