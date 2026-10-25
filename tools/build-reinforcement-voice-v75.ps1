$ErrorActionPreference='Stop'
$radioCom=New-Object -ComObject SAPI.SpVoice
$radioCom.Rate=0
$radioTokens=$radioCom.GetVoices()
$radioEnglish=$null
for($radioIndex=0;$radioIndex -lt $radioTokens.Count;$radioIndex++){if($radioTokens.Item($radioIndex).GetDescription().Contains('Zira')){$radioEnglish=$radioTokens.Item($radioIndex);break}}
if($null -eq $radioEnglish){throw 'Microsoft Zira voice is required to match existing radio notifications.'}
$radioCom.Voice=$radioEnglish
$radioStream=New-Object -ComObject SAPI.SpFileStream
$radioStream.Format.Type=22
$radioStream.Open((Join-Path (Split-Path $PSScriptRoot -Parent) 'voice-sources/reinforcements.wav'),3,$false)
$radioCom.AudioOutputStream=$radioStream
$null=$radioCom.Speak('Reinforcements have arrived.',0)
$radioStream.Close()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($radioStream)|Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($radioCom)|Out-Null
