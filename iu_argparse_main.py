# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 18:28:35 2023

@author: Dr. CiDre
"""

"""Module d'interface visuel en Argparse du programme de liste d'épicerie
automatique."""

#IMPORTER les modules créés par Dr. CiDre.
import iu_argparse_fncts as iuf
from entreposer_lire import lst_lvrs_rctts_csv, affchr_lsts_epcr_dspnbl
from entreposer_mod import boucle_mod_rctt_lvr_csv
from utilitaire import boucle_frc_entr_lwrcs


#IMPORTER le module Python.
import subprocess



#%% Préambule
#DOTEXE - Ouvre invite de commande automatiquement:
subprocess.Popen(['start', 'cmd', '/k',
                  "title  - * Liste d'épicerie automatique par web-scraping * - & type epicerie_startup.txt"], shell=True)





#TODO print quel paramètre par défauts ils utilisent, et / ou quel profil.Plus:
print("Dans n'importe quel input, écrire 's' pour sortir de l'option \
proposée !!.\n")



#DÉBUTE ce programme et oriente selon l'entrée.
if __name__ == "__main__":
    arg = iuf.analyse_cmd_wndw_inpt()

    print("Construisons ta liste ensemble !!!.\n")

    #TODO changer print par défaut.

    #TODO implémenter arg.utilisateur:
    #check if utilisateur possible ou add un profil
    nm_prfl = iuf.gere_si_prfl_exst_ou_nn(arg.utilisateur)


#TODO LONG-TERME, permettre d'afficher les instructions pour que je pusise l'utiliser en cuisine avec des checkboxs.
#%% Ajouter au livre de recettes   
    #BOUCLE afficher liste de recette
    if arg.ajouter_au_livre_de_recettes:
        print("\nDans n'importe quel input, écrire 's' pour sortir de l'option \
proposée !!.\n")

        #Continuer de voir/modifier des recettes sans sortir
        #de cette partie du programme. (s = sortir, t = terminer)
        prog_lst_rctts = ''
        while prog_lst_rctts != 's':

            #0.DEMANDER de choisir entre voir/modifier, ajouter manuelllement
            #ou ajouter par web-scrape. Aussi, recevoir le num_lvr rctts d'intérêt.
            prog_lst_rctts, num_lvr_rctts = iuf.chx_dprt_aj_au_lvr_rctt()


            #1.1.OPTION VOIR/MOD: CHOISIR afficher une recette et la modifier.
            if  prog_lst_rctts == 'v':
                #1.1.1.OPTION VOIR une recette selon un chiffre ou non.
                prog_lst_rctts = iuf.voir_une_rctte(num_lvr_rctts)               


            #1.2.OPTION WEB-SCRAPING.
            elif prog_lst_rctts == 'w':
                prog_lst_rctts = iuf.aj_rctt_wbs_lvr_csv(num_lvr_rctts)


            #1.3.OPTION AJOUTER MANUELLEMENT.
            elif prog_lst_rctts == 'm':
                prog_lst_rctts = boucle_mod_rctt_lvr_csv(num_lvr_rctts, 'nouvelle')


            #1.4.0.
            #1.4.SORTIR puisque demander par l'utilisateur.
            if num_lvr_rctts == 's':
                prog_lst_rctts_cont = 's'


            #1.4.1.CLAMER succès et recommencer la boucle.
            elif prog_lst_rctts == 'OK':
                print(f'La recette est ajoutée/modifiée avec succès dans le livre\
de recettes : {lst_lvrs_rctts_csv[num_lvr_rctts-1]}!!\n..Bravo!!\n')




#%% Ingrédients épicerie
    #TODO
    #BOUCLE création ou agrandissement de la liste d'épicerie.
    if arg.ingr_lst_epcr:
        #0.AFFICHER informations sur quitter la partie du programme.
        print("\nDans n'importe quel input, écrire 's' pour sortir de l'option \
création de liste d'épicerie !!.\n")

        #0.1.AFFICHER les listes d'épiceries disponibles.
        affchr_lsts_epcr_dspnbl()

        #00.DEMANDER un nom.
        nm_fchr_epcr = input("Écrivez le nom de la nouvelle liste d'épicerie \
ou le nom de la liste archivée à utiliser :\n")


        #POUVOIR ajouter des recettes en boucle.
        continuer = True
        while continuer:
            #1.CHECK si existant ET AFFICHER liste d'épicerie.
            nm_fchr_epcr = iuf.affchr_epcr_et_chcks(nm_fchr_epcr)


            #2.0.
            if nm_fchr_epcr == 's':
                continuer = False
                continue


            #2.CHOISIR source de la recette.
            inpt_text = "Désirez-vous ajouter les ingrédients;\n - d'une recette \
provenant du (w)eb,\n - de recettes (a)rchivées,\n - (m)odifier la liste\
(m)anuellement ou,\n - de (s)ortir du programme?\n( w / a / m / s ) : "
            #2.0.FORCER une entrée valide parmis: (w), (a) ou (s)ortir             
            src_rctt = boucle_frc_entr_lwrcs(inpt_text, ['w', 'a', 'm', 's'])


            #3.1.OPTION WEB-SCRAPPING
            is_wbs = ''
            if src_rctt == 'w':
                lst_infos = iuf.option_wbs_lst_epcr(nm_fchr_epcr)


            #3.2.OPTION ARCHIVE: prendre ingrédients d'une recette archivée.
            elif src_rctt == 'a':
                lst_infos = iuf.option_archv_lst_epcr(nm_fchr_epcr)


            #TODO
            #3.3.OPTION AJOUTER MANUELLEMENT.
            elif src_rctt == 'm':
                lst_infos = iuf.option_mod_manl_lst_epcr(nm_fchr_epcr)


            #4.0.
            if lst_infos == 's':
                continuer = False

            #4.1.RECOMMENCER.
            elif lst_infos == 'continuer':
                continue


            #4.2.ELSE ENVOYER les nouvelles informations à la liste d'épicerie.
            #TODO envoyer infos à la liste. (Faire une boucle??)
            iuf.aj_lst_a_lst_epcr(src_rctt, lst_infos, nm_fchr_epcr)    

            
            #5.AFFICHER le message de succès avant de recommencer.            
            print(f"Informations ajoutées à la liste d'épicerie \
'{nm_fchr_epcr}' avec succès!\nToutes mes félicitations !!\n\n")


            #6.WBS DEMANDER si ajouter à archv ou nn.
            if src_rctt == 'w':
               cntnr_ou_nn = iuf.prtgr_wbs_a_archv_ou_nn(lst_infos)

               #6.1.
               if cntnr_ou_nn == 's':
                   continuer = False


#TODO
#%% Gérer liste épicerie
    #TODO BOUCLE enlever, de la liste d'épicerie, les ingrédients d'une recette.
    #TODO trier les ingrédients selon épiceries
    #TODO gérer masterfile et/ou rang dans les épiceries.
    if arg.gérer_liste_epicerie:
        pass
    #TODO idée : mettre noms d'épicerie ou une liste pour qu'avant d'envoyer la liste, ça donne l'erreur pas ordonnée.



#TODO copier une recette, supprimer une recette, (ajouter une omission de mot dans les ingrédients.)
#%% Gérer livres recettes
    if arg.gérer_livre_recettes:
        pass
    #TODO ajouter un livre avec qqch d'écrit car csv_read retourne erreur sinon


#TODO
#%% Partager liste
    #FINALISER et envoyer la liste à G_Keep et Favoris
    if arg.partager_liste:
        #TODO montrer puis forcer choix entre plusieurs listes d'épicerie

        #TODO MONTRER la liste d'épicerie soit en format tableau ou boucle for print

        #TODO FORCE input.
        #VEUT-IL vraiment l'envoyer?
        Envoie_check = input('\nVoulez-vous vraiment envoyer cette liste à \
Google Keep et aux favoris de Chrome ?\n( o / n ) : ').lower()

        #PAS à envoyer?
        if Envoie_check != 'o':
            print(f"\nListe d'épicerie pour {arg.nom_fichier_epicerie} NON-partagée.")
            
        #TODO ENVOYER la liste à G_Keep et aux favoris dans Chrome.
        else:
            #(Voir excel "Structure" pour layout)
            pass


#TODO - Par défaut, quel ordre (rang et épicerie) pour ajouter une recette dans la liste d'épicerie
#TODO - "        ", enregistrer la liste ou non.
#%% Profils par défaut
