from pickle import*
from time import*
from copy import*
#preparation turtle
from turtle import*
speed(0)
hideturtle()
paper=Screen()
def main():                         #fonction pour créer la fenetre 
    setup (1200, 800, 0, 0)
    title ('Towers Of Hanoi')
main() 
#deuxieme turtle pour dessiner le score
score=Turtle()                  
score.ht()
score.speed(0)

#Variables Globales
coup={}
origin_tower=[]
spare_tower=[]
target_tower=[]
plateau=[origin_tower,spare_tower,target_tower] 
TowerOneSelected=False
TowerTwoSelected=False
TowerOrigin = -1
TowerTarget = -1
compteurMouvements=0
listeCouleurs=["","blue","red","green","purple","brown","white","pink","orange","blue","red","green","brown","white","pink","orange","purple"]
listeMouvements=[]
lignes = []

#Distances
nombreDisques=int(paper.numinput("Nombre de Disques","saisir la quantité des disques"))   #nombre des disques
nombreTowers=3
diametreDisqueMax=40+30*nombreDisques
epaisseurDisques=30
hauteurTour=(epaisseurDisques*nombreDisques)+20 
espaceEntreTours=diametreDisqueMax+20
longueurPlateau=4*espaceEntreTours

#parie a
def init(n):        #Partie A, 1
    origin_tower=[]
    spare_tower=[]
    target_tower=[]
    plateau=[origin_tower,spare_tower,target_tower]
    nombre_disques=n
    if n<0:
        return -1
    while 0<n:
        origin_tower.append(n)               #Ajouter tous les disques dans la liste
        n-=1
    plateauCopy=deepcopy(plateau)
    coup[compteurMouvements]=plateauCopy         #Ajouter configuration dans le dictionnaire
    return plateau

def nombre_disques(numtower):                #Partie A, 2
    if 0<=numtower<=2:
        return len(plateau[numtower])
    else:
        return -1

def disque_superieur(numtower):             #Partie A, 3, disque superieur dans une tour
    if 0<=numtower<=2:
        listetower=plateau[numtower]
        if len(plateau[numtower])==0:
            return -1
        else:
            return listetower[-1]
    else:
        return -1
    
def position_disque(nd):        #Partie A, 4, touver dans quel tour se trouve le disque
    positiondisque=-1
    i=0
    while positiondisque==-1 and i<3:
        if nd in plateau[i]:
            positiondisque=i
        i+=1
    return positiondisque

def position_disque_in_list(nd):                 #touver ou se trouve le disque dans une tour selectionne
    listetower=plateau[position_disque(nd)]
    positionDisque=listetower.index(nd)
    return positionDisque

def verifier_deplacement(nt1, nt2):         #verifier si le mouvement est autorisé
    if disque_superieur(nt1)<disque_superieur(nt2) or len(plateau[nt2])==0:
        return True
    else:
        return False

def verifier_victoire(nombreDisques):
    return len(plateau[2])==nombreDisques 

#partie b

def allez_au(x,y):                              #fonction pour reduir un code de 3 lignes en 1 ligne
    up()
    goto(x,y)
    down()
    
def dessine_score():                            #fonction pour dessiner le score
    score.up()
    score.goto(-longueurPlateau/2,-300)
    score.down()
    score.pencolor("black")
    score.write("SCORE",font="Impact")
    score.pencolor("white")
    score.fillcolor("white")
    score.begin_fill()
    score.up()
    score.goto(-longueurPlateau/2+70,-300)
    score.down()
    for i in range(4):
        score.forward(20)
        score.left(90)
    score.end_fill()
    score.up()
    score.goto(-longueurPlateau/2+72,-300)
    score.down()
    score.pencolor("black")
    score.write(compteurMouvements,font="Impact")
    
