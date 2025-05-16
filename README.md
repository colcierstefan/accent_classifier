# REM Waste Accent Classifier

A web application that analyzes videos to identify the speaker's English accent. Simply provide a URL to a public video (YouTube, Loom, or direct MP4), and the classifier will process the audio to determine the most likely accent.


## Features

- 🎥 Download videos from YouTube, Loom, or direct MP4 links
- 🔊 Extract audio for processing
- 🗣️ Classify English accents using a pre-trained model
- 📊 Display confidence scores and top predictions
- 🎛️ Simple and intuitive web interface

## Installation

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone https://github.com/colcierstefan/accent_classifier.git
cd tech-challenge

# Install dependencies with Poetry
poetry install

# Activate the virtual environment
poetry shell
```

### Using pip

```bash
# Clone the repository
git clone (https://github.com/colcierstefan/accent_classifier).git
cd tech-challenge

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### System Requirements

- Python 3.12+
- FFmpeg (must be installed on your system and available in PATH)

## Usage

### Running the Web Application

```bash
# Start the Streamlit application
streamlit run src/app.py
```

Then navigate to `http://localhost:8501` in your web browser to access the application.

### Example

1. Paste a YouTube, Loom, or direct MP4 URL into the text field
2. Click "Analyze Accent"
3. Wait for processing (download, audio extraction, and classification)
4. Review the results showing predicted accent, confidence score, and alternative predictions

### Handling YouTube Verification Issues

If you encounter errors like "Sign in to confirm you're not a bot," you have several options:

#### Option 1: Use Browser Cookies (Recommended)
1. Expand the "Advanced Options" section in the app
2. Select your browser from the dropdown (Chrome or Firefox recommended)
3. This will use cookies from your browser where you're already logged into YouTube

**Note: Safari is NOT supported** due to macOS security restrictions. Safari users should use Option 2 or 3 instead.

#### Option 2: Use a cookies.txt File
1. Create a `cookies.txt` file in the application directory
2. Export your cookies from your browser using an extension:
   - For Chrome: Install the ["Get cookies.txt LOCALLY" extension](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - For Firefox: Install the ["cookies.txt" extension](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)
3. Visit YouTube, make sure you're logged in
4. Use the extension to export cookies for the youtube.com domain
5. Save the file as `cookies.txt` in the root directory of the project
6. Restart the application

#### Option 3: Try Different Videos
Some videos may not trigger the verification check. Try using videos from smaller channels or less popular content that may not have the same anti-bot protections.

For more information on creating cookies files, see the [yt-dlp wiki](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp).

## Architecture

The application consists of three main components:

1. **VideoDownloader**: Downloads videos from URLs using either direct HTTP requests or yt-dlp
2. **AudioExtractor**: Extracts audio from videos and converts to WAV format using FFmpeg
3. **AccentClassifier**: Analyzes audio using a pre-trained Hugging Face model to predict the speaker's accent

## Model Information

The accent classification model used is [`dima806/english_accents_classification`](https://huggingface.co/dima806/english_accents_classification) from Hugging Face, which can identify various English accents.

## Project Structure

```
tech-challenge/
├── audio/                  # Extracted audio files
├── downloads/              # Downloaded video files
├── src/
│   ├── __init__.py
│   ├── app.py              # Streamlit web application
│   ├── downloader.py       # Video downloading functionality
│   ├── audio_utils.py      # Audio extraction functionality
│   └── classifier.py       # Accent classification functionality
├── pyproject.toml          # Poetry configuration
├── requirements.txt        # Pip dependencies
└── README.md               # This file
```

## Error Handling

The application implements robust error handling for:
- Failed video downloads
- Audio extraction issues
- Classification errors

## License

[MIT License](LICENSE)

## Contributors

- Stefan Colcier
