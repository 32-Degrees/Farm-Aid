import time
import mysql.connector as sql
import webbrowser
from customtkinter import *
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox
from sklearn.linear_model import LinearRegression

def HOME():
    if 'resource_view' in globals():
        resource_view.pack_forget()
    if 'land_view' in globals():
        land_view.pack_forget()
    if 'forecast_view' in globals():
        forecast_view.pack_forget()
    if 'weather_frame' in globals():
        weather_frame.pack_forget()
    if 'soil_frame' in globals():
        soil_frame.pack_forget()
    if 'soil_management_frame' in globals():
        soil_management_frame.pack_forget()
    if 'new_grain_frame' in globals():
        new_grain_frame.pack_forget()
    if 'grain_frame' in globals():
        grain_frame.pack_forget()
    if 'cold_storage_frame' in globals():
        cold_storage_frame.pack_forget()


    main_page()
def quit_program():
    cursor.close()
    connection.close()
    app.destroy()



connection = sql.connect(
    user="root",
    password="<your password>",
    host="localhost",
    database="<your db>"
)

cursor = connection.cursor()

app = CTk()
app.geometry("600x480")
app.title("Farm-Aid by THE Z.U.C.C.S")
app.resizable(0, 0)


def land_management():
    main_view.pack_forget()
    global land_view
    land_view = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
    land_view.pack_propagate(0)
    land_view.pack(expand=True, side="right")

    def fetch_crops():
        try:
            land_area = float(entry_land_area.get())
            soil_id = int(entry_soil_id.get())
            min_capital = float(entry_min_capital.get())

            query = f"""
            SELECT grain_details.grain_id, grain_details.grain_name, grain_details.minimum_capital, soil_conditions.soil_name, pesticides.pesticide_name, pesticides.application_method, pesticides.toxicity_level, pesticides.recommended_dosage, soil_conditions.organic_content 
            FROM grain_details, soil_conditions, pesticides
            WHERE grain_details.soil_id = soil_conditions.soil_id AND grain_details.pesticide_id = pesticides.pesticide_id AND grain_details.land_area_required <= %s AND grain_details.soil_id = %s AND grain_details.minimum_capital <= %s;
            """

            cursor.execute(query, (land_area, soil_id, min_capital))
            results = cursor.fetchall()
            columns = [i[0] for i in cursor.description]
            df = pd.DataFrame(results, columns=columns)
            print(df)

            if results:
                crops = [result[0] for result in results]
                messagebox.showinfo("Suitable Crops", f"Crops you can plant: {', '.join(crops)}")


        except Exception as e:
            messagebox.showerror("Error", str(e))

    label_land_area = CTkLabel(land_view, text="Enter Land Area (in acres):",text_color="#ec7a00", anchor="w", justify="left", font=("Arial Bold", 14), compound="left")
    label_land_area.pack(anchor="w", pady=(21, 0), padx=(25, 0))
    entry_land_area = CTkEntry(land_view,placeholder_text="land are", width=225, fg_color="#EEEEEE", border_color="#ec7a00", border_width=1, text_color="#000000",)
    entry_land_area.pack(anchor="w", padx=(25, 0))

    entry_soil_id = CTkEntry(master=land_view, width=225,placeholder_text="soil id", fg_color="#EEEEEE", border_color="#ec7a00", border_width=1, text_color="#000000",)
    entry_soil_id.pack(anchor="w", padx=(25, 0))
    entry_min_capital = CTkEntry(master=land_view,placeholder_text="min capital", width=225, fg_color="#EEEEEE", border_color="#ec7a00", border_width=1, text_color="#000000",)
    entry_min_capital.pack(anchor="w", padx=(25, 0))
    fetch_button = CTkButton(land_view, text="Fetch Crops", fg_color="#ec7a00", hover_color="#ec0000", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=fetch_crops)
    fetch_button.pack(anchor="w", padx=(25, 0))
    CTkButton(master=land_view, text="HOME", fg_color="transparent", hover_color="#ec0000",
              font=("Arial Bold", 8), text_color="black", width=8, border_width=2,
              border_color='black', corner_radius=32, command=HOME).pack(
        anchor="se", pady=(30, 20), padx=(0, 50))
