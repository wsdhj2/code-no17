$ErrorActionPreference='Stop'
$radioCom = New-Object -ComObject SAPI.SpVoice
$radioCom.Rate = 0
$radioLines = @(
 @('airstrike','Air strike incoming.','Zira'), @('orbital','Orbital strike incoming.','Zira'),
 @('supply','Supply inbound.','Zira'), @('armor','Armored support inbound.','Zira'),
 @('shield','Shield deployment confirmed.','Zira'), @('emp','EMP strike confirmed.','Zira'),
 @('linked','Command link established.','Zira'), @('warning','Heavy hostile approaching.','David'),
 @('objective','Objective complete. Proceed to extraction.','Zira'), @('unknown','还有活人吗？收到请回答。','Huihui')
)
$radioTokens = $radioCom.GetVoices()
foreach($radioLine in $radioLines){
 for($radioIndex=0;$radioIndex -lt $radioTokens.Count;$radioIndex++){if($radioTokens.Item($radioIndex).GetDescription().Contains($radioLine[2])){$radioCom.Voice=$radioTokens.Item($radioIndex);break}}
 $radioStream = New-Object -ComObject SAPI.SpFileStream
 $radioStream.Format.Type=22
 $radioStream.Open((Join-Path (Get-Location) ('voice-sources/'+$radioLine[0]+'.wav')),3,$false)
 $radioCom.AudioOutputStream=$radioStream
 $null=$radioCom.Speak($radioLine[1],0)
 $radioStream.Close()
 [System.Runtime.InteropServices.Marshal]::ReleaseComObject($radioStream) | Out-Null
}
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($radioCom) | Out-Null
