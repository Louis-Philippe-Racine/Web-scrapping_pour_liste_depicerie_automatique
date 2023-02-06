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



#TODO faire premier troubleshooting.
#%% Modification d'une liste
def prep_lst_epcr_pr_mli(nm_fchr_epcr):
    """Préparer la liste d'épicerie pour la tâche ardueuse de la modifier manuellement
    avec le programme.


    RETOURNE: [[lst_infos], [lst_entts]]




    """
    #1.OBTENIR le df de la liste d'épicerie
    df_lst_epcr = e_l.df_lst_epcr(nm_fchr_epcr)


    #2.OBTENIR les entêtes de la liste d'épicerie
    lst_entts_epcr = [entt for entt in df_lst_epcr]


    #3.CRÉER la liste d'info unique de la liste d'épicerie avec les #indexs.
    lst_lst_epcr = []
    for entt in lst_entts_epcr:
        lst_lst_epcr += [entt]
        for info in df_lst_epcr[entt]:
            if info:
                lst_lst_epcr += [info]

    #4.REVOYER [[lst_infos], [lst_entts]]
    return lst_lst_epcr, lst_entts_epcr



#TODO check l'option profil par défaut parce que chaque modif emporte des changements dans les .csv
#et dans les noms de fichiers.
def mod_lst_infos(lst_infos, type_lst):
    """Après avoir obtenu la liste d'information d'une recette:
        - Afficher les infos,
        - Demander:
            1.Modifier indx.nouvelleinfo;
            2.Échanger rang, bouger indx à indx;
            3.Voir la recette;
            4.Confirmer la recette;
            5.Supprimer un info (outre 0,1);
            5.Help

    *type_lst = 'la recette', 'le profil par défaut', 'la liste d'épicerie'


    RETOURNE: 's', 'continuer', 'lst_infos_mod'


    @boucle_mod_rctt_lvr_csv
    @option_wbs - iuf - Constuire liste
    @gere_si_lw_wbs_dns_arch - utl - Gérer si dans archive

    """
    #0.AFFICHER les informations avant la boucle.
    print("Voici les informations complètes pour {type_lst}':\n")

    mli_affchr_sln_type_lst(lst_infos, type_lst)

    #1.BOUCLE MODIFIER cette liste d'information.
    cntnuer_cnfrmtn = True
    lst_infos_mod = lst_infos
    while cntnuer_cnfrmtn:
        #0.1.DEMANDER si OK ou modifier les infos.
        dmnde_actn = input("""Désirez-vous:
 - (c)onfirmer ces informations;
 - (r)ecommencer le processus avec une autre liste d'information;
 - Modifier une de ces informations (#.nouvelleinfo);
 - Échanger le rang de ces informations dans la liste (#info1.#info2)
 - Supprimer une information (s.#info) ou
 - (v)oir la recette avec ses informations à jour.
 - (h)elp.
( #.nouvelleinfo / #info1.#info2 / a / r / d.#info / h ) : """) 


        #1.0.(S)ORTIR du programme.
        if dmnde_actn.lower() == 's':
            return 's'


        #1.1.(R)ECOMMENCER la boucle.
        if dmnde_actn.lower() == 'r':
            return 'continuer'


        #1.2.(V)OIR la recette à jour.
        if dmnde_actn.lower() == 'v':
            #1.2.0AFFICHER la recette et redébutter la boucle while.
            print(f'Voici les informations à jour pour {type_lst} :\n')

            mli_affchr_sln_type_lst(lst_infos, type_lst)

            continue


        #1.3.(C)ONFIRMER ces informations.
        if dmnde_actn.lower() == 'c':
            #1.3.1.SKIP le check final si liste non modifiée
            if lst_infos == lst_infos_mod:
                return lst_infos


            #1.3.2.AFFICHER la liste d'épicerie à jour
            print('Voici les informations finales à envoyer:\n')

            mli_affchr_sln_type_lst(lst_infos, f'{type_lst} finale')    

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
            mli_help()
            continue


        #2.0.TRIER selon les types de modifications
        #Types = Ajouter, Modifier, Échanger ou Supprimer de l'information.
        entr_mod_splt = dmnde_actn.split('.')
        nouv_lst_infos_mod = lst_infos_mod

        #2.0.1.SI split plus qu'une fois, remettre ensemble avec des points.
        if len(entr_mod_splt) > 1:
            entr_mod_splt = entr_mod_splt[0] + '.'.join(entr_mod_splt[1:])

        #2.0.2.INT pour les indexes, à gerer avant les multiples checks et utilisation.
        for indx, entr in enumerate(entr_mod_splt):
            if entr.isnumeric():
                entr_mod_splt[indx] = int(entr)

        #2.0.2.TROUVER le type de modification choisie par l'utilisateur.
        type_mod = tri_si_mod_echngr_ou_supprmr(entr_mod_splt, lst_infos_mod)


        #2.1.OPTION AJOUTER une information (On ne peut qu'en ajouter une à la fin.)
        if type_mod == 'ajtr':
            #2.1.1.LISTE D'ÉPICERIE a un format différent que les autres.
            if type_lst == "la liste d'épicerie":
                lst_infos_mod[0] += [entr_mod_splt[1]]

            else:
                lst_infos_mod += [entr_mod_splt[1]]


        #2.2.OPTION MODIFIER une information.
        elif type_mod == 'mod':
            nouv_lst_infos_mod = mli_gerer_mod(entr_mod_splt, lst_infos_mod, type_lst)


        #2.3.OPTION ÉCHANGER des informations.
        elif type_mod == 'echngr':
            nouv_lst_infos_mod = mli_gerer_echng(entr_mod_splt, lst_infos_mod, type_lst)


        #2.4.OPTION SUPPRIMER une information.
        elif type_mod == 'supprmr':
            nouv_lst_infos_mod = mli_gerer_supprmr(entr_mod_splt, lst_infos_mod, type_lst)


        #3.SI liste a été modifiée, alors l'entrée était valide.
        if nouv_lst_infos_mod != lst_infos_mod:
            print("\nSuccès!!\n")
            
            #3.1.METTRE la liste modifiée à jour et continuer la boucle.
            lst_infos_mod = nouv_lst_infos_mod
            continue


        #4.TOUTE les autres options signifient que l'entrée est invalide.
        print(f"Cette entrée, {dmnde_actn}, est invalide. Écrivez 'h' pour plus \
d'information sur les entrées de modifications de la recette.")
        continue    




