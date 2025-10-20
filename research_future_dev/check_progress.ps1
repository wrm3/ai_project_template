# Check YouTube analysis progress
Write-Host "=" * 80
Write-Host "YouTube Video Analysis - Progress Check"
Write-Host "=" * 80
Write-Host ""

$files = Get-ChildItem -Path "." -File | Where-Object { $_.Name -match "FOqbS_llAms" }

if ($files.Count -eq 0) {
    Write-Host "[INFO] No files yet - still downloading video..."
} else {
    Write-Host "[INFO] Files created so far:"
    Write-Host ""
    foreach ($file in $files) {
        $sizeMB = [math]::Round($file.Length / 1MB, 2)
        Write-Host "  - $($file.Name) ($sizeMB MB) - $($file.LastWriteTime)"
    }
}

Write-Host ""
Write-Host "Expected files:"
Write-Host "  1. FOqbS_llAms_video.mp4 - Downloaded video"
Write-Host "  2. FOqbS_llAms_audio.mp3 - Extracted audio"
Write-Host "  3. FOqbS_llAms_transcript.txt - Whisper transcription"
Write-Host "  4. FOqbS_llAms_analysis_prompt.txt - LLM prompt"
Write-Host "  5. FOqbS_llAms_metadata.json - Video metadata"
Write-Host ""

