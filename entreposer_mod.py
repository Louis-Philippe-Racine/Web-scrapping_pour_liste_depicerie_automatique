# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 19:58:08 2023

@author: Dr. CiDre
"""

"""Module comportant des fonctions pour l'entreposage des données. En somme
il fonctionne à modifier les fichiers d'entreposage."""

#IMPORTER module créer par Dr. CiDre
import entreposer_lire as e_l
import utilitaire as utl

#IMPORTER module Python
import pandas as pd




def mod_lst_infos(lst_infos_rctt):
    """Après avoir obtenu la liste d'information d'une recette:
        - Afficher les infos,
        - Demander:
            1.Modifier indx.nouvelleinfo;
            2.Échanger rang, bouger indx à indx;
            3.Voir la recette;
            4.Confirmer la recette;
            5.Supprimer un info (outre 0,1);
            5.Help


    RETOURNE: 's', 'continuer', 'lst_infos_mod'


    @boucle_mod_rctt_lvr_csv
    @option_wbs - iuf - Constuire liste
    @gere_si_lw_wbs_dns_arch - utl - Gérer si dans archive

    """
    print("Voici les informations complètes de cette recette:\n")

    for indx, info in enumerate(lst_infos_rctt):
        print(f'{indx} - {info}')

    #1.BOUCLE MODIFIER cette liste d'information.
    cntnuer_cnfrmtn = True
    lst_infos_mod = lst_infos_rctt
    while cntnuer_cnfrmtn:
        #DEMANDER si OK ou modifier les infos.
        dmnde_actn = input("""Désirez-vous:
 - Modifier une de ces informations (#.nouvelleinfo);
 - Échanger le rang des ingrédients dans la liste (#ingr1.#ingr2)
 - (c)onfirmer ces informations;
 - (r)ecommencer le processus avec une autre liste d'info deleter
 - (d)eleter une information (d.#ingr) ou
 - (h)elp.
( #.nouvelleinfo / #ingr1.#ingr2 / a / r / d.#ingr / h ) : """) 


        #1.0.(S)ORTIR du programme.
        if dmnde_actn.lower() == 's':
            return 's'



        #1.1.(R)ECOMMENCER la boucle.
        if dmnde_actn.lower() == 'r':
            return 'continuer'



        #1.2.(V)OIR la recette à jour.
        if dmnde_actn.lower() == 'v':
            #AFFICHER la recette et redébutter la boucle while.
            print('Voici les informations à jour de la recette :\n')

            for indx, info in enumerate(lst_infos_mod):
                print(f'{indx} - {info}')

            continue



        #1.3.(C)ONFIRMER ces informations.
        if dmnde_actn.lower() == 'c':
            #1.3.1.SKIP le check final si liste non modifiée
            if lst_infos_rctt == lst_infos_mod:
                return lst_infos_rctt


            #1.3.2.AFFICHER la liste d'épicerie à jour
            print('Voici les informations finales à envoyer:\n')

            for indx, info in enumerate(lst_infos_mod):
                print(f'{indx} - {info}')    

            #1.3.3.DEMANDER la confirmation de l'envoie
            inpt_txt = input("(C)onfirmez-vous cet envoie ou désirez-vous le \
(m)odifier avant d'envoyer?\n( c / m ) : ")
            #1.3.3.0.FORCER la réponse.
            envyr_ou_nn = utl.boucle_frc_entr_lwrcs(inpt_txt, ['c', 'm', 's'])


            #1.3.4.SI CONFIRMÉ, renvoyer la liste.
            if envyr_ou_nn == 'c':
                return lst_infos_mod


            #1.3.5.SI À MODIFIER, continue la boucle de modification SINON ERREUR.
            if envyr_ou_nn == 'm':
                continue


            #1.3.5.6.ELSE 's'
            return 's'



        #1.4.(H)ELP pour l'écriture de modification.
        if dmnde_actn.lower() == 'h':
            print("\n\n\
 - Pour la modification d'information, le format est 'chiffre', \
'.' et 'nouvelle information';\n\n\
**(Pour ajouter un ingrédient, insérez un chiffre plus grand que le nombre \
max actuel dans cette recette. Aussi, l'option indx1 = 1 est indisponible.')**\n\n\
Un exemple de format pour changer une information:\n\
3.2 Broccolis\n\n\
Ou encore:\n\
0.Toasts au ketchup\n\n\n\
 - Pour l'échange d'emplacement des ingrédients dans la liste, inscrivez les numéros \
associés aux deux ingrédients (donc >1), en format 'chiffre', '.' puis 'chiffre' comme par exemple:\n\
3.4\n\
 - Pour 'deleter' une information, inscrivez 'd', '.', puis chiffre de l'index à enlever.n\n\n\
Autrement,\n - 'v' permet de voir la liste avec les modifications effectuées,\n\n\n\
 - 'c' permet de confirmer la liste actuel et de la partager ainsi.\n\n\
 - 'r' et 's' permettent de sortir de la boucle de modification d'une liste \
d'information.\n")

            continue



        #1.5.DIVISER l'input.
        lst_modif = dmnde_actn.split('.')

        #1.6
        if len(lst_modif) > 1:
            #1.6.1.SI modifié ou échanger (#.info ou #.#). 1 car cela change le lien web.
            if lst_modif[0].isnumeric() and lst_modif[0] != 1:
                #1.6.0.STR puisque input.
                index = int(lst_modif[0])
            

                #1.6.1.1.OPTION MODIFICATION. (#.info)
                if not lst_modif[1].isnumeric():
                    #1.6.1.0.UN nombre > len() veut dire qu'on instaure une nouvelle info.
                    if index > len(lst_infos_mod):
                        lst_infos_mod += [lst_modif[1]]
                        continue


                    #TODO créer liste des changements de mots (demander si on enregistre comme mots synonymes si
                    #les infos non numériques changent.) Envoyer cette liste au dictionnaire. ALSO if not index>len() donc else.
                    #1.6.1.1.SINON on modifie une entrée existante.
                    lst_infos_mod[index] = lst_modif[1]
                    continue


                #1.6.1.2.OPTION ÉCHANGE. (#.#) Si index < 1, pas un ingrédient donc erreur.
                #Aussi, nécessairement numérique vue le check précédent en 1.6.1.
                if index > 1:
                    #ÉCHANGER les positions de manière pythonesque! ;)
                    (lst_infos_mod[index],
                     lst_infos_mod[lst_modif[1]]) = (lst_infos_mod[lst_modif[1]],
                                                     lst_infos_mod[index])
                    continue


            #1.6.2.VÉRIFIER si deleter. Vérifier numérique sinon donne erreur next.
            if lst_modif[0].lower() == 'd' and lst_modif[1].isnumeric():
                #1.6.2.0.STR can input à la base.
                lst_modif = int(lst_modif)
                #1.6.2.1.SI 2<index<len(), l'entrée est valide.
                if 1<lst_modif[1]<=len(lst_infos_mod):
                    #1.6.2.2.SUPPRIMER de la liste.
                    lst_modif = lst_infos_mod.pop(lst_modif)


        #1.7.ELSE, l'entrée est invalide.
        print('''Cette entrée est invalide. Écrivez "h" pour plus d'information sur
les entrées de modifications de la recette.''')
        continue    



