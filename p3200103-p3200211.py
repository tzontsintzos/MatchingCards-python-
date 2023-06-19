import random 
import time

class Game():

    def create_list(self,d):
        ''' 
        Στη συναρτηση αυτη κατασκευαζουμε τα δεδομενα των τραπουλοχαρτων( αριθμοι η ειδικες καρτες μεσω της λιστας ranks , συμβολα μεσω της λιστας symbols).
        d = μεταβλητη για τον αριθμο των καρτων ( το μισο των καρτων που θα υπαρχουν στο προγραμμα )
        '''
        ranks = ['A','2','3','4','5','6','7','8','9','10','J','K','Q']  # αριθμοι και ειδικες καρτες
        symbols = ['♦','♥','♣','♠'] #συμβολα καρτων
        cardsv = {} #λεξικο που περιεχει τα 52 φυλλα τα οποια εχουν ως key το ονομα του φυλλου(πχ Α♠) και ως value την αξια του(1-10) πχ 1
        cards=[]    #λιστα που περιεχει τα 52 φυλλα
        play=[]     #λιστα με τις καρτες που θα υπαρχουν στον πινακα του παιχνιδιου
        play2=[]    #λιστα με 'χ' 
        teams_list=[1,2,3,4]  # γραμμες του πινακα που θα θελουμε να εμφανισουμε

        value = 1 
        for rank in ranks:
            for symbol in symbols:
                if rank in ('J','K','Q'):
                    value=10
                cardsv.update({rank + symbol:str(value)})  #κατασκευη λεξικου
                cards.append(rank + symbol)
            value = value + 1

        cards2=cards[:]
        random.shuffle(cards2)  #ανακατευουμε τις καρτες της λιστας cards2
        random.shuffle(cards)   #ανακατευουμε τις καρτες της λιστας cards
        
        a=0                 # δημιουργια λιστας με ζευγαρια αριθμων
        for i in cards:     
            for j in cards2:
                if cardsv[i] == cardsv[j] and i!=j and i[0]==j[0] and i not in play and j not in play and a<d:
                    play.append(i)
                    play.append(j)
                    play2.append('X') 
                    play2.append('X') 
                    a+=1
                
        random.shuffle(play)    #ανακατεμα φυλλων
              
        return play, play2, cardsv

    def player_in(self,x1):
        if self.player>int(self.arithmos_paiktwn):
            self.player=1
        s='ΠΑΙΚΤΗΣ '+str(self.player)   #ονομα παικτη 
        if self.flag==0:
            mes = s + ' ({}) Δώσε γραμμή και στήλη της πρώτης κάρτας: '.format(self.paiktes[s])     #τυπωνει καθε φορα το μηνυμα και τον παικτη που θα παιξει 
        else:mes = s + ' ({}) Δώστε γραμμή και στήλη της δεύτερης κάρτας: '.format(self.paiktes[s])
        try:        # αν κατι παει στραβα μεταφερει στο except
            y,x=input(mes).split(' ')
            y=int(y)    #γραμμη
            x=int(x)    #στηλη
            if x>x1 or y>4:
                print('Άκυρη Θέση')
                self.player+=-1
            else:
                self.card_control(x,y,x1,s)
            
        except: # αν δοθουν μη εγκυρα δεδομενα
            print('Κάτι πήγε λάθος!!\n')
            self.player+=-1
        
    def start(self):
        '''
        Η συναρτηση ζητα απο το χρηστη τα δεδομενα δυσκολια και αριθμο παικτων τυπωνοντας σχετικα μηνυματα , κανοντας παραλληλα ελεγχο εγκυροτητας

        '''
        arithmos_paiktwn = input('Δωστε αριθμο παικτων : ')
        if int(arithmos_paiktwn) <2 :   #ελεγχος εγκυροτητας 
            print('\nΠρεπει να συμμετεχουν 2 τουλαχιστον παικτες.\n')
            input('Δωστε αριθμο παιχτων : ')
            
        print('\nΥπαρχουν 3 βαθμοι δυσκολιας.\n ')    
        difficulty = int(input('Επιλεξε βαθμο δυσκολιας : ')) 

        if difficulty not in (1,2,3):   # ελεγχος εγκυροτητας
            print('\nΥπαρχουν 3 βαθμοι δυσκολιας.\n ')    
            difficulty = input('Επιλεξε βαθμο δυσκολιας : ')
        
        return difficulty, arithmos_paiktwn

    def card_control(self,x,y,x1,s):
        '''
        Η συναρτηση δεχεται ως ορισματα τις συντεταγμενες της καρτας που εδωσε ο χρηστης και τον παικτη που παιζει 
        Γινονται οι ελεγχοι των καρτων ανα περιπτωση 
        Τυπωνει τα αναλογα μηνυματα

        '''

        pos=x1*(y-1)+x -1       # αλγοριθμος για την ευρεση καρτας στον πινακα
        if pos in self.z:       # ελεγχος εγκυροτητας...αν η καρτα που επιλεγει ο παικτης ειναι ανοικτη(δηλαδη βρισκεται στη λιστα z ) του ζητα να ξαναδωσει τιμη
            print('Η κάρτα είναι ήδη ανοικτή, δοκιμάστε ξανά')
            self.player+=-1
            pass
        else:
            self.z.append(pos)

            if self.play[self.z[-1]][0]=='Q' and self.prev_card=='K' or self.play[self.z[-1]][0]=='K' and self.prev_card=='Q': # περιπτωση που δοθει νταμα και ρηγας
                self.play2[self.z[-1]]=self.play[self.z[-1]]
                self.special_card_control(s,x1)
            else:

                if self.prev_card!='' and self.prev_card==self.play[self.z[-1]][0]:     #αν τα φυλλα που ανοιχτηκαν ειναι ισα
                    self.paiktes[s]=self.paiktes.get(s,0)+int(self.cardsv[self.play[self.z[-1]]])
                    print('Επιτυχές ταίριασμα +{} πόντοι! {} έχεις συνολικά {} πόντους.'.format(self.cardsv[self.play[self.z[-1]]],s,self.paiktes[s]))
                    self.epitix=1
                    if self.play[self.z[-1]][0]=='J':   #περιπτωση που ανοιχτηκαν 2 βαλεδες 
                        self.player+=-1
                    if self.play[self.z[-1]][0]=='K':   #περιπτωση που ανοιχτηκαν 2 ρηγαδες
                        self.player+=1
                    

                if self.prev_card!='' and self.prev_card!=self.play[self.z[-1]][0]: 
                    self.hide=1
                self.prev_card=self.play[self.z[-1]][0]
                self.play2[self.z[-1]]=self.play[self.z[-1]]

            if self.flag==0:
                self.flag=1
                self.player+=-1
            else:self.flag=0

    def special_card_control(self,s,x1):    # για περιπτωση που δοθει νταμα και ρηγας
        if x1==4: #πληθος στηλων
            w=self.print_tables.print_table1    
        if x1==10:
            w=self.print_tables.print_table2    #ελεγχος επιπεδου δυσκολιας
        if x1==13:
            w=self.print_tables.print_table3
        w(self.play2)
        mes = s + ' ({}) Δώσε γραμμή και στήλη της τρίτης κάρτας: '.format(self.paiktes[s])
        try:
            y,x=input(mes).split(' ')   
            y=int(y)    #γραμμες
            x=int(x)    #στηλες 
            if x>x1 or y>4:
                print('Άκυρη Θέση')
                self.special_card_control(s,x1)
            else:
                pos=x1*(y-1)+x -1
                if pos in self.z:
                    print('Η κάρτα είναι ήδη ανοικτή, δοκιμάστε ξανά')
                    self.special_card_control(s,x1)
                    
                else:
                    self.z.append(pos)
                    if self.play[self.z[-1]][0] in ('K','Q'):
                        self.play2[self.z[-1]]=self.play[self.z[-1]]
                        self.paiktes[s]=self.paiktes.get(s,0)+int(self.cardsv[self.play[self.z[-1]]])
                        print('Επιτυχές ταίριασμα +{} πόντοι! {} έχεις συνολικά {} πόντους.'.format(self.cardsv[self.play[self.z[-1]]],s,self.paiktes[s]))
                        if self.play2[self.z[-1]][0]==self.play2[self.z[-2]][0]:
                            self.play2[self.z[-3]]='X'
                            self.z.pop(-3)
                        else:
                            self.play2[self.z[-2]]='X'
                            self.z.pop(-2)
                        self.prev_card=''
                    else:
                        self.play2[self.z[-1]]=self.play[self.z[-1]]
                        w(self.play2)
                        print('Λάθος συνδυασμός!!!')
                        self.play2[self.z[-1]]='X'
                        self.play2[self.z[-2]]='X'
                        self.play2[self.z[-3]]='X'
                        self.z.pop(-1)
                        self.z.pop(-1)
                        self.z.pop(-1)
                        self.prev_card=''
        except:
            print('Κάτι πήγε λάθος!!\n')


    def __init__(self):   # κατασκευαστης της ταξης      
        max1=0
        self.epitix=0   # flag που δειχνει αν ο χρηστης εχει επιτυχια η οχι
        self.z=[]       # λιστα που περιεχει την θεση των ανοιγμενων καρτων
        self.hide=0     # μεταβλητη που δειχνει αν ο συνδυασμος που επιλεχτηκε ειναι σωστος(0) η λαθος(1)
        self.player=1   # μεταβλητη που δειχνει ποιος παικτης παιζει
        self.paiktes={} # λεξικο που περιεχει τα ονοματα των παικτων και το σκορ του καθενος
        self.flag=0     # δειχνει αν η καρτα που ανοιγει ο παικτης ειναι η 1η ή η 2η 
        self.prev_card=''     #μεταβλητη που περιεχει την προηγουμενη καρτα που ανοιχτηκε
        print('ΚΑΛΩΣΗΡΘΑΤΕ ΣΤΟ MATCHING GAME!\n')
        self.difficulty, self.arithmos_paiktwn = self.start()   # καλουμε την συναρτηση start και αποθηκευουμε στις difficulty και arithmos_paiktwn τα δεδομενα που δινει ο χρηστης 

        for i in range(int(self.arithmos_paiktwn)):
            s='ΠΑΙΚΤΗΣ '+str(i+1)
            self.paiktes.update({s:0})  #δημιουργει λεξικο με τους παικτες με αρχικους ποντους 0

        if self.difficulty==1:      
            self.play,self.play2,self.cardsv=self.create_list(8)
            self.print_tables.print_table1(self.play)
            time.sleep(4)   #χρονος αναμονης μεχρι να κρυφτουν τα φυλλα του πινακα
            for _i in range(10):
                print('\n')
            while len(self.z)<16:
                self.print_tables.print_table1(self.play2)      #τα εμφανιζει ολα ως 'χ'
                if self.hide==1:        #αν ο συνδυασμος ειναι λαθος 
                    self.play2[self.z[-1]]='X'  
                    self.play2[self.z[-2]]='X'
                    print('Λάθος συνδυασμός!!!')
                    self.print_tables.print_table1(self.play2)
                    self.hide=0
                    self.prev_card=''
                    self.z.pop(-1)
                    self.z.pop(-1)
                self.player_in(4)
                if self.epitix==1:
                    self.prev_card=''
                    self.epitix=0
                self.player+=1
            else:
                self.print_tables.print_table1(self.play2)
                for i in self.paiktes.keys():
                    if int(self.paiktes[i])>max1:
                        max1=int(self.paiktes[i])
                        max=i
                print('Συγχαρητήρια {} κέρδισες με {} πόντους!'.format(max,self.paiktes[max]))

                


        if self.difficulty==2:
            self.play,self.play2,self.cardsv=self.create_list(20)
            self.print_tables.print_table2(self.play)
            time.sleep(6)    #χρονος αναμονης μεχρι να κρυφτουν τα φυλλα του πινακα
            for _i in range(10):
                print('\n')
            while len(self.z)<40:
                self.print_tables.print_table2(self.play2)  #τα εμφανιζει ολα ως 'χ'
                if self.hide==1:         #αν ο συνδυασμος ειναι λαθος 
                    self.play2[self.z[-1]]='X'
                    self.play2[self.z[-2]]='X'
                    print('Λάθος συνδυασμός!!!')
                    self.print_tables.print_table2(self.play2)
                    self.hide=0
                    self.prev_card=''
                    self.z.pop(-1)
                    self.z.pop(-1)
                self.player_in(10)
                if self.epitix==1:
                    self.prev_card=''
                    self.epitix=0
                self.player+=1
            else:
                self.print_tables.print_table2(self.play2)
                for i in self.paiktes.keys():
                    if int(self.paiktes[i])>max1:
                        max1=int(self.paiktes[i])
                        max=i
                print('Συγχαρητήρια {} κέρδισες με {} πόντους!'.format(max,self.paiktes[max]))

        if self.difficulty==3:
            self.play,self.play2,self.cardsv=self.create_list(26)
            self.print_tables.print_table3(self.play)
            time.sleep(8)    #χρονος αναμονης μεχρι να κρυφτουν τα φυλλα του πινακα
            for _i in range(10):
                print('\n')
            while len(self.z)<52:
                self.print_tables.print_table3(self.play2)  #τα εμφανιζει ολα ως 'χ'
                if self.hide==1:         #αν ο συνδυασμος ειναι λαθος 
                    self.play2[self.z[-1]]='X'
                    self.play2[self.z[-2]]='X'
                    print('Λάθος συνδυασμός!!!')
                    self.print_tables.print_table3(self.play2)
                    self.hide=0
                    self.prev_card=''
                    self.z.pop(-1)
                    self.z.pop(-1)
                self.player_in(13)
                if self.epitix==1:
                    self.prev_card=''
                    self.epitix=0
                self.player+=1
            else:
                self.print_tables.print_table3(self.play2)
                for i in self.paiktes.keys():
                    if int(self.paiktes[i])>max1:
                        max1=int(self.paiktes[i])
                        max=i
                print('Συγχαρητήρια {} κέρδισες με {} πόντους!'.format(max,self.paiktes[max]))

    class print_tables():
        '''
        ταξη που περιεχει τις συναρτησεις των πινακων που θα εμφανιστουν στο παιχνιδι
        οι πινακες 1 2 3 θα χρησιμοποιουνται αναλογα με το επιπεδο για το παιχνιδι
        
        '''

        def print_table1(list):     #εκτυπωση πινακα επιπεδου 1
            play2=list
            i=1
            print ("{:<10} {:<10} {:<10} {:<10} {:<10}\n".format("",'1','2','3','4'))
            for v in range(0,len(play2),4):
                a, b, c, d = play2[v],play2[v+1],play2[v+2],play2[v+3]
                print ("{:<10} {:<10} {:<10} {:<10} {:<10}\n".format(i, a, b, c, d))
                i+=1



        def print_table2(list):      #εκτυπωση πινακα επιπεδου 2
            play2=list
            i=1
            print ("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}\n".format("",'1','2','3','4','5','6','7','8','9','10'))
            for v in range(0,len(play2),10):
                a, b, c, d, e, f, g, h, k, j = play2[v],play2[v+1],play2[v+2],play2[v+3],play2[v+4],play2[v+5],play2[v+6],play2[v+7],play2[v+8],play2[v+9]
                print ("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}\n".format(i, a, b, c, d, e, f, g, h, k, j))
                i+=1


        def print_table3(list):      #εκτυπωση πινακα επιπεδου 3
            play2=list
            i=1
            print ("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}\n".format("",'1','2','3','4','5','6','7','8','9','10','11','12','13'))
            for v in range(0,len(play2),13):
                a, b, c, d, e, f, g, h, k, j, g, v, n = play2[v],play2[v+1],play2[v+2],play2[v+3],play2[v+4],play2[v+5],play2[v+6],play2[v+7],play2[v+8],play2[v+9],play2[v+10],play2[v+11],play2[v+12]
                print ("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}\n".format(i, a, b, c, d, e, f, g, h, k, j, g, v, n))
                i+=1


if __name__ == "__main__":      #εναρξη προγραμματος
    Game()
    