def dessine_exit_button():                       #fonction pour dessiner le bouton pour sortir
    width(3)
    allez_au((-longueurPlateau/2), hauteurTour+30)
    pencolor("black")
    fillcolor("red")
    begin_fill()
    for i in range(2):
        forward(83)
        left(90)
        forward(60)
        left(90)
    end_fill()
    width(1)
    allez_au((-longueurPlateau/2)+3, hauteurTour+30)
    write("EXIT",font=("Impact",35))
    
def dessine_return_button():                    #fonction pour dessiner le bouton de retour
    width(3)
    allez_au((longueurPlateau/2)-110, hauteurTour+30)
    pencolor("black")
    fillcolor("blue")
    begin_fill()
    for i in range(2):
        forward(113)
        left(90)
        forward(50)
        left(90)
    allez_au(((longueurPlateau/2)-110)+3, hauteurTour+30)
    width(1)
    end_fill()
    write("Return", font=("Impact",30))

def dessine_timer():
    a=0
    listeSecondes=[]
    while a<nombreDisques*10000:
        listeSecondes.append(a)
        sleep(1)
        a+=1
        
def dessine_automatic_button():             #dessiner le automatic button
    allez_au(longueurPlateau/2-115,-300)
    write("Automatic",font=("Impact",20))
    
def glow(numTower):                          #remarquer le disque selectionné
    disque=disque_superieur(numTower)
    dessine_disque(disque, nombreDisques, "yellow")
    
def dessine_plateau(nombreDisques):    #dessiner le plateau
    x=-(longueurPlateau/2)
    allez_au(x,-200)
    fillcolor("black")
    begin_fill()
    for i in range(2):
        forward(longueurPlateau)
        right(90)
        forward(20)
        right(90)
    for i in range(3):
        forward(espaceEntreTours+4)
        left(90)
        forward(hauteurTour)
        left(90)
        forward(8)
        left(90)
        forward(hauteurTour)
        left(90)
        up()
        forward(4)
        down()
    end_fill()
    dessine_exit_button()
    dessine_return_button()
    dessine_score()
    dessine_automatic_button()
    
def dessine_disque(nd, nombreDisques, color):    #dessiner 1 disque
    pencolor(color)
    numtour=position_disque(nd)
    positionDisque=position_disque_in_list(nd)
    x=0
    y=0
    #Coordonées x
    if numtour==0:
        x=(-longueurPlateau/4)
    elif numtour==1:
        x=0
    elif numtour==2:
        x=(longueurPlateau/4)
    #coordonées y
    y=-200+(epaisseurDisques*positionDisque)
    allez_au(x,y)
    fillcolor(listeCouleurs[nd])
    begin_fill()
    for i in range(2):
        if i==0:
            pencolor("black")
            forward((40+(30*nd))/2)
        elif i==1:
            pencolor(color)
            forward(40+(30*nd))
        pencolor(color)
        left(90)
        forward(epaisseurDisques)
        left(90)
    pencolor("black")
    forward((40+(30*nd))/2)
    end_fill()
    
def efface_disque(nd, nombreDisques):           #efface disque
    pencolor("white")
    numtour=position_disque(nd)
    positionDisque=position_disque_in_list(nd)
    x=0
    y=0
    #Coordonées x
    if numtour==0:
        x=(-longueurPlateau/4)
    elif numtour==1:
        x=0
    elif numtour==2:
        x=(longueurPlateau/4)
    #coordonées y
    y=-200+(epaisseurDisques*positionDisque)
    allez_au(x,y)
    fillcolor("white")
    begin_fill()
    for i in range(2):
        if i==0:
            up()
            forward((40+(30*nd))/2)
            down()
            left(90)
            forward(epaisseurDisques)
            left(90)
        if i==1:
            forward(40+(30*nd))
            left(90)
            forward(epaisseurDisques)
            left(90)
            up()
            forward((40+(30*nd))/2)
            down()
    end_fill()
    #redessiner la tour effacée
    pencolor("black")
    fillcolor("black")
    begin_fill()
    backward(4)
    for i in range(2):
        forward(8)
        left(90)
        forward(epaisseurDisques)
        left(90)
    forward(4)
    end_fill()
    
