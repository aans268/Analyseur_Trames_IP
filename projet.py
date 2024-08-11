#!/usr/bin/python3
# -- coding: utf-8 --

import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys
#ouverture fichier
if(len(sys.argv)<2):
    f = open("trames.txt", "r")
else:
    f = open(sys.argv[1], "r")
#lecture première trame
l = ''
fin_direct=False
l2=f.readline()
if(l2=="FIN"):
    fin_direct=True
l2_size=0
l2_first=True
while(l2!='' and l2!="FIN"):
    l=l2[0:len(l2)-1]
    l2=f.readline()
    if (l2_first==True and l2!='\n'):
        l2_size=int(l2[0:4],base=16)
        # print(l2_size)
        l2_first=False
        l=l[0:7+l2_size-1+l2_size*2]
    while(l2[0:4]!="0000" and l2!="FIN"):
        l+=' '+l2[7:7+l2_size-1+l2_size*2]
        l2=f.readline()
    l3=l2
    l2=''
#creation interface graphique
root = tk.Tk()
root.title("Visualiseur de trafic")

window_width = 1100
window_height = 700

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

main_frame=Frame(root)
main_frame.pack(fill=BOTH,expand=1)

canvas = tk.Canvas(root)
scrollbar=ttk.Scrollbar(main_frame,orient=VERTICAL,command=canvas.yview)
scrollbar.pack( side = RIGHT, fill = Y )
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
canvas.config(width=window_width,height=window_height,yscrollcommand = scrollbar.set)
canvas.pack()
canvas.create_text(550, 999999, text="FIN DE PAGE", fill="black", font=('Arial'))

line_dimension1_x=200
line_dimension1_y=80
line_dimension2_x=900
line_dimension2_y=80

