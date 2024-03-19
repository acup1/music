import requests
from urllib.parse import unquote,quote ##### штука шоб ссылки переводить с казахского

TORRSERVER_IP = '127.0.0.1'
TORRSERVER_PORT = '8090'

def send_torrent_file(server_ip, server_port, torrent_filepath):
    url = f"http://{server_ip}:{server_port}/torrent/upload"

    # Загружаем файл как есть, без преобразования в base64
    with open(torrent_filepath, 'rb') as file:
        files = {'file': file.read()}

    response = requests.post(url, files=files)

    if response.status_code == 200:
        print(f"File {torrent_filepath} uploaded successfully.")
        return response.json()  # возвращаем json ответ
    else:
        print("Something went wrong.")
        print(f"Status code: {response.status_code}")
        print(f"Response text: {response.text}")
        return None

# пример использования
torrent_filepath = '1.torrent'  # замените на путь к вашему .torrent файлу
print(send_torrent_file(TORRSERVER_IP, TORRSERVER_PORT, torrent_filepath))