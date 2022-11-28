import pandas as pd
import numpy as np
from datetime import date

from haversine import haversine, Unit
from streamlit_folium import folium_static
import seaborn as sns
from folium import plugins
import folium
import streamlit as st
import HotelAvail as hv
import time
pd.options.mode.chained_assignment = None  # default='warn'
from pathlib import Path



def recommender_system():
    jp = st.text_input("Enter Jp code Pls...(Ex : JPxxxxxx)")
    start_date = str(st.text_input("Enter Start Date Pls...(Ex : 2022-11-25)"))
    end_date = str(st.text_input("Enter End Date Pls...(Ex : 2022-11-26)"))
    nationality = str(st.text_input("Enter Nationality Pls...(Ex : EG)"))
    pax = str(st.text_input("Number of Pax Pls...(Ex : 2)"))

    try:

        search = st.checkbox('Submit', key='submit')
       # try:
        if search:
            current_dir = Path(__file__).parent
            df_path = current_dir/'FullData.csv'
            response_msg=None
            dfX = pd.read_csv(df_path, encoding="ISO-8859-1", low_memory=False)
            df = dfX.copy()

            df['R Lat'] = df['R Lat'].str[:-1].astype(float)
            df['Real Long'] = df['Real Long'].str[:-1].astype(float)
            rawOfData = df[df['JP Code'] == jp].copy().reset_index()
            if rawOfData.shape[0] == 0:
                response_msg = '<p style="font-family:Courier; color:Red; font-size: 20px;">Sorry this JpCode is not identified in our database</p>'
                st.markdown(response_msg, unsafe_allow_html=True)
            else:
                response_msg = None
            prod_JpCodes = []
            hotel_names = []
            hotel_address = []
            latidudes = []
            longtudes = []
            countries = []
            distances = []
            categories = []
            # first filtering
            new_df = df[df['Country'] == rawOfData['Country'][0]].copy()
            new_df = new_df[new_df['Category'] >= rawOfData['Category'][0]].reset_index()
            for j in range(new_df.shape[0]):
                lat = new_df['R Lat'][j]
                long = new_df['Real Long'][j]

                # calculate the distance
                distance = haversine((rawOfData['R Lat'][0], rawOfData['Real Long'][0]), (lat, long))

                # second filtering
                if distance < 10 and distance != 0:
                    prod_JpCodes.append(new_df['JP Code'][j])
                    hotel_names.append(new_df['Hotel Name'][j])
                    hotel_address.append(new_df['Hotel Address'][j])
                    latidudes.append(new_df['R Lat'][j])
                    longtudes.append(new_df['Real Long'][j])
                    countries.append(new_df['Country'][j])
                    categories.append(new_df['Category'][j])
                    distances.append(distance)
            # grouping the data into dataframe
            suggested_dataFrame = pd.DataFrame({"JpCode": prod_JpCodes, "Hotel_Name": hotel_names,
                                                "Latitude": latidudes, "Longtude": longtudes,
                                                "Hotel_Address": hotel_address, "Country": countries,
                                                "Category": categories,
                                                "Distance": distances})

            print("{} Rows Added successfully !".format(suggested_dataFrame.shape[0]))
            # convert distance to float to avoid the errors
            suggested_dataFrame['Distance'] = suggested_dataFrame['Distance'].astype('float64')
            # map the classes to the dataframe

            # st.markdown(f'<p style="font-family:Arial; color:black; font-size: 20px;<b>"> Very close data No.Hotels : {very_close.shape[0]} --- \nFair Distance data No.Hotels : { fair_distance.shape[0]} --- \nFar Distance : {far_distance.shape[0]} <b></p>'
            #             ,unsafe_allow_html=True)
            #
            # final_reviews=very_close.copy()
            final_reviews = suggested_dataFrame.copy().sort_values(by="Distance", ascending=True)

            # initialization
            final_reviews['Rates'] = "Not Available"
            final_reviews['Board Type'] = "Not Available"
            final_reviews['Lowest Rate'] = "Not Available"
            iterator = 0
            progress=1
            my_bar = st.progress(0)
            for i in range(final_reviews.shape[0]):
                try:
                    if iterator < 20:
                        xml_df = hv.extract_data(start_date, end_date, final_reviews['JpCode'][i].strip(), nationality, pax)
                        xml_df['Nett'] = xml_df['Nett'].astype(float)
                        rates = []
                        unique_boards = xml_df['Board_Type'].unique()
                        for board in unique_boards:
                            new_df = xml_df[xml_df['Board_Type'] == board]
                            rates.append(new_df['Nett'].min())
                        final_reviews['Board Type'][i] = unique_boards
                        final_reviews['Rates'][i] = rates
                        final_reviews['Lowest Rate'][i] = np.min(rates)
                        iterator += 1
                        time.sleep(0.1)
                        my_bar.progress(iterator/20)
                        print(iterator)
                    else:
                        break
                except Exception as e:
                    print(e)
                    continue
            print(iterator)
            if "level_0" in final_reviews.columns:
                final_reviews.drop('level_0', axis=1, inplace=True)
            final_reviews = final_reviews[final_reviews['Rates'] != "Not Available"]
            final_reviews = final_reviews.sort_values(by='Lowest Rate', ascending=True).reset_index()

            final_reviews = final_reviews.reset_index().drop('index', axis=1)
            data_msg=f'<p style="font-family:Courier; color:White; font-size: 20px;"><b>Final Data No of rows : {final_reviews.shape[0]}<b></p>'
            st.markdown(data_msg, unsafe_allow_html=True)

            final_reviews = final_reviews.sort_values(by='Lowest Rate', ascending=True).reset_index()
            try:
                final_reviews=final_reviews.drop("level_0",axis=1)
                final_reviews = final_reviews.drop("index", axis=1)
            except:
                pass

            st.dataframe(final_reviews)
            incidents = folium.map.FeatureGroup()
            # My Hotel data
            nLatidude = rawOfData['R Lat'][0]
            nLongtude = rawOfData['Real Long'][0]
            sanfran_map = folium.Map(location=[nLatidude, nLongtude], zoom_start=12)

            for lat, lng, label in zip(final_reviews['Latitude'], final_reviews['Longtude'], final_reviews['Hotel_Name']):
                incidents.add_child(
                    folium.features.CircleMarker(
                        [lat, lng],
                        radius=5,  # define how big you want the circle markers to be
                        color='yellow',
                        fill=True,
                        fill_color='blue',
                        fill_opacity=0.6,
                        popup=label
                    )
                )
                incidents.add_child(
                    folium.features.CircleMarker(
                        [nLatidude, nLongtude],
                        radius=7,  # define how big you want the circle markers to be
                        fill=True,
                        fill_color='blue',
                        fill_opacity=0.6
                    )
                )

            # add incidents to map
            sanfran_map=sanfran_map.add_child(incidents)
            folium_static(sanfran_map,width=1000,height=600)

        # except Exception as e:
        #     print(e)
    except Exception as e:
        print(e)

def data_class(x):
    if x <= 2:
        return "Very Close"
    elif 2 < x < 4:
        return "Fair Distance"
    else:
        return "Far Distance"

