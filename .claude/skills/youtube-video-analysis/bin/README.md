# FFmpeg Binaries

## Local Installation

This folder contains FFmpeg binaries for the YouTube Video Analysis Skill.

**Current Status**: ✅ Binaries installed locally

### Files
- `ffmpeg.exe` (141.79 MB) - Main conversion tool
- `ffprobe.exe` (141.66 MB) - Metadata extraction
- `ffplay.exe` (141.64 MB) - Media player

**Version**: 2025-03-27 build (git-114fccc4a5)

## Why Not in Git?

These binaries (141MB each) exceed GitHub's 100MB file size limit and are excluded via `.gitignore`. However, they remain in your local copy for optimal performance.

## For Users Cloning from GitHub

If you clone this repository and this folder is empty, you have two options:

### Option 1: Use imageio-ffmpeg (Easiest)
```bash
pip install imageio-ffmpeg
```
This is already in `requirements.txt` and will automatically download bundled ffmpeg binaries (~50MB).

### Option 2: Download FFmpeg Manually (Best Performance)
1. Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract the following files to this folder:
   - `ffmpeg.exe`
   - `ffprobe.exe`
   - `ffplay.exe`

## Automatic Fallback

The skill automatically searches for ffmpeg in this priority order:
1. **Local binaries** (this folder) - Best performance
2. **imageio-ffmpeg** (bundled) - Good performance, easy install
3. **System PATH** - Manual installation

You don't need to do anything if the binaries are already here!

---

**Note**: This README is included in git, but the .exe files are not.

