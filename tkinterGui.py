from Tkinter import *
from PIL import ImageTk, Image
import datetime
import math
import radarLogic
from threading import Thread


class GUI(Canvas):

    def __init__(self, master):
        self.root = master
        self.canvas = Canvas(master, width=600, height=600)
        self.canvas.pack(fill=BOTH, expand=1)
        self.img = ImageTk.PhotoImage(Image.open("radar.jpg"))  # PIL solution
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.lab = Label()
        self.lab.pack()
        
        
        ##Hypothenuse = line_Length, winkel ist bekannt, mit kosinus und sinus x_end + y_end berechnen 
        angle_in_degrees = 0
        angle_in_radians = angle_in_degrees * math.pi / 180
        line_length = 550
        center_x = 540
        center_y = 540
        end_x = center_x + line_length * math.cos(angle_in_radians)
        end_y = center_y + line_length * math.sin(angle_in_radians)
        self.line = self.canvas.create_line(center_x, center_y, end_x, end_y, fill="red", width="10")
        self.lines = []
        self.radar = radarLogic.Radar()
        thread = Thread(target = self.radar.run_radar)
        try:
            thread.start()
        except KeyboardInterrupt:
            print "Ctrl+C pressed..."
            sys.exit(1)



    def update_radar(self):
        for line in self.lines:
            self.canvas.delete(line)
        time = datetime.datetime.now().strftime("Time: %H:%M:%S")
        self.lab.config(text=time)
        
        self.canvas.delete(self.line)
        for i in range(0, 10):
            angle_in_degrees = - self.radar.current_angle + i
            angle_in_radians = angle_in_degrees * math.pi / 180
            line_length = 550
            center_x = 540
            center_y = 540
            end_x = center_x + line_length * math.cos(angle_in_radians)
            end_y = center_y + line_length * math.sin(angle_in_radians)
            if self.radar.current_distance < self.radar.distances[self.radar.current_angle] + 0.5 and self.radar.distances[self.radar.current_angle] < 20:
                self.lines.append(self.canvas.create_line(center_x, center_y, end_x, end_y, fill="red", width="10"))
            else:
                self.lines.append(self.canvas.create_line(center_x, center_y, end_x, end_y, fill="green", width="10"))
        #lab['text'] = time
        self.root.after(100, self.update_radar)# run itself again after 1000 ms
        
    def print_update(self):
        print("Current Distance in GUIClass: " + str(self.radar.current_distance))
        print("Current Distance in Dictionary: " + str(self.radar.distances[self.radar.current_angle]))
        self.root.after(1000, self.print_update)# run itself again after 1000 ms

def main():
    try:
        root = Tk()
        root.wm_geometry("1080x1080")
        root.title('Radar')
        gui = GUI(root)
        gui.update_radar()
        gui.print_update()
        root.mainloop()
    except KeyboardInterrupt:
            print "Ctrl+C pressed..."
            sys.exit(1)

if __name__ == "__main__":
    main()