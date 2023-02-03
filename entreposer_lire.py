# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 09:44:57 2023

@author: Dr. CiDre
"""

"""Créer pour LISTE D'ÉPICERIE AUTOMATIQUE PAR WEB-SCRAPPING.

Sert à créer des listes permettant aux informations d'êtres lues :

    1. Recettes archivées - nom
    2. Recette - information (nom, lien web, ingrédients)
    3. Liste d'épicerie - ordonnée
"""
#IMPORTER module créer par Dr. CiDre
import utilitaire as utl

#IMPORTER modules Python
import pandas as pd
import os




#%%Livre de recettes
def lst_lvrs_rctts_csv():
    """Retourner une liste de livres de recettes disponibles sous format .csv.

    @df_des_rctts_un_lvr
    @lst_rctts_depuis_csv
    @envyr_modif_lvr_rctts_csv - e_m
    @gere_silw_dns_archv - iuf - Construire liste
    """    
    #TROUVER le chemin d'accès aux livres de recettes Excel.
    lvrs_rctts_dir_pth = utl.chmn_accs_lvrs_rctts_dir()

    #LA liste des fichiers sont les livres de recettes disponibles.
    return os.listdir(lvrs_rctts_dir_pth)



def df_des_rctts_un_lvr(num_lvr_rctts):
    """Simple fonction pour créer le dataframe pandas des recettes archivées
    d'un livre de recettes.

    @lst_ingr_rctt_csv
    @mod_info_rctt_csv - e_m
    @envyr_modif_lvr_rctts_csv
    @est_dans_archv_check_csv
    @mod_la_rctt_affchr - iuf - Afficher recettes csv
    """
    #OBTERNIR le chemin d'accès au livre de recettes.
    lst_rctts_pth = f'{utl.chmn_accs_lvrs_rctts_dir()}/\
{lst_lvrs_rctts_csv()[num_lvr_rctts-1]}'
    
    return pd.read_csv(lst_rctts_pth, encoding='latin', delimiter=';',
                       na_filter=False
                       )




def tbl_tt_rctts_trier_par_lvr():
    """Créer une table complète, sous forme de liste << [[], [], []] >>,
    des livrs de rctts avec leurs rctts.

    @boucle_chsr_entr_pls_rctts - utl
    """
    tbl_rctts = []
    #OBTENIR la liste de recettes dans chacune
    for num, lvr in enumerate(lst_lvrs_rctts_csv()):
        tbl_rctts += [lst_rctts_depuis_csv(num)]
    
    return tbl_rctts




def lst_rctts_depuis_csv(num_lvr_rctts):
    """Retourner liste des recettes disponibles dans l'entreposage 'liste de recettes'
    Excel d'un livre de recettes.
    
    @affchr_livres_rctts - iuf - Afficher recettes csv
    """
    #OBTENIR le chemin d'accès à la liste de recette.
    lst_rctts_pth = f'{utl.chmn_accs_lvrs_rctts_dir()}/\
{lst_lvrs_rctts_csv()[num_lvr_rctts-1]}'
    
    #OBTENIR liste des recettes (1 recette par index de liste).
    lst_rctts= list(pd.read_csv(lst_rctts_pth, encoding='latin',
                                      delimiter=';', nrows=0))
    
    return lst_rctts




def lst_ingr_rctt_csv(num_lvr_rctts, num_rctt):
    """Retourner la liste d'information d'une recette parmis les recettes disponibles
    de l'entreposage 'liste de recettes' Excel, selon son chiffre et le livre de
    recettes.

    @voir_une_rctte - iuf - Afficher recettes csv
    @gere_si_lw_wbs_dns_arch - utl - Gérer si dans archive
    """    
    #CRÉER le dataframe pandas des recettes.
    df_rctts = df_des_rctts_un_lvr(num_lvr_rctts)
    
    #CRÉER la liste d'information pour la recette désirée (pas le nom d'inclue)
    lst_rctt_dsr = list(df_rctts.iloc[:, num_rctt-1])
    
    #OBTENIR le nom de la recette via liste_rctts_depuis_csv().
    nm_rctt = lst_rctts_depuis_csv(num_lvr_rctts)[num_rctt-1]
    
    return [nm_rctt] + lst_rctt_dsr




#%% Liste d'épicerie
def affchr_lsts_epcr_dspnbl():
    """Afficher les listes d'épiceries disponibles dans l'archive.

    @Ingrédients épicerie
    """
    #1.OBTENIR le chemin d'accès à l'archive des listes d'épicerie.
    dir_lvr_epcr_pth = utl.chmn_accs_dir_lsts_epcr()

    #2.OBTENIR la liste des noms de listes d'épicerie.
    lst_lsts_epcr = os.listdir(dir_lvr_epcr_pth)

    #3.1.LIMITER à un # fixé la quantité de listes d'épicerie à afficher.
    if len(lst_lsts_epcr) > 10:
        lst_lsts_epcr = lst_lsts_epcr[-10:]


    #3.2.SINON envoyer tel quel
    for lst_epcr in lst_lsts_epcr:
        print(lst_epcr)




def df_lst_epcr(nm_lst_epcr):
    """Créer le dataframe pandas de la liste d'épicerie."""

    #TROUVER chemin d'accès à cette liste d'épicerie (nom_fichier)
    lst_epcr_pth = f'{utl.chmn_accs_dir_lsts_epcr(nm_lst_epcr)}\{nm_lst_epcr}.csv'
    
    #LISTE peut être vide
    return pd.read_csv(lst_epcr_pth, encoding='latin', delimiter=';',
                       na_filter=False
                       )




#%% Profil par défaut
#TODO ..on peut assigner LE trie par défaut? Sinon y a til d'autres choses par défaut?
#Le nombre de liste d'épicerie qu'on peut voir par défaut au début du programme "Ingrédients.."
#Où une wbs va être archivé par défaut (montre les options dit veux-tu aller avec ta valeur par défaut ou nn.)
def dict_infos_prfls_dft_csv():
    """Retirer les informations du fichier texte des profils par défaut. Organiser
    l'information s'y trouvant en:
        1.Profil_par_défaut
        2.Nom de profil : colomnes par défaut.


    RETOURNE: {profils par défauts}


    @lst_epcrs_par_dft

    """
    #0.OBTENIR le chemin d'accès à Profils_par_défaut.csv.
    pth_prfls_dft = utl.chmn_accs_prfl_dft()

    #1.DF du profil par défaut.
    df_prfl_dft = pd.read_csv(pth_prfls_dft, sep=';', encoding='latin', na_filter=False)

    #2.CRÉER le dictionnaire.
    dict_prfls_dft = {}
    for clmn_nm in df_prfl_dft:
        dict_prfls_dft[clmn_nm] = list(df_prfl_dft[clmn_nm])

    #3.RETOURNER dictionnaire des profils par défauts.
    return dict_prfls_dft




def lst_entt_epcrs_par_dft():
    """Obtenir les épiceries par défaut.


    RETOURNE: [Entêtes liste d'épiceries par défaut]




    """
    #0.OBTENIR le dictionnaire des profils par défaut.
    dict_prfls = dict_infos_prfls_dft_csv()

    #1.NOM du profil par défaut actuel.
    pfl_dft = dict_prfls['Profil_par_defaut'][0]
    lst_clnns_dft = [f'{3+indx}.nm_col' for indx,
                     nm_col in enumerate(dict_prfls[pfl_dft])]
    
    #2.LISTE des épiceries par défaut actuel.
    return ['1.Nom_de_recette', '2.Lien_web'] + lst_clnns_dft




