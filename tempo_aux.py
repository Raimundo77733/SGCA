import datetime

try:
    import ntplib  # pyright: ignore[reportMissingImports]
except ModuleNotFoundError:
    ntplib = None


def time_get():
    if ntplib is None:
        raise RuntimeError("O módulo 'ntplib' não está instalado.")

    client = ntplib.NTPClient()

    response = client.request('a.st1.ntp.br', version=3)

    return str(datetime.datetime.fromtimestamp(response.tx_time))


def date_get():
    ntp_string=time_get()
    ntp_string=ntp_string.split(" ")
    ntp_string=str(ntp_string[0])
    ntp_string=ntp_string.split("-")
    data = datetime.datetime(int(ntp_string[0]),int(ntp_string[1]),int(ntp_string[2]))
    return data


def criar_data(data):
    data_string = data.split("/")
    data = datetime.datetime(int(data_string[2]),int(data_string[1]),int(data_string[0]))
    return data

