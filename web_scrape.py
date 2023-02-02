# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 19:33:13 2023

@author: Dr. CiDre
"""

"""Module pour les fonctions de Web_scraping du programme de liste d'épicerie
automatique.

BEAUTIFUL SOUP - Python Web Scrapper choisi.
"""

from bs4 import BeautifulSoup
import requests

#TODO
def scrp_sln_site_web(lien_web, dns_archv_ou_nn): 
    """Trie le lien web pour engager la fonction scrapping appropriée.
    Si dns_archv_ou_nn == 'O', prendre les ingrédients de l'archive.
    """    
    
    if 'ricardo' in lien_web:
        return 'ricardo_function'
    
    return 'Pas en mémoire(Fonction ou sinon on recommence?'



#TODO
def scrape_ricardo(lien_web):
    """Scrape le site web de Ricardo pour le titre et les ingrédients d'une
    recette."""
    return
