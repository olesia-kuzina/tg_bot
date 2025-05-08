from json import load


class CountryHelpers:
    with open("country.json", encoding='utf8') as file:
        capitals = {key.lower(): value for key, value in load(file).items()}

    @classmethod
    def search_capital(cls, country: str):
        return cls.capitals.get(country.lower())