def market_forecast():
    main_view.pack_forget()
    global forecast_view
    forecast_view = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
    forecast_view.pack_propagate(0)
    forecast_view.pack(expand=True, side="right")
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
        new_x = pd.date_range(start=data_file['Date'].max(), periods=1 * 12, freq='M')
        new_x_ordinal = new_x.map(pd.Timestamp.toordinal).values.reshape(-1, 1)
        new_y = regression.predict(new_x_ordinal)
        plt.plot(new_x, new_y, color='red')
        plt.show()

    def market_choice():
        global mk_choice
        mk_choice = crop_choice.get()
        if mk_choice:
            open_data_files(mk_choice)


    CTkLabel(master=forecast_view, text="Projection", text_color="#ec7a00", anchor="w", justify="left",
             font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))

    crop_choice = CTkComboBox(master=forecast_view, values=["soybean", "wheat", "corn","barley"], font=("Arial Bold", 12),
                              text_color="#ffffff",
                              width=225)
    crop_choice.pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkButton(master=forecast_view, text="Show Graph", fg_color="#ec7a00", hover_color="#ec0000", font=("Arial Bold", 12),
              text_color="#ffffff", width=225, command=market_choice).pack(anchor="w", pady=(40, 0), padx=(25, 0))
    CTkButton(master=forecast_view, text="HOME", fg_color="transparent", hover_color="#ec0000",
              font=("Arial Bold", 8), text_color="black", width=8, border_width=2,
              border_color='black', corner_radius=32, command=HOME).pack(
        anchor="se", pady=(30, 20), padx=(0, 50))