def mli_affchr_sln_type_lst(lst_infos, type_lst):
    """Afficher une liste selon son type (liste d'épicerie est plus complexe
    à modifier).
    *type_lst = 'la recette', 'le profil par défaut', 'la liste d'épicerie'
    *(suite): f'{type_lst} final'


    RETOURNE: None (print lst_infos)


    @mod_lst_infos

    """
    #1.OPTION LISTE D'ÉPICERIE, INITIALE ou FINALE
    if "la liste d'épicerie" in type_lst:
        df_infos_epcr_ac_indx = prep_mli_affchr_df_lst_epcr(lst_infos, type_lst)
        print(df_infos_epcr_ac_indx.to_string(index=False, na_rep=''))


    #3.OPTION RECETTE ou PROFIL PAR DÉFAUT, INITIAL OU FINAL!
    else:
        for x, info in enumerate(lst_infos):
            print(f'{x} - {info}')


    return None




def prep_mli_affchr_df_lst_epcr(lst_infos, type_lst):
    """Préparer la liste d'informations de la liste d'épicerie afin de l'afficher
    sous forme df.
    *lst_infos = [[lst_infos_epcr], [lst_entt_epcr]]

    RETOURNE: df_lst_indxs_pls_infos


    @mliaffchr_sln_type_lst

    """
    #1.0.PRÉPARER un dictionnaire pour print en df après.
    dict_info_par_entt = {}

    #1.1.LES entêtes se trouves dans lst_infos[1]. On assigne le 1er pour pouvoir
    #ajouter "Optionnel pour ajouter" plus facilement
    entt = lst_infos[1][0]

    #1.2.CRÉER le dictionnaire avec les indexs associés aux modifications futures.
    for indx, info in enumerate(lst_infos[0][1:]):
        #1.2.1.SI c'est pas un entête, ajoute l'entrée d'emblée.
        if info not in lst_infos[1][1]:
            dict_info_par_entt[entt] = (dict_info_par_entt.get(entt, []) +
                                        [f'{indx} - {info}']
            )

            #1.2.1.1.C'EST nice d'avoir un option 'ajtr' si c'est le fin dernier.
            if info != lst_infos[0][-1]:
                continue

            #1.2.1.2.C'EST le dernier? Ajoute un indx de plus pour l'option 'ajtr'.
            indx += 1

        #1.2.2.SI l'info est un entt, changer la clef du dict et ajt l'option 'ajtr'.
        #1.2.2.1.FAIRE seulement si pas l'affichage de la liste finale.
        if type_lst == "la liste d'épicerie":
            dict_info_par_entt[entt] = (dict_info_par_entt.get(entt, []) +
                                        [f'  {indx} - Optionnel pour ajouter ingr']
            )

        #1.2.2.2. APRÈS avoir ajouté l'option 'ajtr', changer la clef.
        entt = info


    #2.CRÉER le dataframe de cette liste.
    df_lst_epcr_indx = pd.DataFrame()
    for entts in lst_infos[1]:
        #2.1.CONSTRUIRE un df temporaire.
        df = pd.DataFrame({entts: dict_info_par_entt.get(entts, [])})
        #2.2.AJOUTER le df temp au df_lst_epcr
        df_lst_epcr_indx = pd.merge(
            df_lst_epcr_indx, df, how='outer', left_index=True, right_index=True
        )


    #3.RETOURNER le df avec les infos indexés.
    return df_lst_epcr_indx




