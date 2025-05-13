import logging
import os
import streamlit as st

from downloader import VideoDownloader, VideoDownloadError
from audio_utils import AudioExtractor, AudioExtractionError
from classifier import AccentClassifier, AccentClassificationError

# Configure root logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_video(url: str, cookies_browser: str = None) -> dict:
    """
    Download and analyze video to classify the speaker's accent.

    Args:
        url: URL of the video to analyze
        cookies_browser: Browser to extract cookies from (if needed)
    """
    # Check for cookies.txt file in the current directory
    cookies_file = "cookies.txt" if os.path.exists("cookies.txt") else None

    downloader = VideoDownloader(cookies_file=cookies_file)
    extractor = AudioExtractor()
    classifier = AccentClassifier()

    video_path = downloader.download(url, cookies_browser=cookies_browser)
    wav_path = extractor.extract(video_path)
    result = classifier.classify(wav_path)
    return {"wav_path": wav_path, **result}


def main() -> None:
    st.set_page_config(page_title="REM Waste Accent Classifier", layout="centered")
    st.title("🗣️ REM Waste Accent Classifier")

    st.write(
        "Enter a public video URL (YouTube, Loom, direct MP4). "
        "We'll download it, extract the audio, and predict the speaker's English accent."
    )

    # Main user inputs
    url = st.text_input("Video URL")

    # Advanced options in an expander
    with st.expander("Advanced Options"):
        st.write("If you encounter YouTube bot verification errors, select your browser to use cookies:")

        st.warning("⚠️ Safari is not supported due to macOS security restrictions")

        cookies_browser = st.selectbox(
            "Browser for cookies (optional)",
            [None, "chrome", "firefox", "edge", "opera"],
            index=0
        )

        st.write(
            "Alternatively, you can place a 'cookies.txt' file in the application directory. "
            "See the README for instructions on creating this file."
        )

    if st.button("Analyze Accent"):
        if not url.strip():
            st.error("Please enter a valid URL.")
            return

        try:
            with st.spinner("Analyzing…"):
                output = analyze_video(url, cookies_browser)

            st.audio(output["wav_path"])
            st.markdown(f"**Predicted Accent:** `{output['accent']}`")
            st.markdown(f"**Confidence:** `{output['confidence']:.2f}%`")
            st.markdown("**Top Predictions:**")
            st.table(output["top_n"])
            st.markdown(f"---\n*{output['info']}*")

        except VideoDownloadError as e:
            logger.exception("Download error")
            st.error(f"❌ {e}")
            # Provide helpful suggestions for common errors
            if "YouTube verification required" in str(e):
                st.info("Try expanding 'Advanced Options' to use browser cookies (Safari not supported).")
        except (AudioExtractionError, AccentClassificationError) as e:
            logger.exception("Processing error")
            st.error(f"❌ {e}")
        except Exception as e:
            logger.exception("Unexpected error")
            st.error("❌ Something went wrong. Please try again.")


if __name__ == "__main__":
    main()
