Add-Type -AssemblyName System.Speech
$radioSynth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$radioSynth.Rate = 0
$radioSynth.Volume = 100
$radioFmt = [System.Speech.AudioFormat.SpeechAudioFormatInfo]::new(22050,[System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen,[System.Speech.AudioFormat.AudioChannel]::Mono)
$radioLines = @(
 @('airstrike','Air strike incoming.','Microsoft Zira Desktop'),
 @('orbital','Orbital strike incoming.','Microsoft Zira Desktop'),
 @('supply','Supply inbound.','Microsoft Zira Desktop'),
 @('armor','Armored support inbound.','Microsoft Zira Desktop'),
 @('shield','Shield deployment confirmed.','Microsoft Zira Desktop'),
 @('emp','EMP strike confirmed.','Microsoft Zira Desktop'),
 @('linked','Command link established.','Microsoft Zira Desktop'),
 @('warning','Heavy hostile approaching.','Microsoft David Desktop'),
 @('objective','Objective complete. Proceed to extraction.','Microsoft Zira Desktop'),
 @('unknown','还有活人吗？收到请回答。','Microsoft Huihui Desktop')
)
New-Item -ItemType Directory -Force -Path 'voice-sources' | Out-Null
foreach($radioLine in $radioLines){
 $radioSynth.SelectVoice($radioLine[2]); $radioSynth.SetOutputToWaveFile((Join-Path (Get-Location) ('voice-sources/'+$radioLine[0]+'.wav')),$radioFmt); $radioSynth.Speak($radioLine[1]); $radioSynth.SetOutputToNull()
}
$radioSynth.Dispose()