def dessine_config(nombreDisques):                      #dessiner une config
    for i in range(nombreDisques):
        dessine_disque(nombreDisques-i, nombreDisques,"black")

def efface_tout(nombreDisques):                          #effacer tous le disques
    for i in range(nombreDisques):
        efface_disque(nombreDisques-i, nombreDisques)

def jouer_un_coup(nombreDisques):                        #faire un mouvement
    global compteurMouvements
    if verifier_deplacement(TowerOrigin, TowerTarget):
        disqueSuperieur=disque_superieur(TowerOrigin)
        efface_disque(disqueSuperieur, nombreDisques)
        plateau[TowerOrigin].pop(-1)
        plateau[TowerTarget].append(disqueSuperieur)
        dessine_disque(disqueSuperieur, nombreDisques,"black")
        compteurMouvements+=1
    else :
       allez_au(-15,-300)
       pencolor("red")
       write("X",font=("Impact",50))
       sleep(0.5)
       pencolor("white")
       write("X",font=("Impact",50))
    return plateau

def jouer_un_coup_automatique(nombreDisques, nt1, nt2):     #faire un mouvement lors du jeu automatique
    global compteurMouvements
    if verifier_deplacement(nt1, nt2):
        disqueSuperieur=disque_superieur(nt1)
        efface_disque(disqueSuperieur, nombreDisques)
        plateau[nt1].pop(-1)
        plateau[nt2].append(disqueSuperieur)
        dessine_disque(disqueSuperieur, nombreDisques,"black")
        compteurMouvements+=1
    else :
       allez_au(-15,-300)
       pencolor("red")
       write("X",font=("Impact",50))
       sleep(0.5)
       pencolor("white")
       write("X",font=("Impact",50))
    return plateau

def boucle_jeu(x,y):                                         #fonction du boucle jeu qui est appele a chaque click
    global TowerOneSelected, TowerTwoSelected, TowerOrigin, TowerTarget, compteurMouvements
    TowerInAction = get_numTower_fromCords(x, y)
    if TowerOneSelected == True and 0<=TowerInAction<=nombreTowers: #si la premiere tower est pas selectionne
        if TowerInAction==TowerOrigin:                            #si les tours selectionnés sont les memes  
            TowerOneSelected = False
            TowerTwoSelected = False
            TowerOrigin= -1
            TowerTarget =-1
        elif TowerInAction!=TowerOrigin :                       #si les tours selectionnés sont differentes
            TowerTwoSelected=True
            TowerTarget = TowerInAction
            plateau=jouer_un_coup(nombreDisques)
            dessine_score()
            plateauCopy=deepcopy(plateau)
            coup[compteurMouvements]=plateauCopy
            TowerOneSelected = TowerTwoSelected =False
            TowerTarget=TowerOrigin=-1
            if verifier_victoire(nombreDisques):
                clear()
                allez_au(-150,0)
                pencolor("green")
                write("Victoire",font=("Impact",60))
                nomJoueur=str(paper.textinput("NOM", "Écrivez votre nom pour enregistrer le score"))
                enregistre_score(nomJoueur, nombreDisques, compteurMouvements)
                sleep(3)
                bye()
                      
    elif 0<=TowerInAction<=nombreTowers:
        if TowerOneSelected == False:                       #si la premiere tower nest pas selectionne
            TowerOneSelected=True
            TowerOrigin = TowerInAction
            glow(TowerInAction)
    elif TowerInAction==5:
        automatic_game()
        bye()
    elif TowerInAction==6:
        plateau=annuler_dernier_coup()
        dessine_score()
    elif TowerInAction==7:
        automatic_game()