def tri_si_mod_echngr_ou_supprmr(entr_mod_splt, lst_infos_mod):
    """Définir comment changer la liste à modifier, soit en modifiant une information,
    en ajoutant une, en supprimant un ou en échangeant deux de position.


    RETOURNE: 'ajtr', 'mdfr', 'echngr', 'supprmr' ou None


    @mod_lst_infos
    """
    #1.SI il y a eu un split.
    if len(entr_mod_splt) > 1:
        #1.1.SI modifié ou échanger (#.info ou #.#).
        if isinstance(entr_mod_splt[0], int):
            #1.3.(#.info)
            if not entr_mod_splt[1].isnumeric():

                #1.3.0.LISTE D'ÉPICERIE a un format différent des autres type
                if len(lst_infos_mod) == 2:
                    lst_infos_mod = lst_infos_mod[0]

                #1.3.1.OPTION AJOUTER UN nombre > len() veut dire qu'on instaure une nouvelle info.                
                if entr_mod_splt > len(lst_infos_mod):
                    return 'ajtr'


                #1.3.2.SINON OPTION MODIFIER on modifie une entrée existante.
                return 'mod'


            #1.4.OPTION ÉCHANGER. car entr_mod_splt[1] est numérique. (#.#)
            return 'echngr'


        #1.2.VÉRIFIER si supprimer. Vérifier numérique sinon donne erreur next.
        if entr_mod_splt[0].lower() == 's' and entr_mod_splt[1].isnumeric():
            return 'supprmr'


    #2.ELSE, erreur.
    return None


