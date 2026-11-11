"""Verify upload bundle signature, identity, target SDK and shipped offline assets."""
from pathlib import Path
import sys,subprocess,zipfile,re,xml.etree.ElementTree as ET
bundle=Path(sys.argv[1]);tool=Path(sys.argv[2]);root=Path(__file__).resolve().parents[1]
subprocess.run(['java','-jar',str(tool),'validate','--bundle='+str(bundle)],check=True)
verified=subprocess.run(['java','-m','jdk.jartool/sun.security.tools.jarsigner.Main','-verify',str(bundle)],capture_output=True,text=True)
assert verified.returncode==0 and 'jar verified.' in verified.stdout,'AAB signature verification failed: '+verified.stdout+verified.stderr
xml=subprocess.check_output(['java','-jar',str(tool),'dump','manifest','--bundle='+str(bundle),'--module=base'],text=True)
manifest=ET.fromstring(xml);android='{http://schemas.android.com/apk/res/android}'
config=(root/'app/build.gradle').read_text();code=re.search(r'versionCode\s+(\d+)',config).group(1);version=re.search(r"versionName\s+'([^']+)'",config).group(1)
assert manifest.attrib['package']=='pl.neonempire.game','Wrong production package'
assert manifest.attrib[android+'versionCode']==code and manifest.attrib[android+'versionName']==version,'Wrong version'
assert int(manifest.find('uses-sdk').attrib[android+'targetSdkVersion'])>=36,'Play submission requires API 36'
assert manifest.find('application').attrib.get(android+'debuggable','false')=='false','Release is debuggable'
with zipfile.ZipFile(bundle) as z:
 assert z.testzip() is None,'Corrupt AAB'
 assert any(n.startswith('META-INF/') and n.endswith(('.RSA','.DSA','.EC')) for n in z.namelist()),'Unsigned AAB'
 for file in (root/'app/src/main/assets').iterdir():
  if file.is_file():assert z.read('base/assets/'+file.name)==file.read_bytes(),'Asset mismatch: '+file.name
 assert not any('/lib/' in n and n.endswith('.so') for n in z.namelist()),'Review native libraries for 16 KB page size compatibility'
print('PASS: signed production AAB, '+version+' ('+code+'), target API 36+, non-debuggable, all offline assets and privacy policy, no bundled native libraries')
