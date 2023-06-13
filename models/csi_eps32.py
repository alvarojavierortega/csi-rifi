import numpy as np
import pandas as pd


class ESP32:
    """Parse ESP32 Wi-Fi Channel State Information (CSI) obtained using ESP32 CSI 
        This code is based on https://github.com/RikeshMMM/ESP32-CSI-Python-Parser/tree/main
    """

    NULL_SUBCARRIERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 64, 65, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 382, 383]

    def __init__(self, df:pd.DataFrame):
        """Read RAW CSI file (.csv) as a Pandas dataframe
        """
        self.csi_df = df.copy()
        self.__filter_by_sig_mode(1)
        self.__get_csi()
        self.__remove_null_subcarriers()
        self.__get_amplitude_from_csi()
        self.__get_phase_from_csi()



    def __filter_by_sig_mode(self, sig_mode:int) -> pd.DataFrame:
        """Filter CSI data by signal mode
        Args:  
            sig_mode (int):
            0 : Non - High Throughput Signals (non-HT)
            1 : HIgh Throughput Signals (HT)
        """
        self.csi_df = self.csi_df[self.csi_df['sig_mode'] == sig_mode]


    def __get_csi(self):
        """Read CSI string as Numpy array

        The CSI data collected by ESP32 contains channel frequency responses (CFR) represented by two signed bytes (imaginary, real) for each sub-carriers index
        The length (bytes) of the CSI sequency depends on the CFR type
        CFR consist of legacy long training field (LLTF), high-throughput LTF (HT-LTF), and space- time block code HT-LTF (STBC-HT-LTF)
        Ref: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/wifi.html#wi-fi-channel-state-information

        NOTE: Not all 3 field may not be present (as represented in table and configuration)
        """
        raw_csi_data = self.csi_df['csi']
        csi_data = np.array([np.fromstring(csi_datum, dtype=int, sep = ',') for csi_datum in raw_csi_data])
        self.csi_data = csi_data


    # NOTE: Currently does not provide support for all signal subcarrier types
    def __remove_null_subcarriers(self):
        """Remove NULL subcarriers from CSI
        """

        # Non-HT Signals (20 Mhz) - non STBC
        if self.csi_data.shape[1] == 128:
            remove_null_subcarriers = self.NULL_SUBCARRIERS[:24]
        # HT Signals (40 Mhz) - non STBC
        elif self.csi_data.shape[1] == 384:
            remove_null_subcarriers = self.NULL_SUBCARRIERS
        elif self.csi_data.shape[1] == 256:
            aux = [v+128 for v in self.NULL_SUBCARRIERS[:24]]
            remove_null_subcarriers = self.NULL_SUBCARRIERS[:24] + aux 
        else:
            return self

        csi_data_T = self.csi_data.T
        csi_data_T_clean = np.delete(csi_data_T, remove_null_subcarriers, 0)
        csi_data_clean = csi_data_T_clean.T
        self.csi_data = csi_data_clean

        return self

    def __get_amplitude_from_csi(self):
        """Calculate the Amplitude (or Magnitude) from CSI
        Ref: https://farside.ph.utexas.edu/teaching/315/Waveshtml/node88.html
        """
        amplitude = np.array([np.sqrt(data[::2]**2 + data[1::2]**2) for data in self.csi_data])
        self.amplitude = amplitude

    def __get_phase_from_csi(self):
        """Calculate the Amplitude (or Magnitude) from CSI
        Ref: https://farside.ph.utexas.edu/teaching/315/Waveshtml/node88.html
        """
        phase = np.array([np.arctan2(data[::2], data[1::2]) for data in self.csi_data])
        self.phase = phase