#TODO créer liste des changements de mots (demander si on enregistre comme mots synonymes si
#les infos non numériques changent.) Envoyer cette liste au dictionnaire de l'archive.
def mli_gerer_mod(entr_mod_splt, lst_infos_mod, type_lst):
    """Gérer la modification demandée de la liste d'information selon le type de
    liste à modifier (recette, liste d'épicerie ou profil par défaut.
    *Liste d'épicerie - Pas de modification des recettes ou des entêtes.
    

    RETOURNE: lst_infos_mod


    @mod_lst_infos

    """
    #1.EXCEPTION LISTE D'ÉPICERIE
    if type_lst == "la liste d'épicerie":
        #1.1.ERREUR si mod recettes, donc indx < len(clnn_rctts).
        if entr_mod_splt[0] < len(lst_infos_mod[0].find(lst_infos_mod[1][1])):
            print(f"L'option '{entr_mod_splt[0]} - {lst_infos_mod[0][entr_mod_splt[0]]}' \
n'est pas valide car elle est une recette. Voir l'option 'h' pour plus d'information sur les \
modifications.\n")
            #ERREUR, retourner la même liste, mli annoncera gèrera l'erreur.
            return lst_infos_mod


        #1.2.AJOUTER si l'indx de changement est une entt, au lieu de remplacer.
        if lst_infos_mod[0][entr_mod_splt[0]] in lst_infos_mod[1]:
            lst_infos_mod[0].insert(entr_mod_splt[0], entr_mod_splt[1])

            #1.2.0.RETOURNER la liste avec l'ajout.
            return lst_infos_mod


        #TODO ajtr/prpsr d'ajouter au dictionnaire archivé des synonymes.
        #1.3.MODIFIER à l'index.
        lst_infos_mod[0][entr_mod_splt[0]] = entr_mod_splt[1]
        return lst_infos_mod


    #TODO si recette, demande si ajt au dictionnaire archivé des sysnonymes.
    #3.RECETTES aussi sans exception, on peut tout y modifier.
    lst_infos_mod[entr_mod_splt[0]] = lst_infos_mod[1]


    return lst_infos_mod


#TODO VALIDER la portion "Profil par défaut".
#TODO - et aussi ajouter dans le trie par défaut si liste d'épicerie ?
def mli_gerer_echng(entr_mod_splt, lst_infos_mod, type_lst):
    """Échanger la position de deux informations dans la liste.
    - Recette: Échanger des ingrédients seulement
    - Profil par défaut: Échanger que des épiceries.
    - Liste d'épicerie: Échanger des ingrédients et des épiceries


    RETOURNE: lst_infos_mod


    @mod_lst_infos

    """
    #1.OPTION LISTE D'ÉPICERIE.
    if type_lst == "la liste d'épicerie":
        #1.0.OBTENIR les indexs des entêtes.
        indx_entts = [lst_infos_mod[0].find(entt) for entt in lst_infos_mod[1]]

        #1.1.VÉRIFIER si échange d'entêtes ou non.
        if entr_mod_splt[0] in indx_entts or entr_mod_splt[1] in indx_entts:

            #TODO voulez-vous changer les entts par défaut?
            #1.1.1.SI les deux sont des entêtes, c'est valide.
            if entr_mod_splt[0] in indx_entts and entr_mod_splt[1] in indx_entts:
                #1.1.2.ÉCHANGER les positions de manière pythonesque! ;)
                (lst_infos_mod[0][entr_mod_splt[0]],
                 lst_infos_mod[0][entr_mod_splt[1]]) = (lst_infos_mod[0][entr_mod_splt[1]],
                                                        lst_infos_mod[0][entr_mod_splt[0]]
                )
            #1.1.3.RETOURNER la liste - sans mod si 1 seul entt, avec mod si 2 entts.
            return lst_infos_mod

        #TODO proposer d'ajouter ça dans le triage automatique.
        #1.2.VALIDE si après 1ère épicerie et avant le dernier ingrédient.
        if (indx_entts[2]<entr_mod_splt[0]<len(lst_infos_mod) or
            indx_entts[2]<entr_mod_splt[1]<len(lst_infos_mod)
            ):
            #1.2.1.ÉCHANGER les positions de manière pythonesque! ;)
            (lst_infos_mod[0][entr_mod_splt[0]],
             lst_infos_mod[0][entr_mod_splt[1]]) = (lst_infos_mod[0][entr_mod_splt[1]],
                                                    lst_infos_mod[0][entr_mod_splt[0]]
            )
        #1.2.2.RETOURNER la liste - sans mod si 1 seul entt, avec mod si 2 entts.
        return lst_infos_mod
                                                        

    #2.OPTION PROFIL PAR DÉFAUT ou RECETTE
    #2.1.CAS VALIDE:
    if 2<entr_mod_splt[0]<len(lst_infos_mod) or 2<entr_mod_splt[1]<len(lst_infos_mod):
        #2.1.ÉCHANGER les positions de manière pythonesque! ;)
        (lst_infos_mod[entr_mod_splt[0]],
         lst_infos_mod[entr_mod_splt[1]]) = (lst_infos_mod[entr_mod_splt[1]],
                                             lst_infos_mod[entr_mod_splt[0]]
        )

    #2.2.RETOURNER la liste modifiée ou non.
    return lst_infos_mod




