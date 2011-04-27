

import random
#import time
import math


import class_weapon


    
def getBonus(stat):
    bonus=3*math.floor((stat-40)/10)
    return bonus

def reRoll():
    roll=random.randint(1,100)
    return roll


class Actor:
    def __init__(self, chosenName):
        self._name=chosenName
        self.brav=random.randint(1,100)
        self.conc=random.randint(1,100)
        self.grit=random.randint(1,100)
        self.hp=(30+getBonus(self.grit))
        self.losthp=0
        self.draw=False
        self.drawdebuff=0   #negative on the turn you draw
        self.movedebuff=0         #negative number 
        self.dig=0          #dig deep up to 20
        self.grapple=0      #positive 15 on the one that's grappled
        self.wound=0        #negative, based on lost/total hp
        self.concuss=0      #negative up to 15
        self.intimcount=0
        self.x=0
        self.y=0
        self.isNPC=False
        
        
    def __str__(self):
        return self.cap_name+"'s stats: "+str(self.hp)+" Health Points, \nBravery: "+str(self.brav)+"\tConcentration: "+str(self.conc)+"\tGrit: "+str(self.grit)
    
    def get_name(self):
            return self._name
    def set_name(self,name):
        self._name = name
    name = property(get_name,set_name) #use name for middle of a sentence

    def get_cap_name(self):
        if self._name.find("the ")==0: #if the name starts with "the "
            return self._name.capitalize()
        else:
            return self._name
    cap_name = property(get_cap_name) #use cap_name for the start of a sentence
    
    def addRoots(self,root):
        if root==1:
            self.brav+=10
        elif root==2:
            self.conc+=10
        elif root==3:
            self.grit+=10
        else:
            print "Error text!"
    def addWeapon(self):
        if self.isNPC:
            weaponChoice=random.randint(1,4)
        else:
            weaponChoice = 0
            print "Choose your weapon:"
            print "1. Six-shooter \tMedium range penalty\tSix bullets/ reload \tStandard damage"
            print "2. Shotgun \tHigh range penalty \tThree bullets/ reload \tIncreased damage"
            print "3. Rifle \tNo range penalty \tOne bullet/ reload \tMassive damage"
            print "4. Saber \tUsable from 0 to 2 feet\tNo reload \tIncreased damage"
            while weaponChoice < 1 or weaponChoice > 4:
                try:
                    weaponChoice=input("Which weapon will you use?")
                except SyntaxError:
                    print "Please enter your choice by number."
                except NameError:
                    print "Please enter your choice by number."
        
        if weaponChoice==1:
            self.weapon=class_weapon.Weapon(self.name,1,6,"standard",0,True)
            print self.cap_name," chooses a six-shooter."
        elif weaponChoice==2:
            self.weapon=class_weapon.Weapon(self.name,2,3,"standard",10,True)
            print self.cap_name," chooses a shotgun."
        elif weaponChoice==3:
            self.weapon=class_weapon.Weapon(self.name,0,1,"standard",30,True)
            print self.cap_name," chooses a rifle."
        elif weaponChoice==4:
            self.weapon=class_weapon.Weapon(self.name,0,10,"saber",20,False)
            print self.cap_name," chooses a saber."
      
        
        
        
    def rangeChanceCalc(self,defense):
        rangeChance=(50+getBonus(self.conc)+self.drawdebuff+self.movedebuff+self.dig+self.wound
                     +self.concuss+self.weapon.range*max(abs(self.x-defense.y),abs(self.x-defense.y))+
                     defense.movedebuff)
        return rangeChance
    def meleeChanceCalc(self,defense):
        meleeChance=50+getBonus(self.brav)+self.dig+self.wound+self.concuss+defense.grapple+defense.movedebuff
        return meleeChance
    def getLocation(self):
        locationAndDamage=[["Left Leg", 40, 70, 200, 1000], #allows for mods over 100, 4th slot has no value for lower body parts
                   ["Right Leg", 40, 70, 200, 1000],
                   ["Non-Gun Arm", 50, 90, 200, 1000],
                   ["Gun Arm", 30, 80, 200, 1000],
                   ["Left Shoulder", 40, 70, 90, 200],
                   ["Right Shoulder", 40, 70, 90, 200],
                   ["Gut",  30, 60, 80, 200],
                   ["Chest", 20, 70, 80, 200],
                   ["Head", 10, 40, 70, 100]]
        roll=reRoll()
        if roll<=15:
            location=locationAndDamage[0]
        elif roll <=30:
            location=locationAndDamage[1]
        else :
            location=locationAndDamage[(roll-20)/10]
        return location
    def getDamage(self,location): #Concussion(melee) is true, range false
        roll=reRoll()+self.weapon.sharp
        if roll <=location[1]:
            damage=2
            depth="Scratch damage "
        elif roll <=location[2]:
            damage=4
            depth="Light wound "
        elif roll <=location[3]:
            damage=8
            depth="Serious wound "
        else:
            damage=12
            depth="Massive wound "
        print "Hit!   "+ depth+"to the "+location[0]+":",
        if self.weapon.isMelee:
            damage=damage/2
            print damage,"damage and",damage,"concussion."
        else:
            print damage,"damage."
        return damage

    def shoot(self,defense):
        roll=reRoll()
        if roll<=self.rangeChanceCalc(defense):
            damage=self.getDamage(self.getLocation())
            defense.losthp+=damage
        else:
            print "Shot missed!"
    def punch(self,defense):
        roll=reRoll()
        if roll<=self.meleeChanceCalc(defense):
            damage=self.getDamage(self.getLocation())
            defense.losthp+=damage
            defense.concuss-=damage
        else:
            print "Missed!"
    def grab(self,defense):
        roll=reRoll()
        if roll<=self.meleeChanceCalc(defense):
            print "Grab succeeds! Future punches are more likely to hit."
            defense.grapple=15
        else:
            print "Grab missed!"
    def intimidate(self,defense):
        if getBonus(self.grit)+random.randint(1,10)+self.dig>getBonus(defense.grit)+random.randint(1,10):
            print "Intimidate succeeds! 3 successes will win."
            self.intimcount+=1
        else:
            print "Intimidate fails."
            self.intimcount-=1
        print "Overall intimidation score:"
        print self.cap_name,": ",self.intimcount,"\t\t",defense.cap_name,": ",defense.intimcount
    def getWounds(self):
        wounds=self.losthp/self.hp
        if wounds >=.25:
            print self.cap_name," has lost ",self.losthp," points of health and is at "
        if wounds >=.75:
            print "a massive disadvantage due to wounds."
            self.wound=-30
        elif wounds >=.50:
            print "a serious disadvantage due to wounds."
            self.wound=-20
        elif wounds>=.25:
            print "a slight disadvantage due to wounds."
            self.wound=-10
        else:
            pass
    def move(self,defense,distance):
        self.movedebuff = int(-distance *2.5) #will charge as much for a 6 move as an 8
        if distance < 1: #moving backwards
            self.x += distance if self.x < defense.x else -distance
            self.y += distance if self.y < defense.y else -distance
            return
        if abs(self.x-defense.x) <=distance: #run will bring them to the closest spot
            self.x = defense.x + (1 if self.x > defense.x else -1)
        else:
            self.x += distance if self.x < defense.x else -distance
                
        if abs(self.y-defense.y) <=distance: #run will bring them to the closest spot
            self.y = defense.y + (1 if self.y > defense.y else -1)
        else:
            self.y += distance if self.y < defense.y else -distance
        