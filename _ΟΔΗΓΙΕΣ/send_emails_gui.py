# This Python file uses the following encoding: utf-8
import sys

from email.policy import default
from turtle import color
import PySimpleGUI as sg
from send_emails import *


# Helper functions

# Split PDF from excel
def split_pdf_excel(values):
    # Get the filenames from the excel file
        filenames = get_folder_list(values['recipient_list_dir'])

        # Split the pdf
        output_dir = pdf_split(values['pdf_directory'],filenames)
        print('---> START spliting') 
        if output_dir == -1: 
            print('      Το .pdf δεν έχει τις ίδιες σελίδες με τις γραμμές της στήλης FOLDER-NAME του excel')
        else: 
            print('      Ο διαχωρισμός του αρχείου .pdf ολοκληρώθηκε, σε υποφακέλους στον: '+output_dir)
        print('---> END spliting')
        print(' ')
        return output_dir, filenames


# Get relative resource path for a particular file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# έλεγχος για δεξί κλικ στο multiline πεδίο για το USER e-mail-BODYκαι οι λειτουργίες του
right_click_menu = ['', ['Αντιγραφή', 'Επικόληση', 'Επιλογή όλων', 'Αποκοπή']]
def do_clipboard_operation(event, window, element):
    if event == 'Επιλογή όλων':
        element.Widget.selection_clear()
        element.Widget.tag_add('sel', '1.0', 'end')
    elif event == 'Αντιγραφή':
        try:
            text = element.Widget.selection_get()
            window.TKroot.clipboard_clear()
            window.TKroot.clipboard_append(text)
        except:
            print('Nothing selected')
    elif event == 'Επικόληση':
        try:
            element.Widget.insert(sg.tk.INSERT, window.TKroot.clipboard_get())
        except:
            print('Nothing to paste')
    elif event == 'Αποκοπή':
        try:
            text = element.Widget.selection_get()
            window.TKroot.clipboard_clear()
            window.TKroot.clipboard_append(text)
            element.update('')
        except:
            print('Nothing selected')






sg.theme('LightBrown3')

