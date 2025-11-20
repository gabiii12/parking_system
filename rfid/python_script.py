import serial
import time
import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk, ImageFile
from io import BytesIO
from database import db
ImageFile.LOAD_TRUNCATED_IMAGES = True
from insert_data import attendance
port = 'COM3'
baud = 9600

print("Change 1")
print("Change 1")

print("Change 1")

class RFID:
    def __init__(self):
        self.student_id = ""
        self.tag_id = ""
        self.student_name = None  
        self.year_level = ""
        self.course = ""
        self.label_id = ""
        self.student_img = ""
        self.prof_type = None
        self.arduino = None
        self.date_time = datetime.now()
        self.formatted_dt = self.date_time.strftime("%Y-%m-%d %H:%M:%S")
        self.color_bg = "#13491B"
        self.att = attendance()
        self.db = db()
        self.cursor = self.db.cursor

        try:
            self.arduino = serial.Serial(port,baud,timeout=1)
            time.sleep(2)
            print("Arduino is connected!")
        except Exception as e:
            print(f"Error: {e}")

        # FOR THE INTERFACE
        self.window = tk.Tk()
        self.window.title("STUDENT INFORMATION (OUR LADY OF FATIMA UNIVERSITY)")
        self.window.config(bg=self.color_bg)
        self.window.geometry("680x350")
        self.header_label = tk.Label(self.window, text="STUDENT INFORMATION", font=("Arial", 12, "bold"), bg=self.color_bg, fg="white")
        self.header_label.pack(pady=10)
        self.icon = tk.PhotoImage(file="F:\\python_projects\\rfid\\images\\olfu.png")
        self.window.iconphoto(False, self.icon)
         # GROUPING
        self.student_info_frame = tk.Frame(self.window, bg =self.color_bg,width=1000, height=250)
        self.student_info_frame.pack()
        self.student_info_frame.pack_propagate(False)
        # FOR ID
        self.label_id = tk.Label(self.student_info_frame,text="Student ID: ", font=("Arial", 12, "bold"), bg =self.color_bg, fg="white")
        self.label_id_value = tk.Label(self.student_info_frame, text="--", font=("Arial", 12), bg=self.color_bg, fg="white")
        self.label_id.grid(row=0,column=0,sticky="w",padx=10,pady=5)
        self.label_id_value.grid(row=0,column=1,sticky="w",padx=10,pady=5)
        # FOR NAME 
        self.label_name = tk.Label(self.student_info_frame,text="Student Name: ", font=("Arial", 12, "bold"), bg =self.color_bg, fg="white")
        self.frame_name = tk.Label(self.student_info_frame, text="--", font=("Arial", 12), bg=self.color_bg, fg="white")
        self.label_name.grid(row=1,column=0,sticky="w",padx=10,pady=5)
        self.frame_name.grid(row=1,column=1,sticky="w",padx=10,pady=5)
        # FOR YEAR LEVEL
        self.label_name = tk.Label(self.student_info_frame,text="Year Level: ", font=("Arial", 12, "bold"), bg =self.color_bg, fg="white")
        self.frame_lvl = tk.Label(self.student_info_frame, text="--", font=("Arial", 12), bg=self.color_bg, fg="white")
        self.label_name.grid(row=2,column=0,sticky="w",padx=10,pady=5)
        self.frame_lvl.grid(row=2,column=1,sticky="w",padx=10,pady=5)
        # FOR COURSE
        self.label_name = tk.Label(self.student_info_frame,text="Course: ", font=("Arial", 12, "bold"), bg =self.color_bg, fg="white")
        self.frame_crs = tk.Label(self.student_info_frame, text="--", font=("Arial", 12), bg=self.color_bg, fg="white")
        self.label_name.grid(row=3,column=0,sticky="w",padx=10,pady=5)
        self.frame_crs.grid(row=3,column=1,sticky="w",padx=10,pady=5)
        # FOR date and time
        self.label_name = tk.Label(self.student_info_frame,text="Date and time: ", font=("Arial", 12, "bold", ), bg =self.color_bg, fg="white")
        self.frame_dt = tk.Label(self.student_info_frame, text="--", font=("Arial", 12), bg=self.color_bg, fg="white")
        self.label_name.grid(row=4,column=0,sticky="w",padx=10,pady=5)
        self.frame_dt.grid(row=4,column=1,sticky="w",padx=10,pady=5)
        # FOR profile_type
        self.label_prof = tk.Label(self.student_info_frame,text="Profile type: ", font=("Arial", 12, "bold", ), bg =self.color_bg, fg="white")
        self.prof_t = tk.Label(self.student_info_frame, text="--", font=("Arial", 12), bg=self.color_bg, fg="white")
        self.label_prof.grid(row=5,column=0,sticky="w",padx=10,pady=5)
        self.prof_t.grid(row=5,column=1,sticky="w",padx=10,pady=5)
        # FOR IMAGE 
        self.image_frame = tk.Frame(self.student_info_frame, bg="white", width=150, height=150)
        self.image_frame.grid(row=0, column=2, rowspan=5, padx=10, pady=10)

    def get_image(self):
        self.blob_image = None  

        query = "SELECT img FROM rfid_logs WHERE tag_id = %s"
        self.cursor.execute(query, (self.tag_id,))

        img = self.cursor.fetchone()
        if img and img[0]:
            self.blob_image = img[0]


    def display_pic(self):
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        if self.blob_image:
            image = Image.open(BytesIO(self.blob_image))
            image = image.resize((150, 150))
            photo = ImageTk.PhotoImage(image)

            self.img_label = tk.Label(self.image_frame, image=photo, bg="white")
            self.img_label.image = photo  # keep reference alive
            self.img_label.pack(padx=10, pady=10)
        else:
            self.img_label = tk.Label(self.image_frame,text="No Image",font=("Arial", 10),bg="white",width=18,height=9)
            self.img_label.image = None  
            self.img_label.pack(padx=10, pady=10)


    def interface(self, row_tk):
        if not row_tk:
            self.label_id_value.config(text="No data", font=("Arial", 12))
            self.frame_name.config(text="No data", font=("Arial", 12))
            self.frame_lvl.config(text="No data", font=("Arial", 12))
            self.frame_crs.config(text="No data", font=("Arial", 12))
            self.frame_dt.config(text="No data", font=("Arial", 12))
            self.prof_t.config(text="No data", font=("Arial", 12))
        else:
            self.student_id, self.student_name, self.year_level, self.course,self.prof_type = row_tk
            self.label_id_value.config(text=f"{self.student_id}", font=("Arial", 12))
            self.frame_name.config(text=f"{self.student_name}", font=("Arial", 12))
            self.frame_lvl.config(text=f"{self.year_level}", font=("Arial", 12))
            self.frame_crs.config(text=f"{self.course}", font=("Arial", 12))
            self.prof_t.config(text=f"{self.prof_type}", font=("Arial", 12))
        

    def practice(self):
        query = "SELECT student_id,student_name,year_level,course, profile_type FROM rfid_logs WHERE tag_id = %s"
        self.cursor.execute(query, (self.tag_id,))
        row = self.cursor.fetchone()
        if row:
            self.student_id, self.student_name, self.year_level, self.course, self.prof_type = row
            print(f"Student id: {self.student_id} ")
            print(f"Name: {self.student_name} ")
            print(f"Year Level: {self.year_level} ")
            print(f"Course: {self.course} ")
            self.interface(row)
            self.get_image()
            self.display_pic()
            self.att.insert_data(self.tag_id,self.student_id,self.student_name)
        else:
            print("No Record found!")
            self.interface(None)
            self.blob_image = None
            self.display_pic()

    def read_from_arduino(self):
        if self.arduino:
            line = self.arduino.readline().decode('utf-8').strip()
            if line:
                print(f"RFID tag: {line}")
                self.tag_id = line
                self.practice()

        self.window.after(200, self.read_from_arduino)

    def main(self):
        self.read_from_arduino()
        self.window.mainloop()   


if __name__ == "__main__":
    rfid = RFID()
    rfid.main()
