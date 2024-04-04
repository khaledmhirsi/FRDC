#    Tk Project    #
#   Part A and B   #


# Imports
from tkinter import * # For the GUI 
from tkinter import filedialog, messagebox, ttk # For browsing the images, open spreadsheets, error window
from PIL import ImageTk, Image # For Displaying Images on the GUI
import requests # For Downloading image from URL
import urllib.request # For Downloading image from URL if requests doesn't work
import shutil # For Creating temporary files
import os # For Managing files and directories
import cv2 # For Preprocess images


# System program
class GUIfaceRecoginitionBasedSystem:
    def __init__(self):
        
        # Initiate variables 
        self.character_limit = 100
        self.image = None
        self.temp_URL = ''
        self.filename = ''
        self.img_directory = ''
        self.faces_number = 0
        self.title_font_size = 16
        self.text_font_size = 12
        self.temporary_files = []
        self.already_downloaded_file = False
        self.username = ''
        self.logged_in = False
        # Choose values for image resizing
        self.image_height = 500 
        self.image_width = 600
        
        # Initiate GUI 
        self.root = Tk() 
        self.root.tk.call('source', 'theme\\forest-dark.tcl')
        ttk.Style().theme_use('forest-dark')


        self.root.title("Face Recognition App") # Title of the window
        self.root.geometry("1350x800+0+0") # Size of the window
        self.root.iconbitmap('data/icon.ico')
        
        self.top_menu = Menu(self.root)
        self.root.config(menu=self.top_menu)  
        
        
        self.URL_source = IntVar()
        self.URL_source.set(None)
        
        
        # Define functions and widgets
        self.face_detection_menu = Frame(self.root, padx= 10, pady= 10)
        
        
        self.step1_frame = LabelFrame(self.face_detection_menu, text='Step 1: Provide the image', padx= 10, pady= 10,font=('Cambria', self.title_font_size))
        self.step1_frame.grid(row=0, column=0, padx = 50, pady=50)
        
        
        self.step2_frame = LabelFrame(self.face_detection_menu, text=f'Step 2: Import the image\nDisplayed at {self.image_width}x{self.image_height}', padx= 10, pady= 10,font=('Cambria', self.title_font_size))
        self.step2_frame.grid(row=0, column=1,padx= 50, pady= 50)
        self.image_label = Label(self.step2_frame)
        
        
        self.step3_frame = LabelFrame(self.face_detection_menu, text='Step 3: Detect Faces', padx= 10, pady= 10 ,font=('Cambria', self.title_font_size))
        self.step3_frame.grid(row=0, column=3,padx= 50, pady= 50)
        
        
        def display_image():
            
            if self.URL_source.get() == 0: # Read the URL
            
            
                if not self.already_downloaded_file:
                    try:
                        self.filename = 'temp/' + 'internet_image.jpg'

                        # calling urlretrieve function to get resource
                        urllib.request.urlretrieve(self.temp_URL, self.filename)
                        
                    except Exception:
                        try:
                            self.filename = 'temp/' + self.temp_URL.split("/")[-1]
                            requests_data = requests.get(self.temp_URL, stream = True)
                            if requests_data.status_code == 200:
                            # Set decode_content value to True, otherwise the downloaded image file's size will be zero
                                requests_data.raw.decode_content = True

                                # Open a local file with wb ( write binary ) permission.
                                with open(self.filename,'wb') as file_to_create:
                                    shutil.copyfileobj(requests_data.raw, file_to_create)
                        except Exception:
                            messagebox.showerror("Invalid URL", "Please make sure you have right clicked on the image and selected 'Open Image in a Tab' before copying its link.")
                        

                self.already_downloaded_file = True
                    
                try:
                    self.temp_image = Image.open(self.filename)
                    self.image = self.temp_image.resize((self.image_width, self.image_height))
                    self.temp_image = ImageTk.PhotoImage(self.image)
                    self.image_label['image'] = self.temp_image
                    self.image_label.pack()
                    self.grey_scale_button['state'] = ACTIVE
                    self.detect_face_button['state'] = DISABLED
                except Exception:
                    messagebox.showerror("Unknown Error", "Please try an other link.")
    
            if self.URL_source.get() == 1: # Read the directory
                
                try:
                    self.temp_image = Image.open(self.img_directory)
                    self.image = self.temp_image.resize((self.image_width, self.image_height))
                    self.temp_image = ImageTk.PhotoImage(self.image)
                    self.image_label['image'] = self.temp_image
                    self.image_label.pack()
                    self.grey_scale_button['state'] = ACTIVE
                    self.detect_face_button['state'] = DISABLED
                except Exception:
                    messagebox.showerror("Invalid Directory", "Please make sure the directory submitted exists, and also that the name of the file and its extension are included.")

                       
        self.display_image_button = Button(self.step2_frame, state=DISABLED, text='Import Image', command=display_image, font=('Cambria', self.text_font_size)) 
 

        def detect_Face(url_or_directory):    
            if not self.logged_in:
                messagebox.showinfo("Not Logged in", "If you are not logged in, your data will be deleted when you exit the program.")         
            # Load Cascade
            haar_cascade_face = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
            # Load grey image and original image
            loaded_img = cv2.imread('temp/greyed_image.png')
            image = cv2.imread(self.filename).copy() if url_or_directory == 0 else cv2.imread(self.img_directory).copy()
            image_copy = image.copy()
            
            # Applying the haar classifier to detect faces
            faces_rectangle = haar_cascade_face.detectMultiScale(loaded_img, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
            # Store face numbers
            self.faces_number = len(faces_rectangle)
            if self.faces_number > 0:
                cropped_face_number = 0
                # For each face on the image detected by OpenCV
                for (x, y, w, h) in faces_rectangle:
                    # Save faces
                    crop_img = image[y:y+h, x:x+w]
                    dir = f'temp/face{cropped_face_number}.png'
                    cropped_face_number += 1
                    if self.logged_in:
                        for file in os.listdir(f'users/{self.username}'):
                            if os.path.basename(file) == f'face{cropped_face_number}.png':
                                cropped_face_number += 1
                        dir = f'users/{self.username}/face{cropped_face_number}.png'
                    cv2.imwrite(dir, crop_img)
                    
                    # Draw a rectangle around the face
                    cv2.rectangle(image_copy, # Image
                                (x, y), # Bottom left of the rectangle
                                (x+w, y+h), # Top right corner of the rectangle
                                (10, 255, 149),  # color in BGR
                                5) # thickness in px
            
            # Store Image and display it on the GUI
            cv2.imwrite('temp/preprocessed_image.png',image_copy)
            
            self.temp_image = Image.open('temp/preprocessed_image.png')
            self.image = self.temp_image.resize((self.image_width, self.image_height))
            self.temp_image = ImageTk.PhotoImage(self.image)
            self.image_label['image'] = self.temp_image
            self.grey_scale_button['state'] = DISABLED
            self.display_image_button['text'] = 'Display Original Image'
        
        self.detect_face_button = Button(self.step3_frame, text='Save Detected Face', foreground='red', command=lambda: detect_Face(self.URL_source.get()), state=DISABLED, font=('Cambria', self.text_font_size))
        
        
        def gray_scale(url_or_directory):
            
            if url_or_directory == 0: 
                loaded_img = cv2.imread(self.filename)
            if url_or_directory == 1:
                loaded_img = cv2.imread(self.img_directory)
                            
            final_img = cv2.cvtColor(loaded_img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite('temp/greyed_image.png',final_img)
            self.temp_image = Image.open('temp/greyed_image.png')
            self.image = self.temp_image.resize((self.image_width, self.image_height))
            self.temp_image = ImageTk.PhotoImage(self.image)
            self.image_label['image'] = self.temp_image
            
            self.display_image_button['text'] = 'Display Original Image'
            self.detect_face_button['state'] = ACTIVE
            
        self.grey_scale_button = Button(self.step3_frame, text='Grey Scale', foreground='blue', command=lambda: gray_scale(self.URL_source.get()), state=DISABLED, font=('Cambria', self.text_font_size))

        
            # URL Option
        self.URL_widgets = []
        def URL():
            for widget in self.URL_widgets:
                widget.pack_forget()
            for widget in self.directory_widgets:
                widget.pack_forget()
            
            self.text_URL = Label(self.step1_frame, text= 'Input an valid URL:', font=('Cambria', self.text_font_size))
            self.text_URL.pack()
            
            self.input_field_URL = Entry(self.step1_frame)
            self.input_field_URL.pack() 

            def get_input_URL():
                self.already_downloaded_file = False
                self.temp_URL = self.input_field_URL.get()
                if self.temp_URL != "" :
                    self.display_image_button['state'] = ACTIVE
                    self.display_image_button['text'] = 'Import Image'
                self.grey_scale_button['state'] = DISABLED
                self.detect_face_button['state'] = DISABLED
            self.button_URL = Button(self.step1_frame, text='Submit', command=get_input_URL, font=('Cambria', self.text_font_size))
            self.button_URL.pack()
            
            self.URL_widgets = [self.text_URL, self.input_field_URL, self.button_URL]
        
        
            # Directory Option
        self.directory_widgets = []
        def directory():
            for widget in self.URL_widgets:
                widget.pack_forget()
            for widget in self.directory_widgets:
                widget.pack_forget()
                
            self.browse_text = Label(self.step1_frame, text= 'Browse your image:', font=('Cambria', self.text_font_size))
            self.browse_text.pack()
            
            def browse():
                temp_directory = filedialog.askopenfilename(title='Select An Image', filetypes=(('PNG Files', '*.png'), ('JPG Files', '*.jpg'), ('JPEG Files', '*.jpeg'), ('Webp Files', '*.webp'), ('Other Files', '*.*')))
                if temp_directory != '':
                    self.img_directory = temp_directory
                self.display_image_button['state'] = ACTIVE
                self.display_image_button['text'] = 'Import Image'
                self.grey_scale_button['state'] = DISABLED
                self.detect_face_button['state'] = DISABLED
            self.button_browse = Button(self.step1_frame, text='Browse', command=browse, font=('Cambria', self.text_font_size))
            self.button_browse.pack()    
                
            self.text_directory = Label(self.step1_frame, text= 'Input a valid directory:', font=('Cambria', self.text_font_size))
            self.text_directory.pack()
            
            self.input_field_directory = Entry(self.step1_frame)
            self.input_field_directory.pack()
            
            def get_input_directory():
                temp_directory = self.input_field_directory.get()
                if temp_directory != '':
                    self.img_directory = temp_directory
                self.display_image_button['state'] = ACTIVE
                self.display_image_button['text'] = 'Display Image'
                self.grey_scale_button['state'] = DISABLED
                self.detect_face_button['state'] = DISABLED
            self.button_directory = Button(self.step1_frame, text='Submit', command=get_input_directory, font=('Cambria', self.text_font_size))
            self.button_directory.pack()
            
            self.directory_widgets = [self.button_directory, self.input_field_directory, self.text_directory, self.browse_text, self.button_browse]


        self.select_URL = Radiobutton(self.step1_frame, text='By URL', variable=self.URL_source, value=0, command=URL, font=('Cambria', self.text_font_size))
        self.select_directory = Radiobutton(self.step1_frame, text='By Directory', variable=self.URL_source, value=1, command=directory, font=('Cambria', self.text_font_size))
        
        # Step 1: Gathering Data
        self.select_URL.pack()
        self.select_directory.pack()
        
        # Step 2: Display the image  
        self.display_image_button.pack() 
        self.temp_image = Image.open('data/blank.png')
        self.image = self.temp_image.resize((self.image_width, self.image_height))
        self.temp_image = ImageTk.PhotoImage(self.image)
        self.image_label['image'] = self.temp_image
        self.image_label.pack()
        
        # Step 3: Process the image
        self.grey_scale_button.pack()
        self.detect_face_button.pack()
        
        
        self.register_menu = LabelFrame(self.root, text='Register', padx= 100, pady= 100 ,font=('Cambria', self.title_font_size+10))
        self.login_menu = LabelFrame(self.root, text='Login', padx= 100, pady= 100 ,font=('Cambria', self.title_font_size+10))
        
        
        menus = [self.login_menu, self.register_menu, self.face_detection_menu]
        
        def clean_menus():
            for menu in menus:
                menu.pack_forget()
                
        # Create Bar Menu
        self.register_widgets = []
        def register_menu():
            
            for widget in self.register_widgets:
                widget.pack_forget()
            clean_menus()
            username = StringVar()
            password = StringVar()
            
            self.register_menu.pack()
            register_label = Label(self.register_menu, text="Register an account if you don't already have one.", font=('Times', 12), padx= 10, pady= 10)
            register_label.pack()
            
            username_label = Label(self.register_menu, text='Username*', font=('Cambria', self.title_font_size), padx= 25, pady= 25)
            username_label.pack()
            username_field = Entry(self.register_menu, textvariable=username)
            username_field.pack()
            
            password_label = Label(self.register_menu, text='Password*', font=('Cambria', self.title_font_size), padx= 25, pady= 25)
            password_label.pack()
            password_field = Entry(self.register_menu, textvariable=password)
            password_field.pack()
            
            
            success_label = Label(self.register_menu, text='Registered Successfully! You can now Login with your new account!', foreground='green', font=('Times', 12), padx= 10, pady= 10)
            def register_user():
                username_information = username.get()
                password_information = password.get()
                
                if username_information == '' or len(username_information)<2:
                    messagebox.showerror("Invalid Username", "Please make sure it your username at least 2 characters.")
                    username_field.delete(0, END)
                    return
                
                elif password_information == '' or len(password_information) <8:
                    messagebox.showerror("Invalid Password", "For security reasons, please make sure your password is at least 8 characters.")
                    password_field.delete(0, END)
                    return
                
                for file in os.listdir('users'):
                    if os.path.basename(file) == username_information:
                        messagebox.showerror("Username Already Existing", "This username was already taken, please use an other one.")
                        username_field.delete(0, END)
                        return
                
                os.mkdir('users/'+username_information)
                file = open('users/' + username_information + '/' + username_information + '.txt' , 'w')
                file.write(username_information + '\n' + password_information)
                file.close()
                
                username_field.delete(0, END)
                password_field.delete(0, END)
                success_label.pack_forget()
                success_label.pack()
                
                
            mandatory_label = Label(self.register_menu, text='The fields marked with * are mandatory.',pady=10, padx=10, foreground='red', font=('Calibri', 9))
            mandatory_label.pack()
            
            register_button = Button(self.register_menu, text='Register', font=('Cambria', self.title_font_size), padx= 20, pady= 10, command=register_user)
            register_button.pack()
            
            self.register_widgets = [password_field, password_label, username_field, username_label, register_label, register_button, mandatory_label, success_label]
            
            
        self.login_widgets = []
        def login_menu():
            for widget in self.login_widgets:
                widget.pack_forget()
            clean_menus()
            success_label2 = Label(self.login_menu, text='Logged in Successfully! You can link a face database to your account!', foreground='green', font=('Times', 12), padx= 10, pady= 10)
            if not self.logged_in:
                username = StringVar()
                password = StringVar()
                
                self.login_menu.pack()
                register_label2 = Label(self.login_menu, text="Enter your credentials down below.", font=('Times', 12), padx= 10, pady= 10)
                register_label2.pack()
                
                username_label2 = Label(self.login_menu, text='Username', font=('Cambria', self.title_font_size), padx= 25, pady= 25)
                username_label2.pack()
                username_field2 = Entry(self.login_menu, textvariable=username)
                username_field2.pack()
                
                password_label2 = Label(self.login_menu, text='Password', font=('Cambria', self.title_font_size), padx= 25, pady= 25)
                password_label2.pack()
                password_field2 = Entry(self.login_menu, textvariable=password)
                password_field2.pack()
                
            
                def login_user():
                    
                    username_information = username.get()
                    password_information = password.get()
                    
                    user_list = os.listdir('users/')
                    if username_information in user_list :
                        file = open('users/' + username_information + '/' + username_information + '.txt', 'r')
                        credentials = file.read().splitlines()
                        if password_information in credentials:
                            username_field2.delete(0, END)
                            password_field2.delete(0, END)
                            success_label2.pack_forget()
                            for widget in self.login_widgets:
                                widget.pack_forget()
                            self.username = username_information
                            
                            self.logged_in = True
                            success_label2.pack()
                        else:
                            messagebox.showerror("Incorrect Password", "Please verify your password.")
                            password_field2.delete(0, END)
                            return
                    else:
                        messagebox.showerror("Incorrect Username", "This username does not exist, register if you do not already own an account.")               
                        username_field2.delete(0, END)
                        return
                        
                
                empty_label2 = Label(self.login_menu, text='',pady=10)
                empty_label2.pack()
                    
                login_button = Button(self.login_menu, text='Login', font=('Cambria', self.title_font_size), padx= 20, pady= 10, command=login_user)
                login_button.pack()
                self.login_widgets = [password_field2, password_label2, username_field2, username_label2, register_label2, login_button, empty_label2, success_label2]
            else:
                for widget in self.login_widgets:
                    widget.pack_forget()
                self.login_menu.pack()
                success_label2['text'] = f'Welcome {self.username}! Logged in Successfully! You can link a face database to your account!'
                success_label2.pack()
                self.login_widgets = [success_label2]
                
                    
        
        def delete_all_faces():
            if self.logged_in:
                for filename in os.listdir('users/'+ self.username):
                    file_path = os.path.join('users/'+ self.username, filename)
                    if '.png' in filename :
                        try:
                            if os.path.isfile(file_path) or os.path.islink(file_path):
                                os.unlink(file_path) 
                        except Exception as e:
                            messagebox.showerror('Error!', f'Reason {e}')
                            return
                messagebox.showinfo("Success", "Data Deleted Successfully.")
            else:
                messagebox.showinfo("Not Logged In", "The temp file will be emptied.")
                for filename in os.listdir('temp'):
                    file_path = os.path.join('temp', filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path) 
                    except Exception as e:
                        messagebox.showerror('Error!', f'Reason {e}')
                        return        
                messagebox.showinfo("Success", "Data Deleted Successfully.")
        
        def help_documentation():
            help_file_path = 'help.pdf'
            os.system(help_file_path)
        
        def face_detection_menu():
            clean_menus()
            self.face_detection_menu.pack()
        
        self.system_cascade_top_menu = Menu(self.top_menu, tearoff=0)
        self.top_menu.add_cascade(label='Command', menu=self.system_cascade_top_menu)
        self.system_cascade_top_menu.add_command(label='Add Face', command=face_detection_menu)
        self.system_cascade_top_menu.add_command(label='Delete data', command=delete_all_faces)
        
        self.system_cascade_top_menu.add_separator()
        self.system_cascade_top_menu.add_command(label='Register', command=register_menu)
        self.system_cascade_top_menu.add_command(label='Login', command=login_menu)
        self.system_cascade_top_menu.add_command(label='Help', command=help_documentation)
        
        self.system_cascade_top_menu.add_separator()
        self.system_cascade_top_menu.add_command(label='Exit', command=self.root.quit)
        
        # Run
        self.root.mainloop()


def empty_dir(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == "__main__":
    try:
        os.mkdir('users/')
        os.mkdir('temp')
    except FileExistsError:
        pass
    p = GUIfaceRecoginitionBasedSystem()
    empty_dir('temp')