# We will create two columns for this layout
first_column = [
    [   
        sg.Image(resource_path("Logo.png"), size=(200,200)),
        sg.Column([
            [   sg.Text("             ")],
            [   sg.Text("             ")],
            [   sg.Text("             ")],
            [   sg.Text("Εφαρμογή αυτοματοποιημένης μαζικής αποστολής",text_color='DarkGoldenrod4')],
            [   sg.Text("προσωποποιημένων e-mail,",text_color='DarkGoldenrod4')],
            [   sg.Text("σε παραλήπτες που βρίσκονται σε .xls,  ",text_color='DarkGoldenrod4')],
            [   sg.Text("με οσαδήποτε προσωποποιημένα           ",text_color='DarkGoldenrod4')],
            [   sg.Text("συνημμένα αρχεία από υποφακέλλους.    ",text_color='DarkGoldenrod4')],
            [   sg.Button(button_text='Οδηγίες', key='Οδηγίες' ,button_color='dark orange')]
        ],size=(270,250))
    ],
    [   sg.Text("_____________")],
    [   sg.Text(" Α. ΑΡΧΙΚΕΣ ΛΕΙΤΟΥΡΓΙΕΣ",font=("Arial",16)), sg.Text("(Προαιρετικά, πριν την αποστολή ή/και χωρίς αποστολή)",font=("Arial",11))],
    [    
        sg.Button('Δημιουργία υποφακέλων (με βάση τη στήλη FOLDER-NAME του .xls/.xlsx που θα δηλώσετε πιο κάτω), για αρχεία που θα θέλατε να επισυναφθούν στο e-mail',size=(65, 2),key='make_folders',font=("Arial",11),button_color='dark slate gray')
    ],
    [    
        sg.Button('Διαχωρισμός του .PDF που θα δηλώσετε πιο κάτω, σε ξεχωσιστά ανά σελίδα σε υποφακέλους (με βάση τη στήλη FOLDER-NAME του .xls που θα δηλώσετε πιο κάτω) ',size=(65, 2),key='pdf_split',font=("Arial",11),button_color='dark slate gray')
    ], 
    [   sg.Text("             ")],
    [   sg.Text("_____________")],
    [   sg.Text("Β. LOGIN",font=("Arial",16)), sg.Text("(Λογαριασμός e-mail αποστολέα)",font=("Arial",11))],
    [
        sg.Text("    Username/From:",size=(14,1),font=("Arial",12)),
        sg.In(size=(50, 1), font=("Arial",12), enable_events=True,key='username',default_text='ac@athenscollege.edu.gr'),
    ],
    [
        sg.Text("    Password:",size=(14,1),font=("Arial",12)),
        sg.In(size=(16, 1), font=("Arial",12), enable_events=True,key="password",default_text='Dy7oKajk',password_char='*'),
    ],
    [   sg.Text("             ")],
    [   sg.Text("_____________")],
    [   sg.Text("Γ. ΔΗΜΙΟΥΡΓΙΑ e-MAIL",size=(20,1),font=("Arial",16)) ],
    [   sg.Text("             ")],
    [
        sg.Text("    From:",font=("Arial",14))],
    [
        sg.Text("                "),
        sg.In(size=(50, 3), font=("Arial",12), enable_events=True,key="mail_from",default_text='ac@athenscollege.edu.gr',readonly=True),
    ],
    [   sg.Text("        ")],
    [
        sg.Text("    To/CC/BCC (από αντίστοιχες στήλες του αρχείου EXCEL): ",font=("Arial",14))
    ],
    [
        sg.Text("                "),
        sg.In(size=(50, 1), font=("Arial",12), enable_events=True,key="recipient_list_dir",default_text='./01list/list.xlsx'),
        sg.FileBrowse()
    ],
    [   sg.Text("             ")],
    [
        sg.Text("    Subject:",font=("Arial",14))],
    [
        sg.Text("                "),
        sg.In(size=(50, 1),font=("Arial",12), enable_events=True,key="mail_subject",default_text='Κολλεγίο Αθηνών'),
    ],
    [   sg.Text("        ")],
    [   sg.Text("    Body:",font=("Arial",14))],
    [
        sg.Text("        ...από oποιοδήποτε .html αρχείο (*):",font=("Arial",11))
    ],
    [ 
        sg.Text("                "),
        sg.In(size=(50, 1), font=("Arial",12), enable_events=True,key="mail_body",default_text='./02email_body/body.html'),
        sg.FileBrowse()
    ],
    [   sg.Text("           (*) ή απλό κείμενο (και με: {ΝΑΜΕ}, και άλλα πεδία από το .xlsx με {...}) στο πεδίο που ακολουθεί: ",font=("Arial",10),text_color='steel blue')],
    [   sg.Text("               ΣΗΜΕΙΩΣΗ: Αν συμπληρώσετε κείμενο εδώ, θα αποσταλλεί αυτό ως e-mail body" ,font=("Arial",10),text_color='steel blue')], 
    [   sg.Text("                                    και όχι το αρχείο .html ...του προηγούμενου βήματος.",font=("Arial",10),text_color='steel blue')],
    [
        sg.Text("     "),
        sg.Multiline(size=(71,15),  key='USER_MAIL_BODY', right_click_menu = right_click_menu, horizontal_scroll=True)],
    [   sg.Text("        ")],
    [   sg.Text("    Attachements:",font=("Arial",14))],
    [   sg.Text("       A. Επισύναψη αρχείων από υποφακέλους:",font=("Arial",11)),
        sg.Checkbox(" (Ναι/Όχι)",  key="Attachements_yn", default=True)],        
    [
        sg.Text("            Nαι=Αρχεία από τους ατομικούς υποφακέλλους του:",font=("Arial",11))
    ],
    [
        sg.Text("                "),
        sg.In(size=(46, 1), font=("Arial",12), enable_events=True,key="files_directory",default_text='./03folders/'),
        sg.FolderBrowse()
    ],
    [   sg.Text("       B. ή/και επισύναψη σελίδων/αρχείων από το διαχωρισμένο .pdf:",font=("Arial",11)),
        sg.Checkbox(" (Ναι/Όχι)",  key="Attachements_from_pdf_yn",default=True)
    ],
    [
        sg.Text("            Ναι=Αρχεία από τo διαχωρισμένο σε σελίδες .pdf:",font=("Arial",11))
    ],
    [
        sg.Text("                 "),
        sg.In(size=(46, 1), font=("Arial",12), enable_events=True,key="pdf_directory",default_text='./04pdf/Sourcefile.pdf'),
        sg.FileBrowse()
    ],
    [   sg.Text("             ")],
    [   sg.Text("             ")],
    [   sg.Text("_____________")],
    [   sg.Text("Δ. ΑΥΤΟΜΑΤΟΠΟΙΗΜΕΝΗ ΑΠΟΣΤΟΛΗ",font=("Arial",16)) ],
    [
        sg.Submit(' Εκκίνηση αυτoματοποιημένης αποστολής ',  size=(50, 2), key='Submit' , font=("Arial",14), button_color='aquamarine3' )
    ],
    [   sg.Text("               ")],
    [   sg.Text("               ")],
    [   sg.Text("               ")]
    
]

