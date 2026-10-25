"""Build a signed offline Android APK with official SDK tools and the standard library."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import zipfile

PROJECT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--build-tools', default=os.environ.get('ANDROID_BUILD_TOOLS'))
parser.add_argument('--platform-jar', default=os.environ.get('ANDROID_PLATFORM_JAR'))
parser.add_argument('--java-home', default=os.environ.get('JAVA_HOME'))
parser.add_argument('--work', type=Path, default=PROJECT.parent.parent / 'work' / 'ember-android-build')
parser.add_argument('--output', type=Path, default=PROJECT.parent / 'ember-front-0.76.0.apk')
args = parser.parse_args()
if not all([args.build_tools, args.platform_jar, args.java_home]):
    parser.error('Set --build-tools, --platform-jar and --java-home, or their documented environment variables.')
tools, platform, jdk = Path(args.build_tools).resolve(), Path(args.platform_jar).resolve(), Path(args.java_home).resolve()
work, output = args.work.resolve(), args.output.resolve()
work.mkdir(parents=True, exist_ok=True)
output.parent.mkdir(parents=True, exist_ok=True)
java = jdk / 'bin' / ('java.exe' if os.name == 'nt' else 'java')
javac = jdk / 'bin' / ('javac.exe' if os.name == 'nt' else 'javac')
keytool = jdk / 'bin' / ('keytool.exe' if os.name == 'nt' else 'keytool')
aapt = tools / ('aapt2.exe' if os.name == 'nt' else 'aapt2')
align = tools / ('zipalign.exe' if os.name == 'nt' else 'zipalign')
for required in [java, javac, keytool, aapt, align, platform, tools / 'lib/d8.jar', tools / 'lib/apksigner.jar']:
    if not required.is_file():
        raise SystemExit('Missing tool: ' + str(required))
env = dict(os.environ, JAVA_HOME=str(jdk))
def run(command):
    # aapt2 on Windows can misinterpret non-ASCII absolute paths. Keep project/SDK
    # arguments relative to the common workspace, whose child names are ASCII.
    cwd = PROJECT.parent.parent
    normalized = [command[0]]
    for argument in command[1:]:
        if isinstance(argument, Path):
            try:
                argument = argument.relative_to(cwd)
            except ValueError:
                pass
        normalized.append(argument)
    print('> ' + Path(str(command[0])).name + ' ' + ' '.join(map(str, command[1:3])), flush=True)
    subprocess.run(list(map(str, normalized)), env=env, cwd=cwd, check=True)

# Private signing material stays outside the deliverable/source project and is reused for updates.
signing = work.parent / 'ember-android-signing'
signing.mkdir(exist_ok=True)
password_file, keystore = signing / 'password.txt', signing / 'release.p12'
if not password_file.exists():
    password_file.write_text(secrets.token_urlsafe(32), encoding='ascii')
env['EMBER_ANDROID_PASSWORD'] = password_file.read_text(encoding='ascii').strip()
if not keystore.exists():
    run([keytool, '-genkeypair', '-keystore', keystore, '-storetype', 'PKCS12', '-alias', 'ember-release',
         '-keyalg', 'RSA', '-keysize', '3072', '-validity', '40000', '-dname', 'CN=Ember Front',
         '-storepass:env', 'EMBER_ANDROID_PASSWORD', '-keypass:env', 'EMBER_ANDROID_PASSWORD'])

assets = work / 'assets' / 'game'
assets.mkdir(parents=True, exist_ok=True)
index = (PROJECT / 'index.html').read_text(encoding='utf-8')
index = index.replace('</head>', '<script>try{if(!localStorage.getItem("ember-front-record"))localStorage.setItem("ember-front-record",JSON.stringify({difficulty:"normal",campaignVersion:24,storySkipVersion:25}));}catch(e){}</script><style>html,body{margin:0!important;background:#10191f!important}#frame{box-shadow:none!important;max-width:100vw!important;max-height:100dvh!important}body{gap:0!important}</style></head>')
(assets / 'index.html').write_text(index, encoding='utf-8')
runtime = ['vehicles-v74.js','depth-v67.js','signal-branch.js','engine.js','frontline.js','story.js','campaign-story.js','story-events.js','characters.js','audio.js','orbital-v44.js','mechanical-v45.js','battlefield.css','art-direction.css','operation-ui.css','story-ui.css','evacuation-ui.css']
corpus=index
for name in runtime:
    shutil.copy2(PROJECT/name,assets/name)
    corpus+=(PROJECT/name).read_text(encoding='utf-8')
asset_source=PROJECT/'assets'
for source in asset_source.glob('*.js'):
    corpus+=source.read_text(encoding='utf-8')
for source in asset_source.iterdir():
    if source.is_dir():
        shutil.copytree(source,assets/'assets'/source.name,dirs_exist_ok=True,ignore=(lambda directory,names:{name for name in names if name.startswith('score-') and name.endswith(('.ogg','.wav')) and Path(name).stem not in corpus}) if source.name=='audio' else None)
    elif source.name in corpus or source.name=='CREDITS.md':
        dest=assets/'assets'/source.name
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,dest)

native = PROJECT / 'android'
compiled = work / 'compiled-res.zip'
run([aapt, 'compile', '--dir', native / 'res', '-o', compiled])
resources = work / 'resources.apk'
run([aapt, 'link', '-o', resources, '-I', platform, '--manifest', native / 'AndroidManifest.xml',
     '--min-sdk-version', '26', '--target-sdk-version', '36', '--version-code', '76000', '--version-name', '0.76.0',
     '-A', work / 'assets', compiled])
classes = work / 'classes'
classes.mkdir(exist_ok=True)
run([javac, '-encoding', 'UTF-8', '--release', '8', '-Xlint:-options', '-classpath', platform,
     '-d', classes, *sorted((native / 'src').rglob('*.java'))])
classes_jar = work / 'classes.jar'
with zipfile.ZipFile(classes_jar, 'w', zipfile.ZIP_DEFLATED) as archive:
    for source in sorted(classes.rglob('*.class')):
        archive.write(source, source.relative_to(classes).as_posix())
dex = work / 'dex'
dex.mkdir(exist_ok=True)
run([java, '-cp', tools / 'lib/d8.jar', 'com.android.tools.r8.D8', '--release', '--lib', platform,
     '--min-api', '26', '--output', dex, classes_jar])
unsigned = work / 'unsigned.apk'
with zipfile.ZipFile(resources) as source, zipfile.ZipFile(unsigned, 'w') as archive:
    for entry in source.infolist():
        archive.writestr(entry.filename, source.read(entry.filename), compress_type=entry.compress_type)
    for source in dex.glob('*.dex'):
        archive.write(source, source.name, compress_type=zipfile.ZIP_DEFLATED)
aligned = work / 'aligned.apk'
run([align, '-f', '-P', '16', '4', unsigned, aligned])
run([java, '-jar', tools / 'lib/apksigner.jar', 'sign', '--ks', keystore, '--ks-key-alias', 'ember-release',
     '--ks-pass', 'env:EMBER_ANDROID_PASSWORD', '--key-pass', 'env:EMBER_ANDROID_PASSWORD',
     '--v1-signing-enabled', 'false', '--v2-signing-enabled', 'true', '--v3-signing-enabled', 'true',
     '--v4-signing-enabled', 'false', '--out', output, aligned])
run([java, '-jar', tools / 'lib/apksigner.jar', 'verify', '--verbose', '--print-certs', output])
run([align, '-c', '-P', '16', '4', output])
metadata = {'name': '代号 No.17', 'version': '0.76.0', 'package': 'com.emberfront.game', 'versionCode': 76000,
            'minAndroid': '8.0 (API 26)', 'targetApi': 36, 'offline': True,
            'permission': ['android.permission.VIBRATE'], 'architecture': 'universal (Java/WebView, no native libraries)',
            'bytes': output.stat().st_size, 'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
            'verification': 'apksigner v2/v3 signature and zipalign passed; device test not performed'}
output.with_suffix('.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
print('APK ready: ' + str(output), flush=True)
