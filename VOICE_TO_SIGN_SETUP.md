# Voice to Sign Feature - Setup Guide

## Overview
This feature allows users to:
1. **Speak** text through their microphone
2. **See** the recognized text displayed
3. **View** corresponding sign language letter images

## Features
- 🎤 Real-time voice recognition (using Web Speech API)
- 📝 Text display of recognized speech
- 🖼️ Visual sign language letter representation
- ✨ Clean, modern interface
- 📱 Fully responsive design

## Installation Requirements

### 1. Install Python Dependencies
```bash
pip install SpeechRecognition pydub
```

Optional: For audio file support, install FFmpeg
```bash
# Windows (using pip)
pip install pydub

# Or download from: https://ffmpeg.org/download.html
```

### 2. Browser Compatibility
The voice feature uses the **Web Speech API**, which works in:
- ✅ Chrome/Chromium
- ✅ Edge
- ✅ Safari
- ✅ Firefox (limited)

## How to Use

### 1. Accessing the Feature
- Navigate to `/voice-to-sign` route or click "Voice to Sign" in the navigation menu

### 2. Recording Voice
- Click the **"Start Recording"** button
- Speak clearly (e.g., "hi", "hello", "abc")
- The system will recognize your speech
- Recognized text will be displayed

### 3. Sign Images
- Once text is recognized, corresponding sign language letter images will be displayed
- Images are pulled from: `static/signs/`

## Sign Image Setup

### Where to Place Images
Place sign language letter images in: `static/signs/`

### Naming Convention
Images should be named with single characters:
- `a.png` - for letter A
- `b.png` - for letter B
- `h.png` - for letter H
- `i.png` - for letter I
- `0.png` - for number 0
- `1.png` - for number 1
- etc.

### Supported Formats
- PNG ✅
- JPG ✅
- GIF ✅

### Image Size Recommendation
- Minimum: 80x80 pixels
- Recommended: 150x150 pixels
- Maximum: 500x500 pixels

## Backend Module

### VoiceToText Class Location
`app_files/main/voice_to_text.py`

### Methods Available
```python
from app_files import VoiceToText

voice = VoiceToText()

# Recognize speech from microphone
text = voice.recognize_speech()

# Convert text to signs (letters)
signs = voice.text_to_signs("hello")  # Returns ['h', 'e', 'l', 'l', 'o']

# Correct spelling
corrected = voice.correct_text("wrld")  # Returns "world"
```

## API Routes

### 1. Display Voice to Sign Page
```
GET /voice-to-sign
```
Returns the voice-to-sign converter interface

## Troubleshooting

### Issue: "Speech Recognition not supported"
**Solution:** Use Chrome, Edge, or Safari browser

### Issue: Microphone not detected
**Solution:** 
1. Check browser permissions (allow microphone access)
2. Restart browser
3. Check if microphone is connected

### Issue: Images not showing
**Solution:**
1. Verify images are in: `static/signs/`
2. Check file names are lowercase single characters (a.png, b.png, etc.)
3. Clear browser cache (Ctrl+F5)

### Issue: Recognition accuracy poor
**Solution:**
1. Speak clearly and at normal pace
2. Reduce background noise
3. Keep microphone at 15-20cm distance

## Next Steps

1. **Add Sign Images**: Place your sign language letter images in `static/signs/`
2. **Test the Feature**: Visit `/voice-to-sign` and try speaking
3. **Customize**: Modify `templates/VoiceToSign.html` styling as needed

## File Structure
```
project/
├── app.py (updated with /voice-to-sign route)
├── app_files/
│   ├── __init__.py (updated)
│   └── main/
│       └── voice_to_text.py (NEW)
├── templates/
│   ├── VoiceToSign.html (NEW)
│   └── index.html (updated with navigation link)
└── static/
    └── signs/ (NEW - add your letter images here)
        ├── a.png
        ├── b.png
        ├── h.png
        ├── i.png
        └── ...
```

## Additional Notes

- The Web Speech API works client-side (in browser), so no server-side processing is needed
- Fallback to typing text if microphone is unavailable
- The interface gracefully handles errors and shows user-friendly messages
- All styles are embedded in the template for easy customization

## Support

For issues or enhancements, check:
1. Browser console (F12) for JavaScript errors
2. Flask server logs for backend errors
3. Verify all dependencies are installed with: `pip list`
