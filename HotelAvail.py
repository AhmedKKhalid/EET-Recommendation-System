from datetime import datetime, timedelta, date
import time
import requests
import xmltodict
import win32com.client as win32
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def Hotel_Basic_Info(data_dict):
    HotelResults=data_dict['soap:Envelope']['soap:Body']['HotelAvailResponse']['AvailabilityRS']['Results']['HotelResult']
    Hotel_Basic_Info_Dict=dict()
    Hotel_Basic_Info_List=['@Code','@JPCode','@BestDeal','@Type','@DestinationZone','@NonRefundable']
    #Code
    for i in Hotel_Basic_Info_List:
        try :
            Hotel_Basic_Info_Dict[i]=HotelResults[i]
        except KeyError:
            Hotel_Basic_Info_Dict[i]="NA"
    return Hotel_Basic_Info_Dict


# Number and Type of Options
def Number_Of_Option(data_dict):
    Number_of_Options_Type=type(data_dict['soap:Envelope']['soap:Body']['HotelAvailResponse']['AvailabilityRS']['Results']['HotelResult']['HotelOptions']['HotelOption'])

    if Number_of_Options_Type==list:
        Number_of_Options=len(data_dict['soap:Envelope']['soap:Body']['HotelAvailResponse']['AvailabilityRS']['Results']['HotelResult']['HotelOptions']['HotelOption'])
    else:
        Number_of_Options=1
    return Number_of_Options

