from utils import geo_distance
from .csi_eps32 import ESP32

class Transmission:
    def __init__(self, df) -> None:
        self.data = df.copy()
        self.receiver_id = self.data.se.unique()[0] 
        self.tx_lon = self.data.ma_lon.unique()[0]
        self.tx_lat = self.data.ma_lat.unique()[0]
        self.rx_lon = self.data.se_lon.unique()[0]
        self.rx_lat = self.data.se_lat.unique()[0]
        self.__get_distance()
        self.__process_csi_data()

    
    def __get_distance(self):
        self.distance = geo_distance(self.rx_lat, self.rx_lon, self.tx_lat, self.tx_lon)
    
    def __process_csi_data(self):
        self.csi = ESP32(self.data)

    def self_description(self):
        description = f'rx {self.receiver_id} at (lat,lon)=({self.rx_lat},{self.rx_lon}) \n tx at (lat,lon)=({self.tx_lat},{self.tx_lon})'
        return description
    

        