def get_numTower_fromCords(x, y):
    nombreTower=-1
    if ((-espaceEntreTours)-diametreDisqueMax/2)<=x<=((-espaceEntreTours)+diametreDisqueMax/2) and -200<=y<=hauteurTour:
        nombreTower=0
    elif (-diametreDisqueMax/2)<=x<=(diametreDisqueMax/2) and -200<=y<=hauteurTour:
        nombreTower=1
    elif ((espaceEntreTours)-diametreDisqueMax/2)<=x<=((espaceEntreTours)+diametreDisqueMax/2) and -200<y<hauteurTour:
        nombreTower=2
    elif ((-longueurPlateau/2)-15)<x<((-longueurPlateau/2)+150) and ((hauteurTour+30))<y<((hauteurTour+30)+50):
        nombreTower=5                                           #Valeur pour sortir du jeu
    elif ((longueurPlateau/2)-110)<x<((longueurPlateau/2)) and ((hauteurTour+30))<y<((hauteurTour+30)+50):
        nombreTower=6                                                               #Valeur revenir en arriere
    elif (longueurPlateau/2-1153)<x<(longueurPlateau/2) and -300<y<-200:            
        nombreTower=7                                                               #valeur jeu automatique
    return nombreTower

def reset_everything():
    TowerOneSelected = False
    TowerTwoSelected = False
    TowerOrigin= -1
    TowerTarget =-1

def dernier_coup():                 #recuperer le dernier coup
    global plateau, coup, compteurMouvements
    if compteurMouvements>0:
        plateau=coup.get(compteurMouvements-1)
        del coup[compteurMouvements]
        compteurMouvements-=1
    return plateau

def annuler_dernier_coup():         #undo le dernier mouvement
    global plateau, coup, compteurMouvements
    efface_tout(nombreDisques)
    plateau=dernier_coup()
    dessine_config(nombreDisques)
    return plateau

def enregistre_score(nomJoueur, nombreDisques, nombreCoups):                                #sauvegarder score
    partie={"nom joueur":nomJoueur,"nombre de disques": nombreDisques,"Score":nombreCoups}
    with open("scores","ab") as f:
        dump(partie, f)
    f.close()
    
def recupere_scores():                      #recuperer les scores du file pickle
    with open("scores","rb") as f:
        while True:
            try:
                lignes.append(load(f))
            except EOFError:
                break
    return lignes

def affiche_scores():                       #imprimer le meilleur score
    lignes=recupere_scores()
    minVal=(2^nombreDisques+1)+1000
    partieBest=None
    for i in range (len(lignes)):
        partie=lignes[i]
        Score=partie.get('Score')
        if partie.get('nombre de disques')==nombreDisques:
            if Score<minVal:
                minVal=Score
                partieBest=lignes[i]
    allez_au(longueurPlateau/2-70,-350)
    text=str(partieBest["Score"])+" "+partieBest["nom joueur"]
    write(text,font=("Impact",15))
    
def moveTower(nombreDisques, origin, target, spare):            #algorithme towers of hanoi
    if nombreDisques >= 1:
        moveTower(nombreDisques-1, origin, spare, target)
        listeMouvements.append(moveDisk(origin, target))
        moveTower(nombreDisques-1, spare, target, origin)
    return listeMouvements

def moveDisk(fp,tp):                                            #fct pour sauvegarder la tour d'origen et but
    print("moving disk from",fp,"to",tp)
    if fp=="origin":
        fp=0
    elif fp=="spare":
        fp=1
    elif fp=="target":
        fp=2
    if tp=="origin":
        tp=0
    elif tp=="spare":
        tp=1
    elif tp=="target":
        tp=2
    return fp, tp

def automatic_game():                                                   #fct du jeu automatique
    listeMouvements=moveTower(nombreDisques, "origin", "target", "spare")
    i=0
    while not(verifier_victoire(nombreDisques)):
        nt1=listeMouvements[i][0]
        nt2=listeMouvements[i][1]
        plateau=jouer_un_coup_automatique(nombreDisques, nt1, nt2)
        i+=1
    return plateau  

#programme principal

plateau=init(nombreDisques)
dessine_plateau(nombreDisques)
dessine_config(nombreDisques)
affiche_scores()
onscreenclick(boucle_jeu)
mainloop() 


