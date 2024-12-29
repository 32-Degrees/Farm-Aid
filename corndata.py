import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from customtkinter import *
from PIL import Image

def open_data_files(mk_choice):
    file_mk = pd.read_csv(f"{mk_choice}_data.csv")
    print("success")
    print("Graph PROJECTION")
    data_file = file_mk
    print(data_file)

    data_file['Date'] = pd.to_datetime(data_file['Date'])
    data_file['Price'] = data_file['Price']
    plt.xlabel('Date', fontsize=10)
    plt.ylabel('Price', fontsize=10)
    plt.plot(data_file['Date'], data_file['Price'], color="#78ff01")

    data_file['Date_Ord'] = data_file['Date'].map(pd.Timestamp.toordinal)
    X = data_file['Date_Ord'].values.reshape(-1, 1)
    Y = data_file['Price'].values.reshape(-1, 1)
    regression = LinearRegression()
    regression.fit(X, Y)

    new_x = pd.date_range(start=data_file['Date'].max(), periods=1 * 12 , freq='M')
    new_x_ordinal = new_x.map(pd.Timestamp.toordinal).values.reshape(-1, 1)
    new_y = regression.predict(new_x_ordinal)
    plt.plot(new_x, new_y, color='red')
    plt.show()

def market_choice():
    global mk_choice
    mk_choice = crop_choice.get()
    if mk_choice:
        open_data_files(mk_choice)

app = CTk()
app.geometry("600x480")
app.title("Farm-Aid")
app.resizable(0, 0)

side_img_data = Image.open("sunset.jpg")
side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

CTkLabel(master=frame, text="Projection", text_color="#ec7a00", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))

crop_choice = CTkComboBox(master=frame, values=["soybean", "wheat", "corn"], font=("Arial Bold", 12),
                                 text_color="#ffffff", width=225)
crop_choice.pack(pady=12, padx=10)

CTkButton(master=frame, text="Show Graph", fg_color="#ec7a00", hover_color="#ec0000", font=("Arial Bold", 12),
          text_color="#ffffff", width=225, command=market_choice).pack(anchor="w", pady=(40, 0), padx=(25, 0))

app.mainloop()
