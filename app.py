import streamlit as st
from aiortc.contrib.media import MediaRecorder
from pathlib import Path
from streamlit_webrtc import VideoProcessorBase, WebRtcMode, webrtc_streamer
import urllib.request
import subprocess


import urllib.request

HERE = Path(__file__).parent

subprocess.run(['pip3', 'install', '--editable', './'])
subprocess.run(['python', 'setup.py', 'build_ext' ,'--inplace'])
# # This code is based on https://github.com/streamlit/demo-self-driving/blob/230245391f2dda0cb464008195a470751c01770b/streamlit_app.py#L48  # noqa: E501
def download_file(url, download_to: Path, expected_size=None):
    # Don't download the file twice.
    # (If possible, verify the download using the file length.)
    if download_to.exists():
        
        if expected_size:
            if download_to.stat().st_size == expected_size:
                return
        else:
            st.info(f"{url} is already downloaded.")
            if not st.button("Download again?"):
                return

    download_to.parent.mkdir(parents=True, exist_ok=True)

    # These are handles to two visual elements to animate.
    weights_warning, progress_bar = None, None
    try:
        weights_warning = st.warning("Downloading %s..." % url)
        progress_bar = st.progress(0)
        with open(download_to, "wb") as output_file:
            with urllib.request.urlopen(url) as response:
                length = int(response.info()["Content-Length"])
                counter = 0.0
                MEGABYTES = 2.0 ** 20.0
                while True:
                    data = response.read(8192)
                    if not data:
                        break
                    counter += len(data)
                    output_file.write(data)

                    # We perform animation by overwriting the elements.
                    weights_warning.warning(
                        "Downloading %s... (%6.2f/%6.2f MB)"
                        % (url, counter / MEGABYTES, length / MEGABYTES)
                    )
                    progress_bar.progress(min(counter / length, 1.0))
    # Finally, we remove these visual elements by calling .empty().
    finally:
        if weights_warning is not None:
            weights_warning.empty()
        if progress_bar is not None:
            progress_bar.empty()

    


# st.write()


from inter import s2t
def app():
   
    # # https://drive.google.com/file/d/1n0H4ARIZZrfdR7Iwhbfg1XZqf6GAFAGv/view?usp=sharing
    # cloud_model_location = "1n0H4ARIZZrfdR7Iwhbfg1XZqf6GAFAGv"
   
    # gdd.download_file_from_google_drive(file_id=cloud_model_location,
    #                                 dest_path='model/checkpoint_best.pt',
    #                                 unzip=False)

    # url = 'https://github.com/pymedphys/data/releases/download/VacbagModelWeights/unet_vacbag_512_dsc_epoch_120.hdf5'
    # url = 'https://drive.google.com/file/d/1n0H4ARIZZrfdR7Iwhbfg1XZqf6GAFAGv/view?usp=sharing'
    # filename = url.split('/')[-1]

    # urllib.request.urlretrieve(url, filename)

    MODEL_URL = "https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1n0H4ARIZZrfdR7Iwhbfg1XZqf6GAFAGv"  # noqa
    # LANG_MODEL_URL = "https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer"  # noqa
    MODEL_LOCAL_PATH = HERE / "model/checkpoint_best.pt"
    # LANG_MODEL_LOCAL_PATH = HERE / "models/deepspeech-0.9.3-models.scorer"

    download_file(MODEL_URL, MODEL_LOCAL_PATH, expected_size=365042194)
    # download_file(LANG_MODEL_URL, LANG_MODEL_LOCAL_PATH, expected_size=953363776)


    # url = 'https://github.com/pymedphys/data/releases/download/VacbagModelWeights/unet_vacbag_512_dsc_epoch_120.hdf5'
    # filename = url.split('/')[-1]

    # urllib.request.urlretrieve(url, filename)

    st.write("Click start button to record audio.")
    def in_recorder_factory() -> MediaRecorder:
        return MediaRecorder(
            "input.wav", format="wav"
        )

    webrtc_streamer(
        key="loopback",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={
            "video": False,
            "audio": True,
        },
        sendback_audio=False,
        in_recorder_factory=in_recorder_factory,
    )
    try:
        st.audio('input.wav', format="audio/wav")
    except:
        st.write("No record media.")
    s2t()

    





if __name__ == "__main__":
    app()