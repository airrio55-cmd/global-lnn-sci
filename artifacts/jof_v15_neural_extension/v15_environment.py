"""Installed-runtime attestation; capture does not install packages or run models."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,platform,importlib,importlib.metadata,sysconfig
PACKAGES={'torch':'torch','ncps':'ncps','numpy':'numpy','pandas':'pandas','scikit-learn':'sklearn','scipy':'scipy','lightgbm':'lightgbm','nbformat':'nbformat','joblib':'joblib','threadpoolctl':'threadpoolctl'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def snapshot():
 packages={};files={}
 for distname,module in PACKAGES.items():
  d=importlib.metadata.distribution(distname);m=importlib.import_module(module);packages[distname]=d.version
  root=Path(m.__file__).parent
  selected=[Path(m.__file__)]
  if distname=='torch':selected += [root/'lib/libtorch_cpu.so',root/'lib/libc10.so']+list(root.glob('_C*.so'))
  elif distname=='ncps':selected += sorted((root/'torch').glob('*.py'))
  else:selected += sorted(root.rglob('*.so'))
  selected += sorted(root.rglob('*.py'))+sorted(root.rglob('*.so'))
  files[distname]={str(p.relative_to(root)):sha(p) for p in sorted(set(selected)) if p.is_file()}
  sibling=root.parent/(module+'.libs')
  if sibling.is_dir():files[distname].update({'../'+str(p.relative_to(root.parent)):sha(p) for p in sorted(sibling.rglob('*')) if p.is_file()})
 return {'Python':platform.python_version(),'implementation':platform.python_implementation(),'platform':sysconfig.get_platform(),'python_binary_sha256':sha(Path(sys.executable).resolve()),'packages':packages,'installed_distribution_versions':{d.metadata['Name']:d.version for d in importlib.metadata.distributions()},'package_code_binary_sha256':files,'torch_threads':2,'device':'cpu','note':'Installed-runtime hashes, not downloaded-wheel hashes. Reproduction requires matching artifacts; version pins alone do not imply bitwise identity on different hardware.'}
def verify(path):
 expected=json.loads(Path(path).read_text());actual=snapshot()
 if expected!=actual:raise RuntimeError('Frozen execution environment mismatch; use a separately versioned amendment, not in-place changes')
 return True
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--capture',type=Path);p.add_argument('--verify',type=Path);a=p.parse_args()
 if a.capture:
  if a.capture.exists():raise FileExistsError(a.capture)
  a.capture.write_text(json.dumps(snapshot(),indent=2)+'\n')
 elif a.verify:verify(a.verify);print('ENVIRONMENT_PASS')
 else:p.error('Choose --capture or --verify')
