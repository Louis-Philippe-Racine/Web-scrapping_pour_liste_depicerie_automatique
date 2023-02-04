# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 15:54:12 2023

@author: Dr. CiDre
"""
#IMPORTER modules créer par Dr. CiDre
import entreposer_lire as e_l
import entreposer_mod as e_m


#IMPORTER module Python
from os import getcwd, path
import pandas as pd




#VARIABLES GLOBALES 
#(Chemins d'accès dépend de où le programme est installé.)
prgrm_pth = getcwd()
wrk_dir_pth = prgrm_pth[:prgrm_pth.rfind('\\')]




def chmn_accs_lvrs_rctts_dir():
    """Renvoyer le chemin d'accès du livre de recette .csv
    selon la localisation du programme '.exe'.
    
    @df_des_rctts_un_lvr - entreposer_mod
    @lst_rctts_depuis_csv - entreposer_lire
    @envyr_modif_lvr_rctts_csv - entreposer_mod
    """
    #LIVRES DE RECETTES (Excel) - Chemin d'accès
    arch_dir_pth = wrk_dir_pth + r'\Entrepôt\Livres_recettes_csv'
    
    return arch_dir_pth




def chmn_accs_dir_lsts_epcr():
    """Renvoyer le chemin d'accès au dossier des listes d'épicerie
    selon la localisation du programme '.exe'."""
    #LISTE D'ÉPICERIE (Excel) - Chemin d'accès
    return wrk_dir_pth + r"\Listes_d'épiceries"




def chmn_accs_prfls_dft():
    """Renvoyer le chemin d'accès des paramètres actuels du profil par défaut."""

    return f'{wrk_dir_pth}\Entrepôt\Profils_par_défaut\Profils_par_défaut.csv'




def boucle_chsr_entr_pls_rctts(txt_présentation, nums_lvr_rctts, nums_rctt,
                               inpt_txt, outpt_cndtns, ingr=None):
    """Permettre à l'utilisateur de choisir une recette parmis une liste de recette.
    
    0.Présenter les recettes.
    1.Afficher les recettes disponibles et potentiellement leur livres de recettes.
    2.Forcer le choix de l'une d'entre elle.
    
    *les nums doivent être sous forme de liste contenant des int.
    """
    #1.AFFICHER si il y a un txt
    if txt_présentation:
        print(f'{txt_présentation}\n')

    #2.0.OBTENIR les listes hors boucle.
    lst_lvrs_rctts = e_l.lst_rctts_depuis_csv()
    tbl_rctts = e_l.tbl_tt_rctts_trier_par_lvr()  

    #2.1.LIVRES de recettes seulement.
    if nums_lvr_rctts == 'tous':
        #2.1.0.AFFICHER.
        for indx, lvr in enumerate(lst_lvrs_rctts):
            print(f'{indx+1} - {lvr}')

    #2.2.RECETTES d'un livre spécifique.
    elif nums_rctt == 'toutes':
        #2.2.0.AFFICHER recettes du livre
        for inx, rctt in enumerate(tbl_rctts[nums_lvr_rctts-1]):
            print(f'(indx+1) - {rctt}')

    #2.3.RECETTES & LIVRES spécifiques.
    else:
        #2.3.1.BOUCLE d'AFFICHAGE:
        for indx_lvr, lvr in enumerate(nums_lvr_rctts):
            #2.3.1.0.AFFICHER "# - nm_lvr_rctts: nm_rctt".
            print(f'{indx_lvr} - {lst_lvrs_rctts[lvr-1]}: \
{tbl_rctts[lvr-1][nums_rctt[indx_lvr]-1]}')

            #2.3.2.AFFICHER les ingrédients à chaque recette si demandé.
            if ingr:
                #2.3.3.PRÉSENTER les ingrédients.
                print('\nAvec les ingrédients:\n')

                lst_info_rctt = e_l.lst_ingr_rctt_csv(lvr, nums_rctt[indx_lvr])  
                #2.4.0.AFFICHER les ingrédients
                for indx_ingr, info in enumerate(lst_info_rctt):
                    #2.4.1.RETIRER les cases vides.
                    if not info:
                        continue

                    #2.5.AFFICHER "# - info".
                    print(f'{indx+1} - {info}')


    #3.DEMANDER lequel ou laquelle choisir.
    #3.1.CONDITIONNEL
    if outpt_cndtns:
        return boucle_frc_entr_lwrcs(inpt_txt, outpt_cndtns)


    #3.2.INCONDITIONNEL
    return input(inpt_txt)