second_column = [
    [
        sg.Text("Ε. ΠΡΟΒΟΛΗ ΕΡΓΑΣΙΩΝ - ΑΠΟΣΤΟΛΗΣ",font=("Arial",16))
    ],
    [
        sg.Output(size=(100,55), key='-OUTPUT-',expand_x=True,expand_y=True)
    ]
]

col1 = sg.Column(first_column, scrollable=True, vertical_scroll_only=True,sbar_trough_color='light goldenrod',sbar_background_color='sandy brown')
col2 = sg.Column(second_column)
window = sg.Window('Mass Mailer [POBO Athens College]', [[col1,col2]],resizable=True, finalize=True)
col1.expand(False,True)
col2.expand(True,True)


threads     = []
PREV_EMAIL  = -1
NUM         = 0
jobs        = Queue()
unsent      = Queue()








while True:
    event, values = window.read(timeout=1)

    # If username is changed then update the text
    if (event=='username'): window['mail_from'].Update(values['username'])

    # print(event, values)
    if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Cancel') and sg.popup_yes_no('Do you really want to cancel?') == 'Yes': break
    
    # έλεγχος για δεξί κλικ στο multiline πεδίο για το USER e-mail-BODY
    mline:sg.Multiline = window['USER_MAIL_BODY']
    if event in right_click_menu[1]:
            do_clipboard_operation(event, window, mline)


     
    if event =='Οδηγίες':
       sg.popup_scrolled('\
Α.ΑΡΧΙΚΕΣ ΛΕΙΤΟΥΡΓΙΕΣ \n \n \
    - A1.ΔYΝΑΤΟΤΗΤΑ ΔΙΑΧΩΡΙΣΜΟΥ .pdf: Μπορούμε να διαχωρίσουμε ένα αρχείο .pdf σε τόσες σελίδες όσες και οι γραμμές του .xls/xlsx \
(για παράδειγμα ένα αρχείο προσωποποιημένων βεβαιώσεων παρακολούθησης από mail-merge). \
Αν επιλέξουμε ανάλογα, η εφαρμογή μπορεί να κόψει κάθε σελίδα σε ξεχωριστό .pdf με το όνομα που θα βρει στη στήλη FOLDER-NAME απο το .xls/xlsx \
και να το επισυνάψει, ανάλογα πάντα με την αντίστοιχη επιλογή, ως επιπλέον ή μοναδικό συνημμένο αρχείο προς τον παραλλήπτη της αντίστοιχης γραμμής στο .xls/xlsx. \n \n \
    - A2.ΔΗΜΙΟΥΡΓΙΑ ΥΠΟΦΑΚΕΛΛΩΝ με βάση τα ονόματα που θα βρει στη στήλη FOLDER-NAME του .xls/xlsx. \n \
Ότι αρχείο/α τοποθετηθεί/θούν στον υποφάκελο FOLDER-NAME, θα ενσωματωθεί/θούν ως ατομικό/κά συνημμένο/να για κάθε παραλήπτη \
(αν επιλέξετε κάτι τέτοιο φυσικά).  \n \
Άν βρει και στήλη FOLDER1 ή/και FOLDER2 θα δημιουργήσει υποφάκελο στο FOLDER-NAME. \n \
Άν βρει και στήλη FOLDER1-... θα δημιουργήσει nested folder στο FOLDER1. \n \
Άν βρει και στήλη FOLDER2-... θα δημιουργήσει nested folder στο FOLDER2. \n \n \n\
Β.ΔΥΝΑΤΟΤΗΤΕΣ ΤΟΥ ΑΡΧΕΙΟΥ EXCEL. \n\
Για την αποστολή χρειαζόμαστε απαραίτητα το αρχείο .xls/xlsx, το οποίο περιέχει απαραίτητες και μη στήλες, \
με απαραίτητο ή μη περιεχόμενο. Οι βασικές στήλες του αρχείου αυτού είναι:  \n \n \
    - ΕMAIL (Κεφαλαία αγγλικά γράμματα)\n \
      (Υποχρεωτική στήλη και περιεχόμενο): \n \
Σε κάθε γραμμή της στήλης αυτής περιέχεται το e-mail του παραλήπτη. \n \n \
    - FOLDER-NAME (Κεφαλαία αγγλικά γράμματα) \n \
      (Mη υποχρεωτική στήλη ή/και περιεχόμενο): \n \
Αν θελήσουμε όμως να υπάρχει μπορεί να δημιουργήσει φάκελο (με το όνομα -για παράδειγμα- κάθε παραλλήπτη), \
όπου θα τοποθετήσουμε (μετά τη δημιουργία των φακέλων) τα αρχεία που επιθυμούμε, για επισύναψη (όλα όσα βρει και οποιουδήποτε τύπου μέσα στο φάκελο). \
Αν δεν υπάρχει (περιεχόμενο) στη γραμμή για κάποιο παραλλήπτη, απλά δεν θα συμπεριληφθεί κάποιο αρχείο ως συνημμένο.  \n  \
    - FOLDER1 \n \
Άν βρει και στήλη FOLDER1 ή/και FOLDER2 θα δημιουργήσει υποφάκελο στο FOLDER-NAME. \n \
    - FOLDER1-... \n \
Άν βρει περιεχόμενο στη στήλη με τFOLDER1-... θα δημιουργήσει nested folder στο FOLDER1. \n \
    - PREFIX ή/και \n \
    - ΝΑΜΕ ή/και οποιαδήποτε \n \
    - ΑΛΛΗ/ΑΛΛΕΣ ΣΤΗΛΗ/ΣΤΗΛΕΣ \n \
      (Mη υποχρεωτικές στήλες): \n \
Αν υπάρχει περιεχόμενο σ αυτές, μπορεί να ενσωματωθεί στο body ενός e-mail μέσα σε {}. \
(π.χ. Αγαπητέ {PREFIX} {ΝΑΜΕ} ...το υπόλοιπό σας είναι {YPOLOIPO} ...) \n  \
    - CC \n \
      (Mη υποχρεωτική στήλη ή/και περιεχόμενο): \n  \
Αν βρει e-mail (ή/και περισσότερα από ένα με ; ανάμεσα) θα το/τα συμεριλάβει ανάλογα. \n  \
    - BCC \n \
      (Mη υποχρεωτική στήλη ή/και περιεχόμενο): \n  \
Αν βρει e-mail (ή/και περισσότερα από ένα με ; ανάμεσα) θα το/τα συμπεριλάβει ανάλογα.\
',size=(70,40),font=("Arial",11),background_color='SandyBrown' ,keep_on_top=True, title='Οδηγίες')


    if (event == sg.WINDOW_CLOSED): break

    if (event == 'pdf_split') and sg.popup_yes_no('Αν επιλέξετε [Yes] θα γίνουν: \n \n 1. Έλεγχος συμφωνίας αριθμού γραμμών της στήλης FOLDER-NAME του αρχείου EXCEL ...με τον αριθμό σελίδων του αρχικού .pdf  \n \n 2. Δημιουργία τόσων υποφακέλλων όσων και οι γραμμές της στήλης FOLDER-NAME του αρχείου EXCEL ...με το όνομα που υπάρχει σε κάθε μία από αυτές τις γραμμές. \n \n 3. Διαχωρισμός του αρχικού .pdf σε ξεχωριστά (ένα για κάθε σελίδα, με όνομα από τις γραμμές της στήλης FOLDER-NAME του αρχείου EXCEL). \n \n 4. Ενσωμάτωση (μόνο με την αντίστοιχη πιο πάνω επιλογή: [Σελίδες από το διαχωρισμένο .pdf=Nαι]), κάθε .pdf που προέκυψε, ως επιπλέον (ή μοναδικό ανάλογα με τις πιο πάνω επιλογές) συνημμένο για κάθε παραλήπτη.', title='Επιβεβαίωση ΔΙΑΧΩΡΙΣΜΟΥ .pdf',font=("Arial",11), background_color='light grey' ,keep_on_top= True) == 'Yes': split_pdf_excel(values)       

    if (event == 'make_folders') and sg.popup_yes_no('Αν επιλέξετε [Yes] \n \n θα δημιουργηθούν μέσα στο φάκελο των συνημμέμνων, υποφάκελοι με ονόματα που περιέχει η στήλη FOLDER-NAME του αρχείου EXCEL. \n \n _______ \n \n Στη συνέχεια μπορείτε να τοποθετήσετε σε κάθε υποφάκελο, τα απομικά αρχεία (οποιουδήποτε τύπου), τα οποία επιθυμείτε να επισυναφθούν σε κάθε e-mail παραλήπτη. \n \n Προσοχή, ώστε το συνολικό μέγεθος συνημμένων αρχείων ανά παραλήπτη, να μην ξεπερνά το μέγεθος που μπορεί να εξυπηρετήσει το e-mail στο οποίο θα γίνει η αποστολή.',title='Επιβεβαίωση ΔΗΜΙΟΥΡΓΙΑΣ υποφακέλλων',font=("Arial",11), background_color='light grey' ,keep_on_top= True) == 'Yes': 
        files_directory     = values['files_directory']
        recipient_list_dir  = values['recipient_list_dir']
        make_folders_from_xls(files_directory,recipient_list_dir)       

    if (event == 'Submit') and sg.popup_yes_no('Σίγουρα θέλετε να συνεχίσω ... \n με την αυτόματη αποστολή όλων των e-mail \n (προτείνεται όχι περισσότερα από 300-400 τη φορά), \n τα οποία βρίσκονται στην αντίστοιχη στήλη EMAIL του .xls \n και σύμφωνα με τις παραμέτρους που ορίσατε πριν;', title='Επιβεβαίωση ΑΠΟΣΤΟΛΗΣ', font=("Arial",11), background_color='aquamarine' ,keep_on_top= True) == 'Yes':

        username        = values['username']
        password        = values['password']
        mail_from       = values['mail_from']
        mail_subject    = values['mail_subject']
        mail_body_dir   = values['mail_body']
        Attachements_yn = values["Attachements_yn"]

        files_directory     = values['files_directory']
        recipient_list_dir  = values['recipient_list_dir']


        # Get the attachments
        attachments, attachment_names, recipient_list, success = collect_attachments(files_directory, Attachements_yn, recipient_list_dir)
        NUM = len(list(recipient_list.values())[0])

        # If we want a pdf as well
        if values['Attachements_from_pdf_yn'] == True:
            # Split the pdf
            output_dir_split, filenames = split_pdf_excel(values)
            
            # If it was split correctl, load the attachments
            if output_dir_split != -1:
                attachments_split, attachment_names_split, recepient_list_split, success_split = collect_attachments(str(output_dir_split),True,recipient_list_dir)
                
                # Instantiate arrays if needed
                if attachments == []:
                    attachments      = [None]*len(success_split)
                    attachment_names = [None]*len(success_split)
                    success          = [None]*len(success_split)

                # Append the split pdf attachments
                for i in range(len(success_split)):
                    if success_split[i]: 
                        attachments[i]      = attachments_split[i]      if attachments[i] is None       else attachments[i] + attachments_split[i]
                        attachment_names[i] = attachment_names_split[i] if attachment_names[i] is None  else attachment_names[i] + attachment_names_split[i]
                        success[i]          = success_split[i]          if success[i] is None           else success[i] and success_split[i]
            else: 
                print("-------------------------------")
                print("Η διαδικασία αποστολής ΣΤΑΜΑΤΗΣΕ.") 
                print("Ελέγξτε τον αριθμό σελίδων στο αρχείο .pdf να είναι ίδιος με τον αριθμό γραμμών στο .xls")
                print("--> END (Χωρίς αποστολή)") 
               
                continue
                        
        # if failed_split: continue

        if values['USER_MAIL_BODY'] == '':
            # Read the body of the file
            mail_body_file  = open(mail_body_dir,'r',encoding='utf8')
            mail_body       = mail_body_file.read()
            mail_body_file.close()

        else:
            mail_body = values['USER_MAIL_BODY'].replace('\n','<br>')

        # Put all the emails in a Queue
        jobs = get_email_queue(attachments,attachment_names,recipient_list,mail_body,username,password,mail_from,mail_subject,print_func=sg.Print)

        # Create some workers to send emails in parallel
        threads = get_workers(jobs,NUM_THREADS=5)

        # Start sending emails
        print('--> START sending %d emails on %d Threads'%(NUM,len(threads)))
        for t in threads: t.start()
        PREV_EMAIL = 0

    # Print the status of the task
    if jobs.empty() and PREV_EMAIL >= 0:
        PREV_EMAIL = -1
        print('\tLast Batch')

    elif PREV_EMAIL != jobs.qsize() and PREV_EMAIL != -1:
        print("\t%4d e-mails left"%jobs.qsize())
        PREV_EMAIL = jobs.qsize()

    if PREV_EMAIL == -1 and len(threads) > 0:
        T = True
        for t in threads:
            T = T and not t.is_alive()
        
        # If all the threads have stopped working
        if T:
            print("--> END (Με αποστολή) %d e-mails"% NUM)
            threads = []
            NUM     = 0

        

window.close()