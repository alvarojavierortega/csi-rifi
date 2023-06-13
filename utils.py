from math import sin, cos, sqrt, atan2, radians


def split_data(df) -> list:
    id_receivers = df['se'].unique()
    ma_lon = df['ma_lon'].unique()
    ma_lat = df['ma_lat'].unique()
    se_lon = df['se_lon'].unique()
    se_lat = df['se_lat'].unique()
    splitted_data = []
    for id_receiver in id_receivers:
        for tx_lon in ma_lon:
            for tx_lat in ma_lat: 
                for rx_lon in se_lon:
                    for rx_lat in se_lat:
                        df_f =  df[
                            (df['se'] == id_receiver) & 
                            (df['ma_lon'] == tx_lon) &
                            (df['ma_lat'] == tx_lat) &
                            (df['se_lon'] == rx_lon) &
                            (df['se_lat'] == rx_lat)
                            ] 
                        if not df_f.empty: splitted_data.append(df_f)
    return splitted_data


def geo_distance(p_lat1: float, p_lon1: float, p_lat2: float, p_lon2: float) ->  float:
    """ Returns the distance between two float coordenates  in kilometers 

    Args:
        p_lat1 (float): latitude of pont 1
        p_lon1 (float): longitude of pont 1
        p_lat2 (float): latitude of pont 2
        p_lon2 (float): longitude of pont 2

    Returns:
        float: distance between two points based on latitude/longitude
    """    
    
    R = 6373.0 # Approximate radius of earth in km

    lat1 = radians(p_lat1)
    lon1 = radians(p_lon1)
    lat2 = radians(p_lat2)
    lon2 = radians(p_lon2)


    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance
