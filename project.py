#################################     connection of database  #####################################################################   
def connectdb():
    dbroot=Toplevel()
    dbroot.grab_set()
    dbroot.geometry("470x250+745+240")
    dbroot.resizable(False,False)
    dbroot.config(bg="grey")
   

################################# connect db entry ########################################################################################


    hostLabel=Label(dbroot,text="Enter Host",bg="white",font=("times",20,"bold"),relief=GROOVE,borderwidth=3,width=13,anchor="w")
    hostLabel.place(x=10,y=10)
    
    
    userLabel=Label(dbroot,text="Enter User",bg="white",font=("times",20,"bold"),relief=GROOVE,borderwidth=3,width=13,anchor="w")
    userLabel.place(x=10,y=70)

    
    passwordLabel=Label(dbroot,text="Enter Password",bg="white",font=("times",20,"bold"),relief=GROOVE,borderwidth=3,width=13,anchor="w")
    passwordLabel.place(x=10,y=130)


#####################################   conect db replies    ##########################################################################
    

    hostval = StringVar()
    userval = StringVar()
    passwordval = StringVar()
    
    
    hostentry=Entry(dbroot,font=("roman",15,"bold"),bd=5,textvariable=hostval)
    hostentry.place(x=250,y=10)
    

    userentry=Entry(dbroot,font=("roman",15,"bold"),bd=5,textvariable=userval)
    userentry.place(x=250,y=70)

    
    passwordentry=Entry(dbroot,font=("roman",15,"bold"),bd=5,textvariable=passwordval)
    passwordentry.place(x=250,y=130)

 #######################################   submit button of db connectivity          ################################################
    submitbutton=Button(dbroot,text="SUBMIT",font=("roman",15,"bold"),width=20,activebackground="grey",activeforeground="white",bg="red",fg="white",borderwidth=5)
    submitbutton.place(x=150,y=190)

    dbroot.mainloop()

################################    FUNCTIONS OF PROJECT    ############################################################################
def tick():
    time_string=time.strftime("%H:%M:%S")
    date_string=time.strftime("%d/%m/%Y")
    clock.config(text="TIME:"+time_string+"\n"+"DATE:"+date_string)
    clock.after(200,tick)

#import random
#colours=["red","yellow","green","blue","white"]

#def colour():
#    fg=random.choice(colours)
#    SliderLabel.config(fg=fg)
#   SliderLabel.after(20,colour)
#import random
#cl=["red","yellow","green","blue","white"]
#def c():
   # fg=random.choice(cl)
   # clock.config(fg=fg)
   # clock.after(20,c)
from tkinter import*
from tkinter import Toplevel
import time


root=Tk()
root.title("PROJECT BY 1800274")
root.geometry("1174x700+100+40")
root.config(bg="grey")
root.resizable(False,False)


##################################       FRAME            ###############################################################################


DataEntryFrame=Frame(root,bg="grey",relief=GROOVE,borderwidth=5)
DataEntryFrame.place(x=10,y=80,width=500,height=600)


##########################################in left frame intro    #############################################################################

frontlabel=Label(DataEntryFrame,text="------------------------WELCOME------------------------",font=("arial",22," bold"),width=25,borderwidth=5,bg="grey",fg="white")
frontlabel.pack(side=TOP,expand=True)




#################################################################################################################################################
ShowEntryFrame=Frame(root,bg="grey",relief=GROOVE,borderwidth=5)
ShowEntryFrame.place(x=550,y=80,width=620,height=600)


##################################       SLIDER          ###############################################################################


SliderLabel=Label(root,text="Student Management Database System",font=("chiller",30,"italic bold"),relief=RIDGE,borderwidth=5,width=35,bg="grey",fg="white")
SliderLabel.place(x=307,y=0)

#colour()


##################################        clock          ################################################################################


clock=Label(root,font=("times",15,"bold"),relief=RIDGE,bg="Grey",borderwidth=5,fg="white")
clock.place(x=0,y=0)
tick()
#c()


##################################        DATABASE.BUTTON       ########################################################################
connectbutton=Button(root,text="CONNECT TO DATABASE",width=30,fg="white",bg="grey",activebackground="grey",activeforeground="white",borderwidth=5,relief=RIDGE,font=("times",10,"italic bold"),command=connectdb)
connectbutton.place(x=930,y=0)


##################################        buttons               ########################################################################


root.mainloop()



 