#%% Livre de recettes
def boucle_mod_rctt_lvr_csv(num_lvr_rctts, num_rctt):
    """Gérer les étapes permettant de modifier un liste d'information pour finalement
    modifier/ajouter une recette dans les archives.


    RETOURNE: 's', 'continuer', 'OK'


    @mod_la_rctt_affchr - iuf - Afficher recettes csv
    @ajtr_man_une_rctt - iuf - Afficher recettes csv

    """
    print("Modifions la liste de recettes manuellement ensemble !!\n")

    #1.1.OPTION nouvelle recette requiert un nom premièrement puis entre dans la boucle normale.
    lst_info_rctt = ''
    if num_rctt == 'nouvelle':
        #1.1.1.DEMANDER le nom pour la nouvelle recette.
        nm_rctt = input('Quel nom désirez-vous donner à la recette ?\n ')

        #1.1.2.0.
        if nm_rctt == 's':
            return 's'


        #1.1.2.CRÉER liste et assigner nm_rctt.
        lst_info_rctt = [nm_rctt]


    #1.2.OBTENIR liste d'information de la recette si pas une "nouvelle".    
    if lst_info_rctt == '':
        lst_info_rctt = utl.lst_ingr_rctt_csv(num_lvr_rctts, num_rctt)


    #2.GÉRER la boucle de modification, retourner [infos modifiées], 's' ou 'continuer'
    lst_infos_mod = mod_lst_infos(lst_info_rctt)

    #3.0.SORTIR.
    if lst_infos_mod == 's':
        return 's'

    #3.1.CONTINUER.
    if lst_infos_mod == 'continuer':
        return 'continuer'

    #3.2.ENVOYER la liste d'information modifié au livre de recette.
    return envyr_modif_lvr_rctts_csv(num_lvr_rctts, num_rctt, lst_infos_mod)