def mli_gerer_supprmr(entr_mod_splt, lst_infos_mod, type_lst):
    """Supprimer l'information à l'index choisi.
    - On ne peut supprimer les entêtes.
    - On ne peut supprimer le lien web de la recette ou la première épicerie d'un Profil.
    *Supprimer recette dans épicerie = supprimer tout ses ingrs associés.


    RETOURNE: list_infos_mod


    @mod_lst_infos

    """
    #1.OPTION LISTE D'ÉPICERIE.
    if type_lst == "la liste d'épicerie":
        #1.0.VÉRIFIER si l'index est dans la liste.
        if entr_mod_splt[1] >= len(lst_infos_mod[0]):
            #1.0.1.ERREUR, retourner la même liste.
            return lst_infos_mod


        #1.1.SINON, TROUVER les indices des entêtes.
        indx_entts = [lst_infos_mod[0].find(entt) for entt in lst_infos_mod[1]]
        #1.2.SI ENTÊTES, il y a erreur, retourner la même liste.
        if (entr_mod_splt[1] in indx_entts or
            indx_entts[1]<entr_mod_splt[1]<indx_entts[2]
            ):
            return lst_infos_mod


        #TODO 1.3.SI on supprime une recette, on offre d'enlever tous ces ingrédients.
        if entr_mod_splt < indx_entts[1]:
            pass


        #1.3.SUPPRIMER l'information à l'indice choisie.
        lst_infos_mod[0].pop(entr_mod_splt[1])
        return lst_infos_mod


    #TODO valider Profil par défaut après le finaliser.
    #2.OPTION RECETTE ou PROFIL PAR DÉFAUT.
    if 2 < entr_mod_splt[1] < len(lst_infos_mod):
        #VALIDE, pas supprimer d'entête, de lw pour une rctt et la 1ere epcr.
        lst_infos_mod.pop(entr_mod_splt[1])
    
    return lst_infos_mod




