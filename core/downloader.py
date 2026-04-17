# import yt_dlp

# def get_video_info(url):
#     try:
#         with yt_dlp.YoutubeDL() as ydl:
#             info = ydl.extract_info(url, download=False)
#             title = info.get("title", "No title")

#             formats = info.get("formats", [])
#             qualities = []

#             for f in formats:
#                 if f.get("height"):
#                     qualities.append(f"{f['height']}p")

#             qualities = list(set(qualities))
#             return title, qualities

#     except Exception as e:
#         return None, str(e)


# def download_video(url, resolution):
#     try:
#         ydl_opts = {
#             'format': f'bestvideo[height={resolution[:-1]}]+bestaudio/best',
#             'outtmpl': 'downloads/%(title)s.%(ext)s'
#         }

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])

#         return True

#     except Exception as e:
#         return str(e)/

import yt_dlp

# 🔹 Get video info (title + qualities)
def get_video_info(url):
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title", "No title")

            formats = info.get("formats", [])
            qualities = []

            for f in formats:
                if f.get("height"):
                    qualities.append(f"{f['height']}p")

            qualities = sorted(list(set(qualities)))
            return title, qualities

    except Exception as e:
        return None, str(e)


# 🔹 Download video with progress
def download_video(url, resolution, progress_callback=None):
    try:
        def hook(d):
            if d['status'] == 'downloading':
                percent = d.get('_percent_str', '0%')
                if progress_callback:
                    progress_callback(percent)
            elif d['status'] == 'finished':
                if progress_callback:
                    progress_callback("100%")

        ydl_opts = {
            'format': f'bestvideo[height={resolution[:-1]}]+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'progress_hooks': [hook]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return True

    except Exception as e:
        return str(e)


# 🔹 Download audio (MP3)
def download_audio(url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return True

    except Exception as e:
        return str(e)