def boucle_frc_entr_lwrcs(inpt_txt, outpt_cndtns):
    """Assurer une entrée valide pour un input en ouvrant une boucle while
    jusqu'à la satisfactions des conditions.
    """
    #OUVRIR la boucle while pour forcer la réponse.
    continuer_boucle = True
    while continuer_boucle:
        rep = input(f'{inpt_txt}').lower()

        #ERREUR d'entrée, informer l'utilisateur et recommencer.
        if rep not in outpt_cndtns.lower():
            print(f"Pour répondre, veuillez écrire une des options valides parmis: \
{outpt_cndtns}.")
            continue

        #SANS-ERREUR puisque les erreurs sont filtrées.
        continuer_boucle = False

    return rep




#TODO wut iz diss
def str_split_info(txt_info, info_ou_ingr):
    """Diviser une ligne 'str' d'information ou d'ingrédient par les deux côtés
    du '.'.

    Les informations d'une recettes (titre, lien web et ingrédients) sont sous
    forme '#index.information'.
    
    Les ingrédients sont sous forme 'quantité nom de l'ingrédient'.
    
    @
    """
    
    if info_ou_ingr == 'info':
        #('.' remplacé par ' ')
        txt_info = ' '.join(txt_info.split('.'))

        #SPLIT par espace permettra de voir si le premier indx est un nombre
        #puis de réassembler le reste, en LISTE, comme information:
        info_pour_mod_rctt = txt_info.split(' ')

        #T1.3.1.MODIFIER les informations de la recette dans le .csv.
        if info_pour_mod_rctt[0].isnumeric():

            #1.3.1.1. RÉASSEMBLER l'information à modifier.
            nouv_info = ''                
            for info in info_pour_mod_rctt[1:]:
                #'  ', '. ', etc. donnerons un '' dans la liste après les manips.
                if info == '':
                    continue

                nouv_info += info

            #TODO UTILISER le dictionnaire interne de synonymes/omissions.
    
        return info_pour_mod_rctt[0], nouv_info




def chck_epcr_clnns_dft(nm_fchr_epcr):
    """Vérifier si la liste d'entêtes dans la liste d'épicerie actuelle reflète
    les entêtes du profil par défaut actuel.


    RETOURNE: 'True', 'False'


    @affchr_epcr_et_chcks - iuf - Ingrédients épicerie

    """
    #1.OBTENIR la liste d'entête du profil par défaut.
    lst_entts_dft = e_l.lst_entt_epcrs_par_dft()

    #2.OBTENIR la liste d'entête de la liste d'épicerie.
    df_lst_epcr = e_l.df_lst_epcr(nm_fchr_epcr)
    lst_entts_epcr = [entt for entt in df_lst_epcr]

    #3.VÉRIFIER si elles sont équivalentes ou non.
    if lst_entts_epcr == lst_entts_dft:
        return True


    #ELSE
    return False




def est_dans_lst_epcr_dj(lien_web, nm_lst_epcr):
    """Vérifier si le lien web est déjà intégré dans la liste d'épicerie.
    

    RETOURNE: 'continuer', 'lien_web'

    @option_web_scrapping - iu_arparse_fncts - Construire liste

    """
    #OBTENIR le df de la liste d'épicerie.
    df_epcr = e_l.df_lst_epcr(nm_lst_epcr)
    lst_lien_web_epcr = list(df_epcr.iloc[:, 0])

    #SI le lien web est déjà dans la liste d'épicerie, demander si continuer ou sortir
    if lien_web in lst_lien_web_epcr:
        #INFORMER l'utilisateur.
        print(f"Cette recette est déjà dans la liste d'épicerie selon le lien\
web:\n{lien_web}")

        #CONTINUER donnera l'option de recommencer la boucle ou d'en sortir.
        return 'continuer'

    #PAS dans la liste d'épicerie donc pas de problème avec ce lien web pour ce check.    
    return lien_web




def chck_lst_epcr_exst(nm_lst_epcr):
    """Vérifier si la liste d'épicerie du le fichier "nom_fichier" existe.


    RETOURNE: 'True' ou 'False' 

        - selon l'existence ou non, respectivement, du fichier
        "nom_fichier".csv à l'emplacement supposé. -


    @Afficher épicerie - iu_argparse_main.py

    """
    
    #0.TROUVER chemin d'accès à cette liste d'épicerie (nom_fichier)
    lst_epcr_pth = f'{chmn_accs_dir_lsts_epcr(nm_lst_epcr)}\{nm_lst_epcr}.csv'

    #1.LISTE d'épicerie existe.
    if path.exists(lst_epcr_pth):        
        return True


    #2.NON-EXISTANTE.    
    return False




