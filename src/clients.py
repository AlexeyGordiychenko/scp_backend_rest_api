from datetime import datetime

# client
# {
#     id
#     client_name
#     client_surname
#     birthday
#     gender
#     registration_date
#     address_id
# }


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


CLIENTS = {
    1: {
        "id": "1",
        "client_name": "John",
        "client_surname": "Doe",
        "birthday": "2000-01-01",
        "gender": "male",
        "registration_date": get_timestamp(),
        "address_country": "Canada",
        "address_city": "Toronto",
        "address_street": "123 Main Street",
    },
    2: {
        "id": "2",
        "client_name": "Mary",
        "client_surname": "Jane",
        "birthday": "2010-01-01",
        "gender": "female",
        "registration_date": get_timestamp(),
        "address_country": "USA",
        "address_city": "Philadelphia",
        "address_street": "345 Broad Street",
    },
    3: {
        "id": "3",
        "client_name": "Charlie",
        "client_surname": "Brown",
        "birthday": "2005-05-16",
        "gender": "male",
        "registration_date": get_timestamp(),
        "address_country": "Germany",
        "address_city": "Berlin",
        "address_street": "234 Avenue Street",
    },
}


def read_all():
    return list(CLIENTS.values())


def create(client):
    client_name = client.get("client_name")
    client_surname = client.get("client_surname")
    birthday = client.get("birthday")
    gender = client.get("gender")
    address_country = client.get("address_country")
    address_city = client.get("address_city")
    address_street = client.get("address_street")

    id = len(CLIENTS) + 1
    CLIENTS[id] = {
        "id": id,
        "client_name": client_name,
        "client_surname": client_surname,
        "birthday": birthday,
        "gender": gender,
        "registration_date": get_timestamp(),
        "address_country": address_country,
        "address_city": address_city,
        "address_street": address_street,
    }

    return CLIENTS[id], 201
