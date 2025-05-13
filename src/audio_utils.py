import os
import ffmpeg
import logging

logger = logging.getLogger(__name__)

class AudioExtractionError(Exception):
    """Raised when audio extraction fails."""

class AudioExtractor:
    """
    Extracts audio from video files and converts to WAV mono at a given sample rate.
    """

    def __init__(self, output_dir: str = "audio", sample_rate: int = 16000) -> None:
        self.output_dir = output_dir
        self.sample_rate = sample_rate
        os.makedirs(self.output_dir, exist_ok=True)

    def extract(self, video_path: str) -> str:
        """
        Extract audio from `video_path`, return path to mono-WAV file.
        """
        base = os.path.splitext(os.path.basename(video_path))[0]
        wav_path = os.path.join(self.output_dir, f"{base}.wav")

        try:
            (
                ffmpeg
                .input(video_path)
                .output(
                    wav_path,
                    ac=1,
                    ar=self.sample_rate,
                    format="wav",
                    loglevel="error"
                )
                .overwrite_output()
                .run()
            )
            logger.debug("Audio extracted to %s", wav_path)
            return wav_path

        except ffmpeg.Error as e:
            logger.error("FFmpeg error: %s", e)
            raise AudioExtractionError(f"Failed to extract audio: {e}")