IP_DEST=""
premier_passage_pour_de_vrai=True
premier_passage=True
cpt=0
#boucle principale tant que il reste des trames
while (l!="FIN" and fin_direct==False):
    if (premier_passage_pour_de_vrai==True):
        canvas.create_text(line_dimension1_x-140, line_dimension1_y-7, text="Frame Number", fill="black", font=('Arial'))
    cpt+=1
    ordre_classique=False
    print("\n**********************\n")
    print("NOUVELLE TRAME :",cpt)
    i=7
    print("Adresse Mac Destination :",l[i:i+17])
    mac_source=l[i:i+17]
    i+=18
    print("Adresse Mac Source :",l[i:i+17])
    # print(l)
    mac_dest=l[i:i+17]
    i+=18
    t=l[i:i+5]
    rectangle=canvas.create_rectangle(line_dimension1_x-150,line_dimension1_y+10,line_dimension2_x+150,line_dimension2_y+40,fill='orange red')
    line_dimension1_y+=30
    line_dimension2_y+=30
    if (t=="08 05"):
        print("Type : X.25 niveau 3")
    elif (t=="08 06"):
        print("Type : ARP")
    elif (t=="80 35"):
        print("Type : RARP")
    elif (t=="80 98"):
        print("Type : Appletalk")
    #condition IP
    elif (t=="08 00"):
        canvas.itemconfig(rectangle, fill='yellow3')
        print("Type : Dod Internet (Datagramme IP)")
        print()
        i+=6
        print("Version :",l[i:i+1])
        version=l[i:i+1]
        i+=1
        ihl=int(l[i:i+1],base=16)
        print("IHL :",ihl)
        i+=5
        total_length=int(l[i:i+5].replace(" ",""),base=16)
        print("Total Length :", total_length)
        i+=6
        print("Identification :",l[i:i+5])
        i+=6
        flags=int(l[i:i+1].replace(" ",""),base=16)
        F='0'
        if (flags>=4 and flags <8)or flags>=12:
            F+='1'
        else:
            F+='0'
        if (flags>=2 and flags <4)or (flags>=6 and flags <8) or (flags>=10 and flags <12) or (flags>=14 and flags <16):
            F+='1'
        else:
            F+='0'
        print("Flags :",F)
        i+=1
        if (flags%2==1):
            offset='1'+l[i:i+5].replace(" ","")
        else:
            offset='0'+l[i:i+5].replace(" ","")
        print("Fragment offset :",int(offset,base=16))
        i+=5
        print("TTL :",int(l[i:i+2],base=16))
        i+=3
        p=int(l[i:i+2],base=16)
        if(p==1):
            print("Protocol : Internet Control Message Protocol")
        if(p==2):
            print("Protocol : Internet Group Management Protocol")
        if(p==8):
            print("Protocol : Exterior Gateway Protocol")
        if(p==9):
            print("Protocol : any private Interior Gateway Protocol")
        if(p==17):
            print("Protocol : User Datagram Protocol")
        if(p==36):
            print("Protocol : XTP")
        if(p==46):
            print("Protocol : Reservation Protocol")
        if(p==6):
            print("Protocol : Transmission Control Protocol")
        i+=3
        print("Header Checksum :",bin(int(l[i:i+5].replace(" ",""),base=16)))
        i+=6
        ip_source=(str(int(l[i:i+2],base=16))+"."+str(int(l[i+3:i+5],base=16))+"."+str(int(l[i+6:i+8],base=16))+"."+str(int(l[i+9:i+11],base=16))).replace(" ","")
        if (premier_passage):
            canvas.create_text(line_dimension1_x, 75, text=ip_source, fill="black", font=('Helvetica 15 bold'))
        print("Adresse IP Source :",ip_source)
        i+=12
        ip_dest=(str(int(l[i:i+2],base=16))+"."+str(int(l[i+3:i+5],base=16))+"."+str(int(l[i+6:i+8],base=16))+"."+str(int(l[i+9:i+11],base=16))).replace(" ","")
        if (premier_passage):
            canvas.create_text(line_dimension2_x, 75, text=ip_dest, fill="black", font=('Helvetica 15 bold'))
        premier_passage=False
        print("Adresse IP Destination :",ip_dest)
        # print("ip_trame : "+ip_dest)
        # print("ip_initiale : "+IP_DEST)
        if(IP_DEST==""):
            IP_DEST=ip_dest
            ordre_classique=True
        elif(IP_DEST==ip_dest):  #si c'est bien le meme ordre que celui de la première trame
            # print("meme ordre")
            line_dimension1_x=200
            line_dimension2_x=900
            ordre_classique=True
        else:
            line_dimension1_x=900
            line_dimension2_x=200
        canvas.tag_lower(rectangle)
        canvas.create_line(line_dimension1_x, line_dimension1_y+2, line_dimension2_x, line_dimension2_y+2, arrow=tk.LAST)
        i+=12
        i2=0
        #options IP
        print("Options :")
        while(i2/2<ihl*4-20):
            if (l[i+i2:i+i2+2]=="00"):
                print(" EOOL")
                i2+=2
                i+=1
            elif (l[i+i2:i+i2+2]=="01"):
                print(" NOP")
                i2+=2
                i+=1
            else:
                Option_type=" Unknown/"
                if(l[i+i2:i+i2+2]=="07"):
                    Option_type=" RR/"
                if(int(l[i+i2:i+i2+2],base=16)==68):
                    Option_type=" TS/"
                if(int(l[i+i2:i+i2+2],base=16)==131):
                    Option_type=" LSR/"
                if(int(l[i+i2:i+i2+2],base=16)==137):
                    Option_type=" SSR/"
                i2+=2
                i+=1
                Option_taille=int(l[i+i2:i+i2+2],base=16)
                i2+=2
                i+=1
                Option_type+=str(Option_taille)+"/"+str(int(l[i+i2:i+i2+Option_taille*2-4+Option_taille-2].replace(" ",""),base=16))
                i2+=Option_taille*2-4
                i+=Option_taille-2
                print(Option_type)
        i+=i2
        #condition TCP
        if(p==6):
            print()
            canvas.itemconfig(rectangle, fill='green3')
            if (ordre_classique):
                canvas.create_text(line_dimension1_x-40, line_dimension1_y, text=int(l[i:i+5].replace(" ",""),base=16), fill="black", font=('Arial'))
            else:
                canvas.create_text(line_dimension1_x+40, line_dimension1_y, text=int(l[i:i+5].replace(" ",""),base=16), fill="black", font=('Arial'))
            print("Port Source :",int(l[i:i+5].replace(" ",""),base=16))
            port_source=str(int(l[i:i+5].replace(" ",""),base=16))
            i+=6
            if (ordre_classique):
                canvas.create_text(line_dimension2_x+40, line_dimension2_y, text=int(l[i:i+5].replace(" ",""),base=16), fill="black", font=('Arial'))
            else:
                canvas.create_text(line_dimension2_x-40, line_dimension2_y, text=int(l[i:i+5].replace(" ",""),base=16), fill="black", font=('Arial'))
            print("Port Destination :",int(l[i:i+5].replace(" ",""),base=16))
            port_dest=str(int(l[i:i+5].replace(" ",""),base=16))
            i+=6
            print("Sequence Number :",int(l[i:i+11].replace(" ",""),base=16))
            Seq=str(int(l[i:i+11].replace(" ",""),base=16))
            i+=12
            print("Acknowledgment Number :",int(l[i:i+11].replace(" ",""),base=16))
            Ack=str(int(l[i:i+11].replace(" ",""),base=16))
            i+=12
            data_offset=int(l[i:i+1].replace(" ",""),base=16)
            print("Data Offset :",data_offset)
            i+=3
            flags=int(l[i],base=16)
            URG=0
            ACK=0
            PSH=0
            RST=0
            SYN=0
            FIN=0
            if (flags>=2 and flags <4)or (flags>=6 and flags <8) or (flags>=10 and flags <12) or (flags>=14 and flags <16):
                print("URG : 1")
                URG=1
            else:
                print("URG : 0")
            if (flags%2==1):
                print("ACK : 1")
                ACK=1
            else:
                print("ACK : 0")
            i+=1
            flags=int(l[i],base=16)
            if (flags>=8):
                print("PSH : 1")
                PSH=1
            else:
                print("PSH : 0")
            if (flags>=4 and flags <8)or flags>=12:
                print("RST : 1")
                RST=1
            else:
                print("RST : 0")
            if (flags>=2 and flags <4)or (flags>=6 and flags <8) or (flags>=10 and flags <12) or (flags>=14 and flags <16):
                print("SYN : 1")
                SYN=1
            else:
                print("SYN : 0")
            if (flags%2==1):
                print("FIN : 1")
                FIN=1
            else:
                print("FIN : 0")
            i+=2
            print("Window :",int(l[i:i+5].replace(" ",""),base=16))
            Win=str(int(l[i:i+5].replace(" ",""),base=16))
            i+=6
            print("Checksum :",int(l[i:i+5].replace(" ",""),base=16))
            i+=6
            print("Urgent Pointer :",int(l[i:i+5].replace(" ",""),base=16))
            i+=6
            TCP_options_length=data_offset*4-5*4
            i2=0
            #options TCP
            print("Options_TCP :")
            while(i2/2<TCP_options_length):
                if (l[i+i2:i+i2+2]=="00"):
                    print(" EOOL")
                    i2+=2
                    i+=1
                elif (l[i+i2:i+i2+2]=="01"):
                    print(" NOP")
                    i2+=2
                    i+=1
                else:
                    Option_type=" Unknown/"
                    if(l[i+i2:i+i2+2]=="02"):
                        Option_type=" MSS/"
                    if(int(l[i+i2:i+i2+2],base=16)==4):
                        Option_type=" Sack/"
                    if(int(l[i+i2:i+i2+2],base=16)==8):
                        Option_type=" Timestamp/"
                    if(int(l[i+i2:i+i2+2],base=16)==3):
                        Option_type=" WindowScale/"
                    i2+=2
                    i+=1
                    Option_taille=int(l[i+i2:i+i2+2],base=16)
                    i2+=2
                    i+=1
                    if (Option_taille!=2):
                        Option_type+=str(Option_taille)+"/"+str(int((l[i+i2:i+i2+Option_taille*2-4+Option_taille-2].replace(" ","")),base=16))
                    else:
                        Option_type+=str(Option_taille)
                    i2+=Option_taille*2-4
                    i+=Option_taille-2
                    print(Option_type)
            i+=i2
            http_valide=False
            #analyse des datas de TCP
            if(len(l)>i and l[i:i+2]!="  "):
                stop=False
                http=''
                while(l[i:i+2]!='' and l[i:i+2]!="  " and stop==False):
                    if(l[i:i+2]=="5C"or l[i:i+2]=="5c"):
                        if(l[i+3:i+5]=="72"):
                            if(l[i+6:i+8]=="5C"or l[i+6:i+8]=="5c"):
                                if(l[i+9:i+11]=="6E"or l[i+9:i+11]=="6e"):
                                    stop=True
                    if(l[i:i+2]=="0D"or l[i:i+2]=="0d"):
                        if(l[i+3:i+5]=="0A" or l[i+3:i+5]=="0a"):
                            if(l[i+6:i+8]=="0D"or l[i+6:i+8]=="0d"):
                                if(l[i+9:i+11]=="0A"or l[i+9:i+11]=="0a"):
                                    stop=True
                    http+=l[i:i+2]
                    i+=3
                http_i=1
                http_cpt=0
                mot_i=0
                while(http_i<len(http) and http_cpt<10):
                    if(http[http_i-1:http_i+1]=="0d"):
                        http_mot=http[mot_i:http_i-1]
                        # print(http_mot)
                        quote_mot = ''.join([chr(int(''.join(c), 16)) for c in zip(http_mot[0::2],http_mot[1::2])]).replace(';', '\n- ')
                        # print(quote_mot)
                        # print(http_cpt)
                        if(quote_mot=="HTTP/1.1"or quote_mot=="HTTP/1.2"):
                            http_valide=True
                        http_cpt+=9999999
                    if(http[http_i-1:http_i+1]=="20"or http[http_i-1:http_i+1]=="26"or http[http_i-1:http_i+1]=="3f"):
                        http_cpt+=1
                        http_mot=http[mot_i:http_i-1]
                        quote_mot = ''.join([chr(int(''.join(c), 16)) for c in zip(http_mot[0::2],http_mot[1::2])]).replace(';', '\n- ')
                        # print(quote_mot)
                        # print(http_cpt)
                        if(quote_mot=="HTTP/1.1"or quote_mot=="HTTP/1.2"):
                            http_valide=True
                        mot_i=http_i+1
                    http_i+=2
            #si c'est HTTP
            if(http_valide==True):
                print()
                canvas.itemconfig(rectangle, fill='cyan3')
                http2=http[0:http_i]
                quote = ''.join([chr(int(''.join(c), 16)) for c in zip(http[0::2],http[1::2])]).replace(';', '\n- ')
                print("FULL HTTP (CARE INSTABILITY) :")
                print(quote)
                quote2 = ''.join([chr(int(''.join(c), 16)) for c in zip(http2[0::2],http2[1::2])]).replace(';', '\n- ')
                canvas.create_text(550, line_dimension1_y-8, text=quote2, fill="black", font=('Arial'))
            if(http_valide==False):
                TCP_text=port_source+" -> "+port_dest+" ["
                premier_flags=True
                if (URG):
                    TCP_text+="URG"
                    premier_flags=False
                if (ACK):
                    if (premier_flags):
                        TCP_text+="ACK"
                    else:
                        TCP_text+=", ACK"
                    premier_flags=False
                if (PSH):
                    if (premier_flags):
                        TCP_text+="PSH"
                    else:
                        TCP_text+=", PSH"
                    premier_flags=False
                if (RST):
                    if (premier_flags):
                        TCP_text+="RST"
                    else:
                        TCP_text+=", RST"
                    premier_flags=False
                if (SYN):
                    if (premier_flags):
                        TCP_text+="SYN"
                    else:
                        TCP_text+=", SYN"
                    premier_flags=False
                if (FIN):
                    if (premier_flags):
                        TCP_text+="FIN"
                    else:
                        TCP_text+=", FIN"
                    premier_flags=False
                TCP_text+="] Seq="+Seq+" Ack="+Ack+" Win="+Win
                canvas.create_text(550, line_dimension1_y-8, text=TCP_text, fill="black", font=('Arial'))
        #IP
        else:
            canvas.create_text(550, line_dimension1_y-8, text="[Datagramme IPv"+version+"] couche 3 : "+ip_source+" -> "+ip_dest, fill="black", font=('Arial'))
    #ETHERNET
    else:
        canvas.create_text(550, line_dimension1_y-8, text="[Ethernet] couche 2 : "+mac_source+" -> "+mac_dest, fill="black", font=('Arial'))
    premier_passage_pour_de_vrai=False
    line_dimension1_x=200
    line_dimension2_x=900
    canvas.create_text(line_dimension1_x-140, line_dimension1_y, text=str(cpt), fill="black", font=('Arial'))
    l=l3[0:len(l3)-1]
    #lecture trame suivante
    l2=f.readline()
    if(l3=="FIN"):
        l="FIN"
    if(l2!='\n'and l2!=''):
        l2_size=int(l2[0:4],base=16)
    l=l[0:7+l2_size-1+l2_size*2]
    while(l2!='' and l2!="FIN"):            
        while(l2[0:4]!="0000" and l2!="FIN"):
            l+=' '+l2[7:7+l2_size-1+l2_size*2]
            l2=f.readline()
        l3=l2
        l2=''
root.mainloop()