#%% Vérifier si dans archive
def est_dans_arch_check_csv(lien_web):
    """Pour format .csv : Vérifier si le lien_web est dans l'archive. 


    RETOURNE: ([], []) ou ([nums_lvr_rctts], [nums_rctt])


    @option_web_scrapping - iu_arparse_fncts - Construire liste
    @aj_rctt_wbs_lvr_csv - iu_argparse_fncts - Ajouter au livre de recettes csv

    """
    #1.OBTENIR tous les liens web des recettes archivées.
    #[[liste liens web d'un livre], [liste liens web d'un livre], etc.]
    lst_lws = obtnr_lw_rctts_archv()

    #2.VÉRIFIER si lien_web dans un livre de cette et les lvr rctts+num rctt lorsque trouvé.
    #SI non, retourne [], []
    return verf_archv_obt_infos(lst_lws, lien_web)




def obtnr_lw_rctts_archv():
    """Réunir les liens webs disponible de tous les livres de recettes, séparés 
    1 lien web / index de liste.


    RETOURNE: liste des liens webs de tous les livres archivés.


    @est_dans_arch_check_csv

    """
    #1.OBTENIR le nom des livres de recettes.
    nm_lvrs_rctts = e_l.lst_lvrs_rctts_csv()

    #2.LIENS web archivés - non-séparé.
    nn_sep_lst_lw_rctts = []
    for lvr_rctts in nm_lvrs_rctts:
        #list(dfrecettes[retire que les liens web])
        nn_sep_lst_lw_rctts += list(e_l.df_des_rctts_un_lvr(lvr_rctts).iloc[1, :])
    
    #[[liste liens web d'un livre], [liste liens web d'un livre], etc.]
    return nn_sep_lst_lw_rctts




def verf_archv_obt_infos(lst_lws, lien_web):
    """Obtenir le.s # du.es livre.s de recettes et le.s # de.s recette.s où le
    lien web entrée pour le web-scrapping est archivée.


    RETOURNE: [], [] - Si non-trouvé, 
              [nums_lvr_rctts], [nums_rctt] - pour toutes les recettes trouvées
                                               avec ce lien web.


    @est_dans_arch_check_csv
    """
    nums_lvr_rctts= []
    nums_rctt = []
    #VÉRIFIER chaque livre de recette et retenir son # index.
    for indx_lvr, lws_lvr in enumerate(lst_lws):
        #VÉRIFIER chaque recette et retenir son  # index. 
        for indx_rctt in enumerate(lws_lvr):
            if lien_web in lst_lws:
                #ADDITIONER par un puisque que ces # sont normés débuter à 1 et non 0.
                nums_lvr_rctts += [indx_lvr + 1]
                nums_rctt += [indx_rctt + 1]

    return nums_lvr_rctts, nums_rctt



