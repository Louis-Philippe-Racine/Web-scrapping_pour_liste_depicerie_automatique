# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 21:17:51 2023

@author: Dr. CiDre
"""
#IMPORTER les modules du Dr. CiDre
import utilitaire as utl
import entreposer_lire as e_l
import entreposer_mod as e_m
import web_scrape as wbs

#IMPORTER le module Python.
import argparse


def analyse_cmd_wndw_inpt():
    "Analyses the argurment input in command prompt to run the script."

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-a', '--ajouter_au_livre_de_recettes',
        dest='ajouter_au_livre_de_recettes',
        action='store_true',
        help = 'Afficher les listes de recettes disponibles pour pouvoir en ajouter\
une manuellement, en modifier une existante ou en ajouter une par web-scrapping.'
    )

    parser.add_argument(
        '-i', '--ingredients_pour_epicerie',
        dest='ingr_lst_epcr',
        action='store_true',
        help = "Initie la création/agrandissement d'une liste d'épicerie"
    )

    parser.add_argument(
        '-e', '-gerer_liste_epicerie',
        dest='gérer_liste_epicerie',
        action='store_true',
        help = "Top-level gestion: Trier les ingrédients ajouter par épicerie \
et par rang ou enlever les infos d'une recette de la liste \
d'épicerie."
    )

    parser.add_argument(
        '-l', '--gerer_livre_recettes',
        dest='gérer_livre_recettes',
        action='store_true',
        help = "Top-level gestion: Supprimer ou recopier des recettes à travers\
les livres, ajouter des livres de recettes, etc."
    )

    parser.add_argument(
        '-p', '--partager_liste',
        dest='partager_liste',
        action='store_true',
        help = "Partager la liste d'épicerie à G_Keep et Favoris"
    )

    return parser.parse_args()




#%% Ajouter au livre de recettes csv
def chx_dprt_aj_au_lvr_rctt():
    """Proposer les choix disponibles pour l'option "Ajouter au livre de recettes".
    Puis, afficher les livres de recettes disponibles et demander le choix de
    l'utilisateur.


    RETOURNE: optn_aj(soit 'v_m', 'wbs' ou 'manl'), num_lvr_rctts   ou 's'


    @Ajouter au livre de recettes csv

    """
    #1.CHOISIR entre les options d'ajout de recette.
    inpt_txt = 'Désirez-vous;\n - (v)oir/modifier une recette,\n - \
ajouter une recette par (w)eb-scrapping,\n - ajouter une recette (m)anuellement\n\
 - ou (s)ortir de ce programme?n\( v / w / m / s ) : '
    #1.1.AFFICHER, DEMANDER, FORCER entrée
    prog_lst_rctts = utl.boucle_frc_entr_lwrcs(inpt_txt, ['v', 'w', 'm', 's'])


    #2.CHOISIR le livre de recettes à modifier.
    txt_prsnttn = 'Voici les livres de recettes disponibles:'
    inpt_txt = '\nDans quel livre de recettes disponible désirez-vous effectuer\
ce programme?\n (#) : '
    #2.0.OBTENIR le # de recette disponible.
    cndtn = [str(x+1) for x, lvr in enumerate(e_l.lst_lvrs_rctts_csv())]
    #2.1.AFFICHER, DEMANDER, FORCER entrée
    num_lvr_rctts = utl.boucle_chsr_entr_pls_rctts(txt_prsnttn, None, 'tous',
                                   inpt_txt, cndtn+['s'])

    #2.1.0.num_lvr_rctts peut être 's'.
    if num_lvr_rctts != 's':
        num_lvr_rctts = int(num_lvr_rctts)
    
    #3.RETOURNER l'option et le livre de recettes choisis.
    return prog_lst_rctts, num_lvr_rctts




def voir_une_rctte(num_lvr_rctts):
    """Gérer l'option d'afficher une recette en particulier selon la demande
    de l'utilisateur.


    RETOURNE: 's', 'n', 'continuer', 'OK'



    @Étape 2 d'Afficher recettes

    """   
    #0.AFFICHER les recettes disponibles.
    txt_présentation = 'Voici la liste des recettes archivées:'
    #0.1.DEMANDER si veut voir ou non.
    txt_input = 'Voulez-vous voir les ingrédients \
/ modifier une recette en particulier ?\n( o / n ) : '
    #0.2.AFFICHER, DEMANDER, puis FORCER l'entrée.
    voir_rctt_ou_nn = utl.boucle_chsr_entr_pls_rctts(
        txt_présentation, num_lvr_rctts, 'toutes',
        txt_input, ['o', 'n', 's']
    )


    #2.SI VOIR
    if voir_rctt_ou_nn == 'o':
        #2.1.1DEMANDER un numéro de recette.
        inpt_txt = 'Quelle est le numéro de la recette que vous \
voulez voir ou modifier ?\n(#) : '

        #2.1.0.FORCER une entrée.
        num_disp_rctt = [str(x+1) for x, lvr in enumerate(
            e_l.lst_rctts_depuis_csv(num_lvr_rctts)
            )]
        num_disp_rctt += ['s']
        num_rctt = utl.boucle_frc_entr_lwrcs(inpt_txt, num_disp_rctt)
        
        #2.2.0.
        if num_rctt == 's':
            return 's'
        

        #2.2.1.OPTION MODIFIER cette recette
        return mod_la_rctt_affchr(num_lvr_rctts, int(num_rctt))


    #3.ELSE pas voir ou sortir
    return voir_rctt_ou_nn




def mod_la_rctt_affchr(num_lvr_rctts, num_rctt):
    """Gérer l'option modification de la recette afficher.


    RETOURNE:'s', 'n', 'continuer', 'OK'


    @grr_optn_rchrch_rctt_archv_lw
    @voir_une_rctte

    """
    #0.AFFICHER.
    txt_pres = 'Cette recette:'
    inpt_txt = 'Voulez-vous modifier cette recette ou non?\n( o / n ) : '
    #0.1.AFFICHER, DEMANDER puis FORCER entrée.
    mod_rctt_ou_nn = utl.boucle_chsr_entr_pls_rctts(
        txt_pres, num_lvr_rctts, num_rctt, inpt_txt, ['o', 'n', 's'],
        ingr='tous'
    )


    #1.MODIFIER la RECETTE manuellement.
    if mod_rctt_ou_nn == 'o':
        #1.1.BOUCLE de modification de la recette.
        mod_rctt_ou_nn = e_m.boucle_mod_rctt_lvr_csv(num_lvr_rctts, num_rctt)

        #1.2.0.SORTIR.
        if mod_rctt_ou_nn == 's':
            return 's'

        #1.2.1.CONTINUER.
        if mod_rctt_ou_nn == 'continuer':
            return 'continuer'


        print('La recette a été mise-à-jour avec succès. \
Voici le livre de recettes actuel, après les modifications apportées:\n')

        #TODO ajuster les dimensions de visionnement des df par défaut?
        #1.2.AFFICHER le livre de recette mis-à-jour.
        print(f'{e_l.df_des_rctts_un_lvr(num_lvr_rctts)}')

    
    #2.RETURN 'o' (oui et continuer), 
    #'n' (recette pas à modifier et continuer la boucle)
    #'s' (sortir)
    return mod_rctt_ou_nn




def aj_rctt_wbs_lvr_csv(num_lvr_rctts):
    """Ajouter une recette via les informations retirées par wbs.


    RETOURNE: 's', 'continuer', 'OK'

    
    @Afficher recettes

    """
    #1.DEMANDER lien web pour wbs.
    lien_web = input('Insérez le lien web pour initier le web-scrapping:\n')

    #2.0.
    if lien_web == 's':
        return 's'

    #2.1.VÉRIFIER si dans archvs déjà.
    lien_web = utl.gere_si_lw_wbs_dns_archv(lien_web, 'archv')

    #3.0.
    if lien_web in ['s', 'continuer']:
        return lien_web

    #TODO
    #3.1.RETIRER les informations de la page web.
    lst_infos_wbs = wbs.scrp_sln_site_web(lien_web)

    #TODO.3.REMPLACER par synonyme et afficher avant / après.


    #3.VALIDER, MODIFIER ou ANNULER les informations de ce lien web.
    lst_infos_mod = e_m.mod_lst_infos(lst_infos_wbs)

    #4.0.SORTIR.
    if lst_infos_mod in ['s', 'continuer']:
        return lst_infos_mod


    #4.1.AJOUTER les informations à la liste de recette.
    return e_m.envyr_modif_lvr_rctts_csv(num_lvr_rctts, 'nouvelle', lst_infos_mod)




#%% Ingrédients épicerie
def affchr_epcr_et_chcks(nm_fchr_epcr):
    """Vérifier si la liste d'épicerie existe. Si elle n'existe pas, la créer,
    puis afficher les informations dans la liste d'épicerie.


    RETOURNE: 's' ou 'nm_fchr_epcr' <- potentiellement nouveau.


    @Ingrédients épicerie

    """
    #1.CHECK si la liste d'épicerie existe. (False si existe po)
    chck_exst_ou_nn = utl.chck_lst_epcr_exst(nm_fchr_epcr)

    #2.IF CHECK FALSE; le nom du ficher est inexistant.
    if not chck_exst_ou_nn:
        #2.1.AFFICHER problème encontré.
        print("Fichier non-existant.\n")

        #2.2.AIDE à la création d'un fichier.
        nm_fchr_epcr = e_m.creer_nouv_lst_epcr(nm_fchr_epcr)

        #2.3.
        if nm_fchr_epcr == 's':
            return 's'


    #3.0.OBTENIR le df de la liste d'épicerie.
    df_lst_epcr = e_l.df_lst_epcr(nm_fchr_epcr)

    #3.AFFICHER la liste
    print(f"Voici la liste d'épicerie depuis le document \
{nm_fchr_epcr} :\n\n{df_lst_epcr}")

    #4.CHECK si organisée selon le profil par défaut.
    if chck_exst_ou_nn:
        #4.0.VÉRIFIER.
        chck_dft = utl.chck_epcr_clnns_dft(nm_fchr_epcr)

        #4.1.SI chck_dft = Faux, alors la liste est pas organisé selon le profil.
        if not chck_dft:
            #4.1.1.INFORMER de la problématique.
            print("La liste d'épice n'est pas ordonné comme le profil par défaut \
actuel le demande. Elle peut être ordonnée comme tel, à moins que..")

            #4.1.2.PROPOSER un changement de profil par défaut utilisé.
            prfl_dft = e_m.chx_prfl_dft()

            #4.1.3.
            if prfl_dft == 's':
                return 's'

            #TODO réorganiser la liste d'épicerie séparément?
            #TODO obtenir tous les ingrédients plus lw et nm_rctt séparés.
            #TODO les trier selon la valeur par défaut
            #TODO faire des .csv pour chaque profil par défaut ? (initialement, importer les épiceries
            #ou incorporer la liste maître.)


    #5.RETOURNER un nom d'épicerie potentiellement nouveau.
    return nm_fchr_epcr




def option_wbs_lst_epcr(nm_fchr_epcr):
    """Retirer les informations d'une recette par web-scrapping (wbs).


    RETOURNE: 's', 'continuer' ou wbs_info


    @Constuire list - iu_argparse_main

    """
    #1.DEMANDER le lien web pour le web-scrapping.
    lien_web = input("Quel est le lien web de la recette ?\n")


    #2.CHECK si lien web déjà retiré du web.

    #2.1.CHECK LISTE D'ÉPICERIE si lien web présent.
    #RETOURNE 'continuer', le lien web si pas déjà dans la liste d'épicerie.
    lien_web = utl.est_dans_lst_epcr_dj(lien_web, nm_fchr_epcr)

    #2.2.CHECK ARCHIVE RECETTES si lien web présent.
    #La fonction relance le même lien web que reçu si pas dans la liste de recette!
    lien_web = utl.gere_si_lw_wbs_dns_archv(lien_web)


    #3.0.SORTIR.
    if lien_web in ['s', 'continuer']:
        return lien_web


    #TODO 3.1.OBTENIR les ingrédients du web par "scrapping".
    wbs_infos = wbs.scrp_sln_site_web(lien_web)


    #TODO 4.REMPLACER par les synonymes et afficher avant / après.


    #5.GÉRER les infos scrapped (AFFICHER, DEMANDER SI OK ET SI MODIFIER).
    wbs_infos_mod = e_m.mod_lst_infos(wbs_infos)


    #6.0.SORTIR.
    if wbs_infos_mod in ['s', 'continuer']:
        return wbs_infos_mod


    #6.RETOURNER la liste d'info de la recette.
    return wbs_infos_mod




def option_archv_lst_epcr(nm_fchr_epcr):
    """Obtenir les ingrédients d'une recette des livres de recette archivés dans
    la liste d'épicerie.


    RETOURNE: 's' ou 'lst_infos_rctt_arch'


    @Ingrédients épicerie

    """
    #0.BOUCLE pour valider la recette choisie.
    continuer = 'u'
    while continuer == 'u':
        #1.0.AFFICHER les livres de recettes disponibles.
        txt_prsnttn = 'Les livres de recettes disponibles sont:'
        #1.1.DEMANDER un livre de recettes.
        inpt_txt = "Depuis quel livre de recettes désirez-vous extraire les ingrédients \
d'une recette?\n( # ) : "
        #1.2.PRÉPARER les numéros disponibles.
        lst_lvrs_rctts = e_l.lst_lvrs_rctts_csv()
        cndtn = [str(x+1) for x, lvr in enumerate(lst_lvrs_rctts)]
        #1.3.FORCER entrée.
        num_lvr_rctts = utl.boucle_chsr_entr_pls_rctts(
            txt_prsnttn, 'tous', None, inpt_txt, cndtn+['s']
        )


        #2.0.
        if num_lvr_rctts == 's':
            return 's', None


        #2.0.5.INDEX doit être int() et pas de s dont isnumeric()
        num_lvr_rctts = int(num_lvr_rctts)
        
        #2.1.AFFICHER les recettes du livre.
        txt_pres = f'Les recettes du livre de recette {lst_lvrs_rctts[num_lvr_rctts-1]} \
sont:'
        #2.2.DEMANDER une recette.
        inpt_text = "Laquelle de ces recettes aimeriez-vous ajouter à la liste \
d'épicerie?\n( # ) : "
        #2.3.PRÉPARER les conditions.
        lst_rctts = e_l.lst_rctts_depuis_csv(num_lvr_rctts)
        cndtn = [str(x+1) for x, rctt in enumerate(lst_rctts)]
        #2.4.FORCER entrée.
        num_rctt = utl.boucle_chsr_entr_pls_rctts(
            txt_pres, num_lvr_rctts, 'toutes', inpt_text, cndtn
        )


        #3.0.
        if num_rctt == 's':
            return 's'


        #3.0.5.INDEX doit être int() et pas de s dont isnumeric()
        num_rctt = int(num_rctt)
        
        #3.1.CONFIRMER la sélection ou recommencer-la.
        txt_inpt = '\nVeuillez;\n - (c)onfirmer ce choix de recette,\n\
 - (u)tiliser une autre recette ou\n - (s)ortir du programme\n( c / u / s ) : '
        #3.2.FORCER entrée
        continuer = utl.boucle_chsr_entr_pls_rctts(
            None, num_lvr_rctts, num_rctt, txt_inpt, ['c', 'u', 's'], ingr='tous'
        )


        #4.0.continuer = c ou u c'est OK car recommencer ou continue
        if continuer == 's':
            return 's'


    #5.ENVOYER informations.
    return e_l.lst_ingr_rctt_csv(num_lvr_rctts, num_rctt)


#TODO - mod une info donc show toute la liste. 
#ajouter un ingr seulement prcque rctt / lien web est dans les deux autres options.
def option_mod_manl_lst_epcr(nm_fchr_epcr):
    """Ajouter des ingrédients manuellement à la liste d'épicerie.


    RETOURNE: 's' ou 'OK'


    @Ingrédients épicerie

    """
    #TODO afin d'augmenter la rapidité, il n'est pas nécessaire de confirmer chaque changements
    #individuels.






#TODO - En général mais itout quoi mettre où parce qu'il me manque la place des titres de recettes.
#Si il y a des éléments non-triés, demander où les mettre. (Option changer de profil par défaut.)
def aj_lst_a_lst_epcr(source_info, lst_infos, nm_fchr_epcr):
    """Ajouter les ingrédients à la liste d'épicerie.
    
    
    RETOURNE:


    @options_wbs - iuf - Construire liste - Web-scrapping

    """
    #1.OBTENIR le df de la liste d'épicerie.
    df_lst_epcr_ini = e_l.df_lst_epcr(nm_fchr_epcr)

    #2.DIVISER le df en colonnes.
    lst_lst_epcr_ini = []
    for col in df_lst_epcr_ini:
        #OBTENIR "[[lst_rctt], [lst_lwb], [lst_epcr_1], [lst_epcr_2], etc.]
        lst_lst_epcr_ini += [[df_lst_epcr_ini] + df_lst_epcr_ini[col]]

    #TODO trier la liste d'épicerie selon le profil par défaut.
    df_infos_fnl = print('TRIER les ingrédients.')
    

    #5.ENVOYER la liste d'épicerie
    e_m.envyr_lst_epcr_csv(nm_fchr_epcr, df_infos_fnl)


    return 'OK'




def prtgr_wbs_a_archv_ou_nn(wbs_infos):
    """Demander si l'utilisateur est intéressé à partager cette liste d'informations
    à un livre de recettes en particulier ou non.
    SI OUI : s'occupe de partager les informations demandée.


    RETOURNE: 's' ou None


    @option_wbs_lst_epcr

    """
    #1.DEMANDER si les infos sont à ajouter à un livre de recettes ou non.
    txt_inpt = 'Désirez-vous ajouter cette recette retirée du web dans un livre \
de recette?\n ( o / n ) : '
    #1.0.FORCER entrée
    ajtr_ou_nn = utl.boucle_frc_entr_lwrcs(txt_inpt, ['o', 'n', 's'])


    #2.SI OUI, lequel?
    if ajtr_ou_nn == 'o':
        #2.0.AFFICHER questions.
        txt_pres = 'Voici les livres de recettes disponibles.'
        inpt_txt = 'Dans lequel de ces livres désirez-vous ajouter la recette?\n\
(#) : '
        #2.0.1.PRÉPARER les conditions.
        lst_lvrs_rctts = e_l.lst_lvrs_rctts_csv()
        lst_nums_lvrs_rctts = [str(x+1) for x, lvr in enumerate(lst_lvrs_rctts)]

        #2.1.FORCER l'entrée
        num_lvr_rctts = utl.boucle_chsr_entr_pls_rctts(
            txt_pres, 'tous', None, inpt_txt, lst_nums_lvrs_rctts+['s']
        )

        #2.2.OMETTRE l'option 'sortir'.
        if num_lvr_rctts != 's':
            #2.2.0.EST str car input().
            num_lvr_rctts = int(num_lvr_rctts)
            
            #2.2.1.AJOUTER les informations au livre de recette.
            e_m.envyr_modif_lvr_rctts_csv(num_lvr_rctts, 'nouvelle', wbs_infos)

            #2.2.2.AFFICHER le message de succès
            print(f"\nCette recette est ajoutée au livre de recette \
'{lst_lvrs_rctts[num_lvr_rctts-1]}'.\nSi vous désirez l'ajouter dans livre de \
recette supplémentaire, veuillez utiliser l'option 'Gérer livres recettes' de ce \
programme..Merci !!\n\n")

            return None


    #3.
    if 's' in [ajtr_ou_nn, num_lvr_rctts]:
        return 's'


    #4.ELSE, ajtr_ou_nn == 'n'.
    return None
