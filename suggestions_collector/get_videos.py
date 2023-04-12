import google.auth
from googleapiclient.discovery import build
ч
GOOGLE_APPLICATION_CREDENTIALS = 'API_TOKEN.json'

# Аутентификация и настройка API клиента
credentials, project = google.auth.default(scopes=['https://www.googleapis.com/auth/youtube.readonly'])
youtube = build('youtube', 'v3', credentials=credentials)

# ID вашего канала
channel_id = 'UCYspuehThql30psLWg3c-fA'

# Выполнение запроса и вывод списка видео
request = youtube.search().list(
    part='id,snippet',
    channelId=channel_id,
    maxResults=50 # Максимальное количество видео для получения
)
response = request.execute()

# Вывод списка видео
for item in response['items']:
    video_title = item['snippet']['title']
    video_id = item['id']['videoId']
    print(f'{video_title}: {video_id}')