#%% Gérer si dans archive
def gere_si_lw_wbs_dns_archv(lien_web, info_destination):
    """Vérifier, informer puis résoudre si le lien web entrée pour le web-scrape
    est parmis les liens web des recettes archivées - donc la recette et ses ingrédients
    est déjà organisée / triée.
    *info_destination : arch = num_lvr_rctt
                        lst epcr = nm_fchr


    RETOURNE: 'lien_web', 's', 'OK'


    @option_web_scrapping - iuf - Construire liste - Web-scrapping
    @aj_rctt_wbs_lvr_csv - iuf - Ajouter au livre de recettes csv

    """
    #1.VÉRIFIER si le lien web est déjà dans les livres de recettes archivées.
    #SI non, retourne [], []
    nums_lvr_rctts, nums_rctt = est_dans_arch_check_csv(lien_web)

    #1.0.SI [], non-trouvé donc retourne le lien_web original.
    if not nums_lvr_rctts:
        return lien_web


    #2.TROUVÉ donc INFORMER l'utilisateur et demander si ajouter.
    #2.1.UNE seule recette trouvée.
    if len(nums_rctt) == 1:
        #AFFICHER et DEMANDER si ajoutée à la liste.
        nums_lvr_rctts = un_lw_wbs_rctt_archv(nums_lvr_rctts, nums_rctt)

    #2.2.PLUSIEURS recettes contiennent ce lien web.
    #AFFICHER, DEMANDER si ajouter et retirer la recette choisie.
    else:
        nums_lvr_rctts, nums_rctt = plsr_lw_wbs_rctts_archv(
            nums_lvr_rctts, nums_rctt
        )


    #3.0.Sortir du programme.
    if nums_lvr_rctts == 's':
        return nums_lvr_rctts


    #3.2.(N)e pas utiliser le ou les rctts. On web_scrape le lien web.
    if nums_lvr_rctts == 'n':
        return lien_web


    #3.3.ELSE utilise les ingrédient de num_lvr_rctt et num_rctt
    #demande si à modifier, continuer boucle.
    #3.3.0.OBTENIR la liste d'informations à ajouter.
    lst_infos_aj = e_l.lst_ingr_rctt_csv(nums_lvr_rctts, nums_rctt)

    #3.3.1.ARCHIVE : [num_lvr_rctts, num_rctt]
    if isinstance(info_destination, int):
        #3.3.1.1.ENVOYER
        return e_m.envyr_modif_lvr_rctts_csv(info_destination, 'nouvelle', lst_infos_aj)
    
    
    #3.3.2.ELSE LISTE D'ÉPICERIE.    
    #2.2.1.UTILISER les ingrédients entreposés
    for info_rctt in e_l.lst_ingr_rctt_csv(nums_lvr_rctts, nums_rctt):
        ##TODO change_liste_épicerie(ingrédients, nom_fichier_semaine)
        print('I luv me man.')

    #RECOMMENCER la boucle de création de liste d'épicerie. ('o' ou 'n'pas la bonne recette)
    return 'OK'




def un_lw_wbs_rctt_archv(nums_lvr_rctts, nums_rctt):
    """Gérer l'occasion où le lien web du web-scrape est trouvé en une seule recette
    dans les archives.


    RETOURNE: 'o', 'n', 's'


    @gere_si_lw_wbs_dns_arch

    """
    #0.AFFICHER le nom de la recette archivée et sa liste d'ingrédients
    txt_pres = "Ce lien web est trouvé à travers les livres de recettes archivées:"
    #0.1.DEMANDER si c'est bien cette recette.
    input_txt = "Désirez-vous utiliser les informations de cette recette archivée?\n\
( o / n ) : "
    #0.2.FORCER entrée valide parmis : (o)ui, (n)on et (s)ortir.
    dmnd_si_archv_ou_nn = boucle_chsr_entr_pls_rctts(
        txt_pres, nums_lvr_rctts, nums_rctt, input_txt, ['o', 'n', 's'], ingr='tous'
    )

    if dmnd_si_archv_ou_nn == 'o':
        return nums_lvr_rctts

    return dmnd_si_archv_ou_nn




def plsr_lw_wbs_rctts_archv(nums_lvr_rctts, nums_rctt):
    """Gérer l'occasion où le lien web du web-scrape se trouve dans plusieurs recettes
    dans les archives.


    RETOURNE: [num_lvr_rctt, num_rctt], ['n', 'n'] ou ['s', 's']

    
    @gere_si_lw_dns_archv

    """
    #0.AFFICHER les recttes où le lien web est contenu.
    txt_pres = 'Ce lien web est associé à des recettes déjà archivées!\nVoici dans\
quel livre de recettes ils se trouvent, ainsi que leur nom et ingrédients:'
    #0.1.DEMANDER d'ajouter des ingrédients ou nn.
    inpt_txt = "Désirez-vous utiliser les ingrédients (#)d'une de ces recettes?\n\
( # / n ) : "
    #0.2.PRÉPARER les conditions d'entrées.
    num_disp_optns = [str(x+1) for x, lvr in enumerate(nums_lvr_rctts)]
    optns_disps = num_disp_optns + ['n', 's']
    #0.3.AFFICHER, DEMANDER et FORCER entrée.
    num_chx = boucle_chsr_entr_pls_rctts(txt_pres, nums_lvr_rctts, 
                                         nums_rctt, inpt_txt, 
                                         optns_disps, ingr='tous'
                                         )

 
    
    #1.0.GÉRER si retour est numérique ou str
    if num_chx in ['n', 's']:
        #1.0.1.FONCTION mère vérifie le num_chx en 1er, donc elle sortira de la boucle.
        return num_chx, num_chx


    #1.1.ELSE choix d'une recette.
    return nums_lvr_rctts[int(num_chx)], nums_rctt[int(num_chx)]