def extract_data(start_date,end_date,Jp_code,Nationality,Number_of_paxes):
    query = {'start_date':start_date, 'end_date':end_date,'Jp_code':Jp_code,"Nationality":Nationality,"Number_of_paxes":Number_of_paxes}
    response = requests.get('http://18.192.74.107:443/api/v1/jobs/data', params=query)
    data_dict = xmltodict.parse(response.text)
    columns=["Type","Currency","Gross","Nett","ServiceAmount","NonRefundable","Units","Source","AvailRooms","Name","RoomCategoryType","Board_Type","Board_Name"
                               ,"RoomOccupancy","MaxOccupancy","Adult","Children","SupplementCode","SupplementCodeCat","SupplementCodeRes"]
    df=pd.DataFrame(columns=columns)
    Number_Of_Option_Len=Number_Of_Option(data_dict)
    HotelOptions=data_dict['soap:Envelope']['soap:Body']['HotelAvailResponse']['AvailabilityRS']['Results']['HotelResult']['HotelOptions']['HotelOption']
    Hotel_Basic_Info_Dict=Hotel_Basic_Info(data_dict)
    for x in range(Number_Of_Option_Len):
        try :
            RatePlanCode=HotelOptions[x]['@RatePlanCode']
        #RatePlanCode
        except KeyError:
            RatePlanCode="NA"
        except TypeError:
            RatePlanCode="NA"
        # Hotel Options Info
        #Status
        try :
            Status=HotelOptions[x]['@Status']
        #RatePlanCode
        except KeyError:
            Status="NA"
        except TypeError:
            Status="NA"
        # Hotel Options Info
        #NonRefundable
        try :
            NonRefundable=HotelOptions[x]['@NonRefundable']
        #RatePlanCode
        except KeyError:
            NonRefundable="NA"
        except TypeError:
            NonRefundable="NA"
        # Hotel Options Info
        #PackageContract
        try :
            PackageContract=HotelOptions[x]['@PackageContract']
        #RatePlanCode
        except KeyError:
            PackageContract="NA"
        except TypeError:
            PackageContract="NA"
        # Hotel Options Info
        #Board
        try :
            Board_Type=HotelOptions[x]['Board']['@Type']
        #RatePlanCode
        except KeyError:
            Board_Type="NA"
        except TypeError:
            Board_Type="NA"

        try :
            Board_Name=HotelOptions[x]['Board']['#text']
        #RatePlanCode
        except KeyError:
            Board_Name="NA"
        except TypeError:
            Board_Name="NA"

        # Hotel Options Info
        #Prices
        try :
            Type=HotelOptions[x]['Prices']['Price']['@Type']
        #RatePlanCode
        except KeyError:
            Type="NA"
        except TypeError:
            Type="NA"

        try :
            Currency=HotelOptions[x]['Prices']['Price']['@Currency']
        #RatePlanCode
        except KeyError:
            Currency="NA"
        except TypeError:
            Currency="NA"
        try :
            Gross=HotelOptions[x]['Prices']['Price']['TotalFixAmounts']['@Gross']
        #RatePlanCode
        except KeyError:
            Gross="NA"
        except TypeError:
            Gross="NA"
        try :
            Nett=HotelOptions[x]['Prices']['Price']['TotalFixAmounts']['@Nett']
        #RatePlanCode
        except KeyError:
            Nett="NA"
        except TypeError:
            Nett="NA"

        try :
            ServiceAmount=HotelOptions[x]['Prices']['Price']['TotalFixAmounts']['Service']['@Amount']
        #RatePlanCode
        except KeyError:
            ServiceAmount="NA" 
        except TypeError:
            ServiceAmount="NA"
        # Hotel Options Info
        #Rooms
        try :
            if type(HotelOptions[x]['HotelRooms']['HotelRoom'])==list:
                Units=HotelOptions[x]['HotelRooms']['HotelRoom'][0]['@Units']
            else:
                Units=HotelOptions[x]['HotelRooms']['HotelRoom']['@Units']
        #RatePlanCode
        except KeyError:
            Units="NA"
        except TypeError:
            Units="NA"

        try :
            if type(HotelOptions[x]['HotelRooms']['HotelRoom'])==list:
                Source=HotelOptions[x]['HotelRooms']['HotelRoom'][0]['@Source']
            else:
                Source=HotelOptions[x]['HotelRooms']['HotelRoom']['@Source']
        except KeyError:
            Source="NA"
        except TypeError:
            Source="NA"


        try :
            if type(HotelOptions[x]['HotelRooms']['HotelRoom'])==list:
                AvailRooms=HotelOptions[x]['HotelRooms']['HotelRoom'][0]['@AvailRooms']
            else:
                AvailRooms=HotelOptions[x]['HotelRooms']['HotelRoom']['@AvailRooms']
        except KeyError:
            AvailRooms="NA"
        except TypeError:
            AvailRooms="NA"

        try :
            if type(HotelOptions[x]['HotelRooms']['HotelRoom'])==list:
                Name=HotelOptions[x]['HotelRooms']['HotelRoom'][0]['Name']
            else:
                Name=HotelOptions[x]['HotelRooms']['HotelRoom']['Name']
        #RatePlanCode
        except KeyError:
            Name="NA"
        except TypeError:
            Name="NA"


        try :
            if type(HotelOptions[x]['HotelRooms']['HotelRoom'])==list:
                RoomCategoryType=HotelOptions[x]['HotelRooms']['HotelRoom'][0]['@Type']
            else:
                RoomCategoryType=HotelOptions[x]['HotelRooms']['HotelRoom']['@Type']
        except KeyError:
            RoomCategoryType="NA"
        except TypeError:
            RoomCategoryType="NA"

        try :
            RoomOccupancy=HotelOptions[x]['HotelRooms']['HotelRoom']['RoomOccupancy']['@Occupancy']
        #RatePlanCode
        except KeyError:
            RoomOccupancy="NA"
        except TypeError:
            RoomOccupancy="NA"

        try :
            MaxOccupancy=HotelOptions[x]['HotelRooms']['HotelRoom']['RoomOccupancy']['@MaxOccupancy']
        #RatePlanCode
        except KeyError:
            MaxOccupancy="NA"
        except TypeError:
            MaxOccupancy="NA"

        try :
            Adult=HotelOptions[x]['HotelRooms']['HotelRoom']['RoomOccupancy']['@Adults']
        #RatePlanCode
        except KeyError:
            Adult="NA"
        except TypeError:
            Adult="NA"

        try :
            Children=HotelOptions[x]['HotelRooms']['HotelRoom']['RoomOccupancy']['@Children']
        #RatePlanCode
        except KeyError:
            Children="NA"
        except TypeError:
            Children="NA"

        # Hotel Options Info
        #Rooms

        try :
            SupplementCode=HotelOptions[x]['AdditionalElements']['HotelSupplements']['HotelSupplement']['@Code']
        #RatePlanCode
        except KeyError:
            SupplementCode="NA"
        except TypeError:
            SupplementCode="NA"

        try :
            SupplementCodeCat=HotelOptions[x]['AdditionalElements']['HotelSupplements']['HotelSupplement']['@Category']
        #RatePlanCode
        except KeyError:
            SupplementCodeCat="NA"
        except TypeError:
            SupplementCodeCat="NA"

        try :
            SupplementCodeRes=HotelOptions[x]['AdditionalElements']['HotelSupplements']['HotelSupplement']['@OnlyResidents']
        #RatePlanCode
        except KeyError:
            SupplementCodeRes="NA"
        except TypeError:
            SupplementCodeRes="NA"

        try :
            SupplementName=HotelOptions[x]['AdditionalElements']['HotelSupplements']['HotelSupplement']['Name']
        #RatePlanCode
        except KeyError:
            SupplementName="NA"
        except TypeError:
            SupplementName="NA"
        #####

        try :
            HotelOfferCode=HotelOptions[x]['AdditionalElements']['HotelOffers']['HotelOffer']['@Code']
        #RatePlanCode
        except KeyError:
            HotelOfferCode="NA"
        except TypeError:
            HotelOfferCode="NA"

        try :
            HotelOfferCat=HotelOptions[x]['AdditionalElements']['HotelOffers']['HotelOffer']['@Category']
        #RatePlanCode
        except KeyError:
            HotelOfferCat="NA"
        except TypeError:
            HotelOfferCat="NA"

        try :
            HotelOfferNRF=HotelOptions[x]['AdditionalElements']['HotelOffers']['HotelOffer']['@NonRefundable']
        #RatePlanCode
        except KeyError:
            HotelOfferNRF="NA"
        except TypeError:
            HotelOfferNRF="NA"

        try :
            HotelOfferOnlyRes=HotelOptions[x]['AdditionalElements']['HotelOffers']['HotelOffer']['@OnlyResidents']
        #RatePlanCode
        except KeyError:
            HotelOfferOnlyRes="NA"
        except TypeError:
            HotelOfferOnlyRes="NA"

        try :
            HotelOfferName=HotelOptions[x]['AdditionalElements']['HotelOffers']['HotelOffer']['Name']
        #RatePlanCode
        except KeyError:
            HotelOfferName="NA"
        except TypeError:
            HotelOfferName="NA"

        Hotel_Rooms_Info_List=["Type","Currency","Gross","Nett","ServiceAmount","NonRefundable","Units","Source","AvailRooms","Name","RoomCategoryType","Board_Type","Board_Name"
                               ,"RoomOccupancy","MaxOccupancy","Adult","Children","SupplementCode","SupplementCodeCat","SupplementCodeRes"
                               ,"SupplementName""HotelOfferCode","HotelOfferCat","HotelOfferNRF","SupplementCodeRes","HotelOfferOnlyRes","HotelOfferName"]

        Hotel_Rooms_Values_List=[Type,Currency,Gross,Nett,ServiceAmount,NonRefundable,Units,Source,AvailRooms,Name,RoomCategoryType,Board_Type,Board_Name
                               ,RoomOccupancy,MaxOccupancy,Adult,Children,SupplementCode,SupplementCodeCat,SupplementCodeRes
                               ,SupplementName,HotelOfferCode,HotelOfferCat,HotelOfferNRF,SupplementCodeRes,HotelOfferOnlyRes,HotelOfferName]

        Rooms_info_dict=dict()
        #Code
        for i in range(len(Hotel_Rooms_Info_List)):
            try :
                Rooms_info_dict[Hotel_Rooms_Info_List[i]]=Hotel_Rooms_Values_List[i]
            except KeyError:
                Rooms_info_dict[Hotel_Rooms_Info_List[i]]="NA"
        df=df.append(Rooms_info_dict,ignore_index=True)
    for i in list(Hotel_Basic_Info_Dict.keys()):
        df[i]=Hotel_Basic_Info_Dict[i]
    return df