def mli_help():
    """Fonction d'affichage d'aide pour la fonction mod_lst_infos


    RETOURNE: None


    @mod_lst_infos
    """
    print("\n\n\*À noter, il y a certaines exceptions selon le type de\
liste d'information que vous désirez modifier (recette, liste d'épicerie ou profil \
par défaut. Ces exceptions sont notées plus bas*\n\n\
 - Pour la modification d'information, le format est 'chiffre', \
'.' et 'nouvelle information';\n\n\
**(Pour ajouter une informartion, insérez un chiffre plus grand que le nombre \
max disponible.**\n\n\
Un exemple de format pour changer une information:\n\
3.2 Broccolis\n\n\
Ou encore:\n\
0.Toasts au ketchup\n\n\n\
 - Pour l'échange d'emplacement des informations dans la liste, inscrivez les numéros \
associés aux deux informations, en format 'chiffre', '.' puis 'chiffre' comme par exemple:\n\
3.4\n\
 - Pour 'supprimer' une information, inscrivez 's', '.', puis 'chiffre'' de l'index à enlever.n\n\n\
Autrement,\n - 'v' permet de voir la liste avec les modifications effectuées,\n\n\
 - 'c' permet de confirmer la liste actuel et de la partager ainsi.\n\n\
 - 'r' et 's' permettent de sortir de la boucle de modification d'une liste \
d'information.\n\n\n\
*Liste d'épicerie - échange possible qu'avec les ingrédients, pas de modification d'épiceries;\n\
Profil par défaut - échange possible qu'avec les épiceries, pas de modification des entêtes;\n\
Recette - échange avec les indexs 0 et 1 impossible car sont les titres et le lien web, \
on ne supprime pas les entêtes.\n\n")

    return None




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
    df_rctts = pd.merge(
        df_rctts, df_nouv_infos, how='outer', left_index=True,
        right_index=True
    ).sort_index(axis=1)

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




#TODO créer une fonction qui dicte un nom de profil acceptable (sans espace ou char spéciaux?)
#%% Profil par défaut
def chx_prfl_dft():
    """Aider l'utilisateur à choisir un profil par défaut.


    RETOURNE: 's', 'g' ou 'nm_prfl_dft'


    @gere_si_prfl_exst_ou_non - iuf
    @affchr_epcr_et_chcks - iuf - Ingrédients épicerie

    """
    #1.1.OBTENIR le df des profils par défaut.
    df_prfls_dft = e_l.df_prfls_dft_csv()


    #.2.AFFICHER le profil actuel et les profils par défauts.
    print(f"\nVoici les informations stockés sur les profils par défaut:\n\n\
{df_prfls_dft}")


    #3.DEMANDER changer de profil ou garder le même.
    txt_inpt = "Désirez-vous changer de profil par défaut (inscrire le nom exact) \
ou (g)arder l'actuel profil d'utilisateur?\n\
( nom_de_profil_par_défaut / g ) : "
    #3.1.OBTENIR les profils par défaut dispoinibles.
    lst_nm_prfls_dft = [prfl for prfl in df_prfls_dft]
    #3.2.FORCER l'entrée 
    nm_prfl_dft= utl.boucle_frc_entr_lwrcs(txt_inpt, lst_nm_prfls_dft + ['g', 's'])


    #4.GÉRER réponse mod ou non le profil par défaut.
    #4.0.
    if nm_prfl_dft in ['s', 'g']:
        return nm_prfl_dft


    #4.1.ELSE, modifier le profil par défaut utiliser.
    print(f'\n..Le profil par défaut est maintenant le profil : {nm_prfl_dft}\n')
    
    #4.2.
    return nm_prfl_dft