def envyr_modif_lvr_rctts_csv(num_lvr_rctts, num_rctt, lst_infos_mod):
    """Envoyer la liste d'information complètement modifier au livre de recettes.csv


    RETOURNE: 'OK'


    @boucle_mod_rctt_lvr_csv
    @gere_si_lw_wbs_dns_arch - utl - Vérifier si dans archive

    """
    #1.OBTENIR df du livre de recettes.
    df_rctts = e_l.df_des_rctts_un_lvr(num_lvr_rctts)
    #2.CRÉER nouveau df avec la liste d'information.
    df_nouv_infos = pd.DataFrame({lst_infos_mod[0]: [lst_infos_mod[1:]]})

    #3.GÉRER le cas de modification d'une recette (enlever l'ancienne recette avant).
    #Une nouvelle recette -> jamais numérique -> num_rctt = 'nouvelle'.
    if num_rctt.isnumeric():
        #3.0.OBTENIR la liste des noms de recettes.
        lst_rctts = e_l.lst_rctts_depuis_csv(num_lvr_rctts)
        #3.1.TROUVER le nom de la recette pour le df.
        nm_rctts = lst_rctts[num_rctt-1]
        #3.2.ENLEVER la recette à modifier pour ensuite la remplacer.
        df_rctts = df_rctts.drop(columns=nm_rctts)

    #4.JOINDRE les recettes et les ordonner.
    df_rctts = pd.merge(df_rctts, df_nouv_infos, how='outer', left_index=True,
                            right_index=True).sort_index(axis=1)

    #5.OBTENIR le chemin d'accès au livre de recette '.csv'.
    pth_lvr_rctt = f'{utl.chmn_accs_lvrs_rctts_dir()}/\
{e_l.lst_lvrs_rctts_csv()[num_lvr_rctts-1]}'
    
    #6.ENVOYER le df au livre de recette '.csv'.
    df_rctts.to_csv(pth_lvr_rctt, sep=';', encoding='latin', index=False)
    
    return 'OK'




#%% Liste d'épicerie
def creer_nouv_lst_epcr(nm_fchr_epcr):
    """Créer une nouvelle liste d'épicerie si inexistante.


    RETOURNE: 's' ou 'nm_fchr_epcr' <- potentiellement nouveau.

    @Ingrédients épicerie

    """
    #0.DEMANDER si le nom est OK
    txt_inpt = f"Désirez-vous (c)réer une liste d'épicerie portant le nom \
{nm_fchr_epcr} ou (m)odifier le nom de fichier pour la nouvelle liste d'épicerie ?\n\
( c / m ) :"
    #0.1.FORCER l'entrée
    crr_ou_mod = utl.boucle_frc_entr_lwrcs(txt_inpt, ['c', 'm', 's'])


    #1.SI MODIFIER, modifier le nom.
    if crr_ou_mod == 'm':
        #1.0.BOUCLE pour confirmer le nouveau nom.
        while crr_ou_mod in ['m', 'n']:
            #1.1.MODIFIER le nom.
            nm_fchr_epcr = input("Quel nom désirez-vous donner à la liste d'épicerie \
d'aujourd'hui ?\n")

            #1.2.VALIDER le nouveau nom.
            inpt_txt = "Vous confirmer le nom '{nm_fchr_epcr}'? ( o / n ) : "
            #1.2.0.FORCER l'entrée
            crr_ou_mod = utl.boucle_frc_entr_lwrcs(inpt_txt, ['o', 'n', 's'])


    #2.0.
    if crr_ou_mod == 's':
        return 's'


    #2.CRÉER la nouvelle liste d'épicerie selon le profil par défaut.
    #2.1.OBTENIR la liste des noms de colonnes.
    lst_clnns_dft = e_l.lst_entt_epcrs_par_dft()

    #2.2.DÉBUTER le df des colonnes de la liste d'épicerie.
    df_clnns_dft = pd.DataFrame()

    #2.3.AJOUTER les colonnes par défaut.
    for clnn in lst_clnns_dft:
        df_clnns_dft[clnn] = []


    #3.CRÉER le .csv de la liste d'épicerie.
    envyr_lst_epcr_csv(nm_fchr_epcr, df_clnns_dft)

    return nm_fchr_epcr



#TODO
def mod_lst_epcr(nm_fchr_epcr, df_infos):
    """Gérer la modification de la liste d'épicerie déjà créée
    """
    
    

    return




def envyr_lst_epcr_csv(nm_fchr_epcr, df_infos_fnl):
    """Envoyer la liste d'épicerie travaillé à la liste d'épicerie.
    Cette fonction créer une liste d'épicerie si celle-ci n'existe pas


    RETOURNE: None


    @creer_nouv_lst_epcr

    """
    #0.OBTENIR le chemin d'accès de la liste d'épicerie
    lst_epcr_pth = utl.chmn_accs_dir_lsts_epcr(nm_fchr_epcr)

    #1.ENVOYER OU CRÉER la liste à jour dans la liste d'épicerie .csv.
    df_infos_fnl.to_csv(lst_epcr_pth, sep=';', encoding='latin', index=False)

    return None




#TODO
#%% Profil par défaut
#TODO
def mod_prfl_dft():
    """Gérer la modification du profil par défaut.
    """