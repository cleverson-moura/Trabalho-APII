import requests

class GeocodeHelper:
    def __init__(self, user_agent="meu-app-hotel/1.0"):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.headers = {"User-Agent": user_agent}

    def endereco_para_latlng(self, endereco: str):
        """
        Converte endereço (rua, bairro, cidade) em latitude e longitude
        usando a API Nominatim (OpenStreetMap).
        """
        params = {
            "q": endereco,
            "format": "json",
            "limit": 1
        }
        response = requests.get(self.base_url, params=params, headers=self.headers)

        if response.status_code == 200 and response.json():
            data = response.json()[0]
            return float(data["lat"]), float(data["lon"])
        
        return None, None
