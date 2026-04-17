import streamlit as st
import os
import subprocess
from core.downloader import get_video_info, download_video, download_audio

st.set_page_config(page_title="YouTube Downloader", page_icon="🎥")

st.title("🎥 YouTube Video Downloader")

# 🔹 Input
url = st.text_input("Enter YouTube URL")

if url:
    title, qualities = get_video_info(url)

    if title is None:
        st.error(qualities)
    else:
        st.write(f"**Title:** {title}")

        # 🔹 Thumbnail
        try:
            import yt_dlp
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(url, download=False)
                st.image(info.get("thumbnail"))
        except:
            pass

        # 🔹 Mode selection
        mode = st.radio("Select Mode", ["Video", "Audio (MP3)"])

        # 🔹 Progress UI
        progress_text = st.empty()
        progress_bar = st.progress(0)

        def update_progress(p):
            progress_text.text(f"Downloading... {p}")
            try:
                percent = float(p.replace('%', ''))
                progress_bar.progress(int(percent))
            except:
                pass

        # 🔹 Video options
        if mode == "Video":
            if len(qualities) == 0:
                st.warning("No qualities found")
            else:
                choice = st.selectbox("Select Quality", qualities)

        # 🔹 Download button
        if st.button("Download"):
            with st.spinner("Downloading... please wait ⏳"):
                if mode == "Video":
                    result = download_video(url, choice, update_progress)
                else:
                    result = download_audio(url)

            if result == True:
                progress_text.text("Download Complete ✅")
                st.success("Downloaded Successfully!")

                # ✅ Save folder path in session
                folder_path = os.path.abspath("downloads")
                st.session_state["folder_path"] = folder_path
            else:
                st.error(result)


# ✅ SHOW AFTER DOWNLOAD (OUTSIDE BUTTON)
if "folder_path" in st.session_state:
    st.info(f"📁 Saved at: {st.session_state['folder_path']}")

    if st.button("📂 Open Downloads Folder"):
        subprocess.run(f'explorer "{st.session_state["folder_path"]}"')