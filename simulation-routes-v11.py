from pathlib import Path
p=Path('simulate-campaign.cjs');s=p.read_text(encoding='utf-8').replace('let aim=106;',"const resource=r.entities.filter(o=>['rescue','shield'].includes(o.type)&&o.y>145&&o.y<500).sort((a,b)=>(b.type==='rescue'?150:0)+b.y-((a.type==='rescue'?150:0)+a.y))[0];let aim=resource?.x??216;")
s=s.replace('if(threat)aim=threat.x;else if(boss)aim=boss.x;',"if(threat&&threat.y>490)aim=threat.x;else if(boss&&!resource)aim=boss.x;")
s=s.replace("'balance-v9-report.json'", "'balance-v11-report.json'")
p.write_text(s,encoding='utf-8')