def mod_archv_prfls_dft_csv(lst_info_mod_prfl_dft):
    """Modifier l'archive des profils par défaut selon les modifications reçues.
    - lst_info_mod_prfl_dft = [nom_clnn_dft, info1, info2, etc.]


    RETOURNE: None


    @chx_prfl_dft

    """
    #0.TROUVER le nom de la colonne de la liste utilisée.
    nm_clnn_prfl_dft = lst_info_mod_prfl_dft[0]

    #1.OBTENIR le df des profils par défaut.
    df_prfls_dft = e_l.df_prfls_dft_csv()


    #2.TRANSFORMER la liste obtenue en df.
    df_info_mod_prfl = pd.Dataframe(
        {nm_clnn_prfl_dft: lst_info_mod_prfl_dft[1:]}
        )

    #3.1.OPTION MODIFICATION D'UN PROFIL.
    if nm_clnn_prfl_dft in df_prfls_dft:
        #3.1.1.ENLEVER la colonne modifié pour ajouter la nouvelle par la suite.
        df_prfls_dft = df_prfls_dft.drop(columns=nm_clnn_prfl_dft)

    #3.2.OPTION NOUVEAU PROFIL par défaut (car nm_clmnn not in df).
    else:
        #2.3.1.CRÉER nouveau fichier 'ordre ingrédients par défaut'.
        creer_nouv_ordr_triage_csv(lst_info_mod_prfl_dft)


    #4.JOINDRE ET ORDONNÉE les profils par défaut.
    df_prfls_dft_mod = pd.merge(
        df_prfls_dft, df_info_mod_prfl, how='outer', left_index=True,
        right_index=True
    ).sort_index(axis=1)


    #5.ENVOYER les modifications au .csv des profils par défaut.
    envyr_mod_prfls_dft_csv(df_prfls_dft_mod)


    #6.AFFICHIER le succès.
    print(f"Les profils par défaut sont mis-à-jour avec succès!!\nVoici les nouvelles \
informations enregistrées:\n\n{df_prfls_dft_mod}")


    return None




def envyr_mod_prfls_dft_csv(df_infos_mod_prfls_dft):
    """Envoyer la modification du profil par défaut au fichier .csv entreposer à
    cet effet.


    RETOURNE: None


    @mod_archv_prfls_dft_csv

    """
    #1.OBTENIR le chemin d'accès du .csv des profils par défaut.
    prfls_dft_pth = f'{utl.chmn_accs_dir_prfls_dft()}\Profils_par_defaut.csv'

    #2.ENVOYER les modifications au .csv des profils par défaut.
    df_infos_mod_prfls_dft.to_csv(prfls_dft_pth, sep=';', encoding='latin', index=False)

    return None



#TODO quand on trie automatique, on a la liste d'épicerie avec les ingrédients connus/triés
#à côté, on a la liste d'ingrédient non trié avec ses propres index. on pourrait intégrer dans mod_lst_info j'crois.
#avec un ttp de travail =P Je t'aime.
#%% Ordre des ingrédients
#TODO
def creer_nouv_ordr_triage_csv(lst_info_prfl_dft):
    """Créer un nouveau fichier pour entreposer l'ordre de triage des ingrédients
    dans une liste d'épicerie par défaut.
    - lst_info_prfl_dft = [nm_prfl_df, epcr1, epcr2, etc]


    RETOURNE: None


    @mod_archv_prfls_dft_csv

    """
    #1.OBTENIR le chemin d'accès du dossier des profils par défaut
    nouv_prfl_dft_pth = f'{utl.chmn_accs_dir_prfls_dft()}\{lst_info_prfl_dft[0]}\
_ordr_tri_epcrs.csv'

    #2.OBTENIR listes d'ordre déjà construites pour ces épiceries, si disponible.
    #2.0.OBTENIR dictionnaire des profils par défauts.
    dct_pfls_dft = e_l.dct_infos_prfls_dft_csv()

    #TODO VÉRIFIER si ça c vraiment le meilleur move
    #2.1.REGROUPER les profils ayant déjà ces listes.
    dct_pfls_poss = {}
    for epcr in lst_info_prfl_dft:
        for prfl in dct_pfls_dft:
            if epcr in dct_pfls_dft[prfl]:
                dct_pfls_poss[epcr] = dct_pfls_poss.get(epcr, []) + [prfl] 

    #TODO. 2.2.UTILISER ces ordres créées.
    dct_epcr_ordrs = {}
    #TODO read_csv_ordre
    

    #3.1.CRÉER df des entêtes par défaut de ce profil.
    df_entts_tri_dft = pd.DataFrame()
    for epcr in lst_info_prfl_dft[1:]:
        df_entts_tri_dft[epcr] = []