def open_windy_weather():
    main_view.pack_forget()
    global weather_frame
    weather_frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
    weather_frame.pack_propagate(0)
    weather_frame.pack(expand=True,side="right")

    def check_weather():
        city = city_entry.get()
        webbrowser.open_new_tab(f"https://www.windy.com/?{city.replace(' ', '%20')}&lang=en")

    CTkLabel(master=weather_frame, text="Enter Your City Name", text_color="#ec7a00", anchor="w", justify="left",
             font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    city_entry = CTkEntry(master=weather_frame, width=225, fg_color="#EEEEEE", border_color="#ec7a00", border_width=1,
                          text_color="#000000", placeholder_text="New York")
    city_entry.pack(anchor="w", pady=(40, 0), padx=(25, 0))
    CTkButton(master=weather_frame, text="Submit", fg_color="#ec7a00", hover_color="#ec0000", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=check_weather).pack(anchor="w", pady=(40, 0), padx=(25, 0))
    CTkButton(master=weather_frame, text="HOME", fg_color="transparent", hover_color="#ec0000",
              font=("Arial Bold", 8), text_color="black", width=8, border_width=2,
              border_color='black', corner_radius=32, command=HOME).pack(
        anchor="se", pady=(30, 20), padx=(0, 50))

def soil_track():
    main_view.pack_forget()
    global soil_frame
    soil_frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
    soil_frame.pack_propagate(0)
    soil_frame.pack(expand=True, side="right")
    def view_soil():
        q1 = 'SELECT * FROM soil_conditions;'
        cursor.execute(q1)
        r1 = cursor.fetchall()
        print("{SOIL_ID},{SOIL_NAME},{PH_LEVEL},{MOISTURE_LEVEL},{ORGANIC_CONTENT},{CROP_RECOMMENDATION}")
        time.sleep(1.5)
        for i in r1:
            print(i)
            time.sleep(0.5)

    def soil_management():
        soil_frame.pack_forget()
        global soil_management_frame
        soil_management_frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
        soil_management_frame.pack_propagate(0)
        soil_management_frame.pack(expand=True, side="right")
        def search_soil():
            soil_entry_1 = soil_entry.get()
            q = f"SELECT soil_conditions.soil_name, soil_conditions.ph_level, soil_conditions.moisture_level, soil_conditions.organic_content, grain_details.grain_id, grain_details.grain_name, pesticides.pesticide_name, pesticides.recommended_dosage FROM grain_details JOIN soil_conditions ON soil_conditions.soil_id = grain_details.soil_id JOIN pesticides ON grain_details.pesticide_id = pesticides.pesticide_id WHERE soil_conditions.soil_id='{soil_entry_1}';"
            cursor.execute(q)
            results = cursor.fetchall()

            for widget in soil_management_frame.winfo_children():
                if isinstance(widget, CTkLabel) and "Result:" in widget.cget("text"):
                    widget.destroy()

            if results:
                for row in results:
                    result_text = f"(ID,NAME,MIN CAP,SOIL,PEST_ID)\nResult: {row}"
                    CTkLabel(master=soil_management_frame, text=result_text, text_color="black").pack(anchor="w", pady=5,
                                                                                                   padx=(25, 0))
            else:
                CTkLabel(master=soil_management_frame, text="No results found.", text_color="red").pack(
                    anchor="w", pady=5, padx=(25, 0))


        CTkLabel(master=soil_management_frame, text="Soil Management", text_color="#ec7a00", anchor="w", justify="left",
                 font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
        soil_entry = CTkEntry(master=soil_management_frame, width=225, fg_color="#EEEEEE", border_color="#ec7a00",
                                   border_width=1, text_color="#000000", placeholder_text="1001")
        soil_entry.pack(anchor="w", padx=(25, 0))
        button52 = CTkButton(master=soil_management_frame, text="search", fg_color="#ec7a00", hover_color="#ec0000",
                             font=("Arial Bold", 12), text_color="#ffffff", width=225, command=search_soil)
        button52.pack(pady=12, padx=10)
        CTkButton(master=soil_management_frame, text="HOME", fg_color="transparent", hover_color="#ec0000",
                  font=("Arial Bold", 8), text_color="black", width=8, border_width=2,
                  border_color='black', corner_radius=32, command=HOME).pack(
            anchor="se", pady=(0, 20), padx=(0, 20))



    CTkLabel(master=soil_frame, text="Soil Database", text_color="#ec7a00", anchor="w", justify="left",
             font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    button11 = CTkButton(master=soil_frame, text="View Soil Conditions Table", fg_color="#ec7a00", hover_color="#ec0000",
                         font=("Arial Bold", 12), text_color="#ffffff", width=225,command=view_soil)
    button11.pack(pady=12, padx=10)
    button22 = CTkButton(master=soil_frame, text="Soil Id search", fg_color="#ec7a00", hover_color="#ec0000",
                         font=("Arial Bold", 12), text_color="#ffffff", width=225,command=soil_management)
    button22.pack(pady=12, padx=10)
    CTkButton(master=soil_frame, text="HOME", fg_color="transparent", hover_color="#ec0000",
              font=("Arial Bold", 8), text_color="black", width=8, border_width=2,
              border_color='black', corner_radius=32, command=HOME).pack(
        anchor="se", pady=(0, 20), padx=(0, 20))


def resource_mangement_details():
    main_view.pack_forget()
    global resource_view
    resource_view = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
    resource_view.pack_propagate(0)
    resource_view.pack(expand=True, side="right")
    def cold_storage():
        def cold_search():
            storage_name = storage_by_name.get().lower()
            try:
                q = f"SELECT * FROM cold_storages WHERE location = '{storage_name}';"
                cursor.execute(q)
                results = cursor.fetchall()

                for widget in cold_storage_frame.winfo_children():
                    if isinstance(widget, CTkLabel) and "Result:" in widget.cget("text"):
                        widget.destroy()

                if results:
                    for row in results:
                        result_text = f"(ID,NAME,MIN CAP,SOIL,PEST_ID)\nResult: {row}"
                        CTkLabel(master=cold_storage_frame, text=result_text, text_color="black").pack(anchor="w", pady=5,
                                                                                                    padx=(25, 0))
                else:
                    CTkLabel(master=cold_storage_frame, text="No results found.", text_color="red").pack(
                        anchor="w", pady=5, padx=(25, 0))

            except sql.Error as err:
                CTkLabel(master=cold_storage_frame, text=f"Error: {err}", text_color="red").pack(anchor="w",
                                                                                              pady=5,
                                                                                              padx=(25, 0))

        resource_view.pack_forget()
        global cold_storage_frame
        cold_storage_frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
        cold_storage_frame.pack_propagate(0)
        cold_storage_frame.pack(expand=True, side="right")
        CTkLabel(master=cold_storage_frame, text="Search By Name", text_color="#ec7a00", anchor="w", justify="left",
                 font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
        storage_by_name = CTkEntry(master=cold_storage_frame, width=225, fg_color="#EEEEEE", border_color="#ec7a00",
                                 border_width=1, text_color="#000000", placeholder_text="Chennai")
        storage_by_name.pack(anchor="w", padx=(25, 0))

        CTkButton(master=cold_storage_frame, text="Search", fg_color="#ec7a00", hover_color="#ec0000",
                  font=("Arial Bold", 12), text_color="#ffffff", width=225, command=cold_search).pack(anchor="w",
                                                                                               pady=(40, 0),
                                                                                                 padx=(25, 0))
        CTkButton(master=cold_storage_frame, text="HOME", fg_color="transparent", hover_color="#ec0000",
                  font=("Arial Bold", 8), text_color="black", width=8, border_width=2,
                  border_color='black', corner_radius=32, command=HOME).pack(
            anchor="se", pady=(0, 20), padx=(0, 20))


    def grain_details():
        resource_view.pack_forget()
        global grain_frame
        grain_frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
        grain_frame.pack_propagate(0)
        grain_frame.pack(expand=True, side="right")

        def options(choice):
            grain_frame.pack_forget()
            global new_grain_frame
            new_grain_frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
            new_grain_frame.pack_propagate(0)
            new_grain_frame.pack(expand=True, side="right")

            if choice == "Name":
                CTkLabel(master=new_grain_frame, text="Search By Name", text_color="#ec7a00", anchor="w", justify="left",
                         font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
                grain_by_name = CTkEntry(master=new_grain_frame, width=225, fg_color="#EEEEEE", border_color="#ec7a00",
                                         border_width=1, text_color="#000000", placeholder_text="Ex: Wheat")
                grain_by_name.pack(anchor="w", padx=(25, 0))

                def search():
                    search_by_name = grain_by_name.get()

                    try:
                        q = f"SELECT * FROM grain_details WHERE grain_name = '{search_by_name}';"
                        cursor.execute(q)
                        results = cursor.fetchall()

                        for widget in new_grain_frame.winfo_children():
                            if isinstance(widget, CTkLabel) and "Result:" in widget.cget("text"):
                                widget.destroy()

                        if results:
                            for row in results:
                                result_text = f"(ID,NAME,MIN CAP,SOIL,PEST_ID)\nResult: {row}"
                                CTkLabel(master=new_grain_frame, text=result_text, text_color="black").pack(anchor="w",pady=5,padx=(25, 0))
                        else:
                            CTkLabel(master=new_grain_frame, text="No results found.", text_color="red").pack(
                                anchor="w", pady=5, padx=(25, 0))

                    except sql.Error as err:
                        CTkLabel(master=new_grain_frame, text=f"Error: {err}", text_color="red").pack(anchor="w",
                                                                                                      pady=5,
                                                                                                      padx=(25, 0))

                CTkButton(master=new_grain_frame, text="Search", fg_color="#ec7a00", hover_color="#ec0000",
                          font=("Arial Bold", 12), text_color="#ffffff", width=225, command=search).pack(anchor="w",
                                                                                                         pady=(40, 0),
                                                                                                         padx=(25, 0))
                CTkButton(master=new_grain_frame, text="HOME", fg_color="transparent", hover_color="#ec0000",
                          font=("Arial Bold", 8), text_color="black", width=8, border_width=2,
                          border_color='black', corner_radius=32, command=HOME).pack(
                    anchor="se", pady=(0, 20), padx=(0, 20))

            elif choice == "Capital":
                CTkLabel(master=new_grain_frame, text="Search By Capital", text_color="#ec7a00", anchor="w",
                         justify="left",
                         font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
                min_cap = CTkEntry(master=new_grain_frame, width=225, fg_color="#EEEEEE", border_color="#ec7a00",
                                   border_width=1, text_color="#000000", placeholder_text="Min Capital Value")
                min_cap.pack(anchor="w", padx=(25, 0))
                max_cap = CTkEntry(master=new_grain_frame, width=225, fg_color="#EEEEEE", border_color="#ec7a00",
                                   border_width=1, text_color="#000000", placeholder_text="Max Capital Value")
                max_cap.pack(anchor="w", padx=(25, 0))

                def search2():
                    min_value = float(min_cap.get())
                    max_value = float(max_cap.get())

                    try:
                        q2 = f"SELECT * FROM grain_details WHERE minimum_capital BETWEEN '{min_value}' AND '{max_value}';"
                        cursor.execute(q2)
                        results = cursor.fetchall()

                        for widget in new_grain_frame.winfo_children():
                            if isinstance(widget, CTkLabel) and "Result:" in widget.cget("text"):
                                widget.destroy()

                        if results:
                            for row in results:
                                result_text = f"(ID,NAME,MIN CAP,SOIL,PEST_ID)\nResult: {row}"
                                CTkLabel(master=new_grain_frame, text=result_text, text_color="black").pack(anchor="w",
                                                                                                            pady=5,
                                                                                                            padx=(
                                                                                                            25, 0))
                        else:
                            CTkLabel(master=new_grain_frame, text="No results found.", text_color="red").pack(
                                anchor="w", pady=5, padx=(25, 0))

                    except sql.Error as err:
                        CTkLabel(master=new_grain_frame, text=f"Error: {err}", text_color="red").pack(anchor="w",
                                                                                                      pady=5,
                                                                                                      padx=(25, 0))

                CTkButton(master=new_grain_frame, text="Search", fg_color="#ec7a00", hover_color="#ec0000",
                          font=("Arial Bold", 12), text_color="#ffffff", width=225, command=search2).pack(anchor="w",
                                                                                                          pady=(40, 0),
                                                                                                          padx=(25, 0))
                CTkButton(master=new_grain_frame, text="HOME", fg_color="transparent", hover_color="#ec0000",
                          font=("Arial Bold", 8), text_color="black", width=8, border_width=2,
                          border_color='black', corner_radius=32, command=HOME).pack(
                    anchor="se", pady=(0, 20), padx=(0, 20))


        CTkLabel(master=grain_frame, text="Search By?", text_color="#ec7a00", anchor="w", justify="left",
                 font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
        choice_box = CTkComboBox(master=grain_frame, values=["Capital", "Name"], font=("Arial Bold", 12),
                                 text_color="#ffffff",
                                 width=225, command=options)
        choice_box.pack(pady=12, padx=10)
        CTkButton(master=grain_frame, text="HOME", fg_color="transparent", hover_color="#ec0000",
                  font=("Arial Bold", 8), text_color="black", width=8, border_width=2,
                  border_color='black', corner_radius=32, command=HOME).pack(
            anchor="se", pady=(0, 20), padx=(0, 20))



    CTkLabel(master=resource_view, text="Available Resources", text_color="#ec7a00", anchor="w", justify="left",
             font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    button21 = CTkButton(master=resource_view, text="Cold Storage Table", fg_color="#ec7a00",
                         hover_color="#ec0000",
                         font=("Arial Bold", 12), text_color="#ffffff", width=225, command=cold_storage)
    button21.pack(pady=12, padx=10)
    button22 = CTkButton(master=resource_view, text="Grain Details Table", fg_color="#ec7a00",
                         hover_color="#ec0000",
                         font=("Arial Bold", 12), text_color="#ffffff", width=225, command=grain_details)
    button22.pack(pady=12, padx=10)
    CTkButton(master=resource_view, text="HOME", fg_color="transparent", hover_color="#ec0000",
              font=("Arial Bold", 8), text_color="black", width=8, border_width=2,
              border_color='black', corner_radius=32, command=HOME).pack(
        anchor="se", pady=(0, 20), padx=(0, 20))

def main_page():
    if 'frame' in globals():
        frame.pack_forget()

    if 'sign_up_frame' in globals():
        sign_up_frame.pack_forget()

    global main_view
    main_view = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
    main_view.pack_propagate(0)
    main_view.pack(expand=True, side="right")

    CTkLabel(master=main_view, text="Main Menu", text_color="#ec7a00", anchor="w", justify="left",
             font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    button01 = CTkButton(master=main_view, text="Resource Management",fg_color="#ec7a00", hover_color="#ec0000", font=("Arial Bold", 12), text_color="#ffffff", width=225,command=resource_mangement_details)
    button01.pack(pady=12, padx=10)
    button02 = CTkButton(master=main_view, text="Land Management",fg_color="#ec7a00", hover_color="#ec0000", font=("Arial Bold", 12), text_color="#ffffff", width=225,command=land_management)
    button02.pack(pady=12, padx=10)
    button03 = CTkButton(master=main_view, text="View Market",fg_color="#ec7a00", hover_color="#ec0000", font=("Arial Bold", 12), text_color="#ffffff", width=225,command=market_forecast)
    button03.pack(pady=12, padx=10)
    button04 = CTkButton(master=main_view, text="Soil Tracking",fg_color="#ec7a00", hover_color="#ec0000", font=("Arial Bold", 12), text_color="#ffffff", width=225,command=soil_track)
    button04.pack(pady=12, padx=10)
    button05 = CTkButton(master=main_view, text="Weather Tracking",fg_color="#ec7a00", hover_color="#ec0000", font=("Arial Bold", 12), text_color="#ffffff", width=225,command=open_windy_weather)
    button05.pack(pady=12, padx=10)
    CTkButton(master=main_view, text="Quit", fg_color="transparent", hover_color="#ec0000",
              font=("Arial Bold", 8), text_color="black", width=8 ,border_width=2,
              border_color='black', corner_radius=32, command=quit_program).pack(
            anchor="se", pady=(0, 20), padx=(0, 20))


users = {"deepan": 911, "harsha": 9624, "ishana": 3378,"nikhel":42069,"sam":9}


def sign_up():
    frame.pack_forget()
    global sign_up_frame
    sign_up_frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
    sign_up_frame.pack_propagate(0)
    sign_up_frame.pack(expand=True, side="right")
    CTkLabel(master=sign_up_frame, text="Create your\n"
                                        "Farm-Aid account", text_color="#ec7a00", anchor="w", justify="left",
             font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkLabel(master=sign_up_frame, text="Enter your details", text_color="#7E7E7E", anchor="w", justify="left",
             font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))
    CTkLabel(master=sign_up_frame, text="  Username:", text_color="#ec7a00", anchor="w", justify="left",
             font=("Arial Bold", 14), image=user_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
    entry_name1 = CTkEntry(master=sign_up_frame, width=225, fg_color="#EEEEEE", border_color="#ec7a00", border_width=1,
                          text_color="#000000", placeholder_text="Ex: Sam Jaguar Jackson 💀🔥🚨")
    entry_name1.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=sign_up_frame, text="  Password:", text_color="#ec7a00", anchor="w", justify="left",
             font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    entry_pas2 = CTkEntry(master=sign_up_frame, width=225, fg_color="#EEEEEE", border_color="#ec7a00", border_width=1,
                         text_color="#000000", show="*", placeholder_text="ex: sam123")
    entry_pas2.pack(anchor="w", padx=(25, 0))
    new_user = entry_name1.get()
    new_user_pas = entry_pas2.get()
    users[new_user] = new_user_pas
    CTkButton(master=sign_up_frame, text="Sign Up", fg_color="#ec7a00", hover_color="#ec0000", font=("Arial Bold", 12),
              text_color="#ffffff", width=225, command=main_page).pack(anchor="w", pady=(25, 0), padx=(25, 0))
    CTkButton(master=sign_up_frame, text="Quit", fg_color="transparent", hover_color="#ec0000",
              font=("Arial Bold", 8), text_color="black", width=8, border_width=2,
              border_color='black', corner_radius=32, command=quit_program).pack(
        anchor="se", pady=(30, 20), padx=(0, 50))
def login():
    global users
    user_name = entry_name.get().lower()
    user_pass = entry_pas.get()

    if user_name not in users:
        login_message.configure(text="Invalid user, please try again.", text_color="red")
    else:
        try:
            if int(user_pass) == users[user_name]:
                login_message.configure(text="Logged IN", text_color="green")
                main_page()
            else:
                login_message.configure(text="Invalid passcode, please try again.", text_color="red")
        except ValueError:
            login_message.configure(text="Passcode must be a number.", text_color="red")


side_img_data = Image.open("sunset.jpg")
email_icon_data = Image.open("email-icon.png")
password_icon_data = Image.open("password-icon.png")

side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
user_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))

CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

CTkLabel(master=frame, text="Welcome Back!", text_color="#ec7a00", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
CTkLabel(master=frame, text="Sign into your Farm-Aid Database. ", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Username:", text_color="#ec7a00", anchor="w", justify="left", font=("Arial Bold", 14), image=user_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
entry_name = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#ec7a00", border_width=1, text_color="#000000", placeholder_text="Ex: Sam Jaguar Jackson 💀🔥🚨")
entry_name.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Password:", text_color="#ec7a00", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
entry_pas = CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#ec7a00", border_width=1, text_color="#000000", show="*", placeholder_text="ex: sam123")
entry_pas.pack(anchor="w", padx=(25, 0))

login_message = CTkLabel(master=frame, text="", text_color="red", anchor="w", justify="left", font=("Arial Bold", 12))
login_message.pack(anchor="w", pady=(10, 0), padx=(25, 0))

CTkButton(master=frame, text="Login", fg_color="#ec7a00", hover_color="#ec0000", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=login).pack(anchor="w", pady=(25, 0), padx=(25, 0))
CTkButton(master=frame, text="new user? Sign up!", fg_color="#ec7a00", hover_color="#ec0000", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=sign_up).pack(anchor="w", pady=(5, 0), padx=(25, 0))
CTkButton(master=frame, text="Quit", fg_color="transparent", hover_color="#ec0000",
              font=("Arial Bold", 8), text_color="black", width=8 ,border_width=2,
              border_color='black', corner_radius=32, command=quit_program).pack(
            anchor="se", pady=(30, 20), padx=(0, 50))
#cursor.close()
#connection.close()
app.mainloop()


#credits: K.S.HARSHAVARHDNAN AND S.DEEPAN SAI 🫂(POWER OF FRIENDSHIP) NATPU THAN SOTHU NAMAKU MAMAE
