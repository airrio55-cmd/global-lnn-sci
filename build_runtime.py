from pathlib import Path
import shutil,subprocess,concurrent.futures,re,json,hashlib,tarfile,os
BASE=Path('/workspace/v15_container_transfer');ROOT=BASE/'rootfs';ROOT.mkdir(exist_ok=True)
PREFIX=Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python')
def copy(path):
 path=Path(path);dest=ROOT/str(path).lstrip('/')
 if dest.exists():return
 dest.parent.mkdir(parents=True,exist_ok=True)
 if path.is_dir():shutil.copytree(path,dest,symlinks=True)
 else:shutil.copy2(path,dest,follow_symlinks=True)
copy('/workspace/.venvs/global-lnn-sci/lib');copy('/workspace/.venvs/global-lnn-sci/pyvenv.cfg');copy('/workspace/.venvs/global-lnn-sci/bin');copy('/workspace/.jof-phase1-deps')
for folder in ['bin','lib']:
 src=PREFIX/folder;dest=ROOT/str(src).lstrip('/');dest.parent.mkdir(parents=True,exist_ok=True)
 shutil.copytree(src,dest,symlinks=True,ignore=shutil.ignore_patterns('site-packages') if folder=='lib' else None,dirs_exist_ok=True)
for src in ['/usr/local/bin/git','/usr/bin/bash','/usr/bin/env']:copy(src)
elf=[]
for f in ROOT.rglob('*'):
 if f.is_file() and not f.is_symlink():
  with f.open('rb') as stream:
   if stream.read(4)==b'\x7fELF':elf.append(Path('/')/f.relative_to(ROOT))
def dependencies(f):
 result=subprocess.run(['ldd',str(f)],capture_output=True,text=True)
 return set(re.findall(r'(?:=>\s+|^\s*)(/[^\s]+)',result.stdout,re.M))
libs=set()
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for found in pool.map(dependencies,elf):libs.update(found)
for lib in sorted(libs):
 if Path(lib).is_file():copy(lib)
# dlopen/system locale resources; no user directories or credentials are copied.
for p in ['/usr/lib/locale/C.utf8','/usr/share/zoneinfo/UTC','/etc/ld.so.cache']:
 if Path(p).exists():copy(p)
(ROOT/'bin').mkdir(exist_ok=True);(ROOT/'bin/sh').symlink_to('/usr/bin/bash')
(ROOT/'etc').mkdir(exist_ok=True);(ROOT/'etc/passwd').write_text('root:x:0:0:root:/root:/usr/bin/bash\n');(ROOT/'etc/group').write_text('root:x:0:\n');(ROOT/'etc/nsswitch.conf').write_text('passwd: files\ngroup: files\nhosts: files dns\n');(ROOT/'etc/gitconfig').write_text('[safe]\n\tdirectory = /repo\n[core]\n\tfsmonitor = false\n')
for folder in ['tmp','root','repo','runs','authorization','opt/v15']:(ROOT/folder).mkdir(parents=True,exist_ok=True)
os.chmod(ROOT/'tmp',0o1777)
entry='''import sys,os,subprocess,json\nfrom pathlib import Path\nos.environ['PYTHONDONTWRITEBYTECODE']='1'\nsys.dont_write_bytecode=True\nrepo=Path('/repo');p=repo/'artifacts/jof_v15_neural_extension';sys.path.insert(0,str(p))\nmode=sys.argv[1] if len(sys.argv)>1 else 'verify'\nif mode=='verify':\n from v15_locking import check\n _,anchor=check(repo,p/'V15_CONFIG_LOCKED.json','/authorization/record.json')\n print('IMAGE_LOCK_ENVIRONMENT_PASS',anchor,flush=True)\nelif mode=='preflight':\n from v15_preflight_readonly import audit\n report=audit(repo);Path('/runs/preflight.json').write_text(json.dumps(report,indent=2)+'\\n');print('IMAGE_PREFLIGHT_PASS',report['groups'],len(report['folds']),flush=True)\nelif mode=='forward':\n from v15_smoke_no_fit import audit\n report=audit(repo);Path('/runs/forward.json').write_text(json.dumps(report,indent=2)+'\\n');print('IMAGE_FORWARD_PASS',report['forward_checks'],flush=True)\nelse:raise SystemExit('This transfer image entrypoint only verifies; training has not been started.')\n'''
(ROOT/'opt/v15/verify_entry.py').write_text(entry)
(BASE/'Dockerfile').write_text('''FROM scratch\nADD rootfs.tar /\nENV PATH=/usr/local/bin:/usr/bin:/bin PYTHONPATH=/workspace/.jof-phase1-deps PYTHONDONTWRITEBYTECODE=1 LANG=C.UTF-8 LC_ALL=C.UTF-8 HOME=/root GIT_OPTIONAL_LOCKS=0\nWORKDIR /repo\nENTRYPOINT ["/workspace/.venvs/global-lnn-sci/bin/python", "/opt/v15/verify_entry.py"]\n''')
with tarfile.open(BASE/'rootfs.tar','w') as tar:
 for p in ROOT.iterdir():tar.add(p,arcname=p.name)
(BASE/'build_manifest.json').write_text(json.dumps({'copied_runtime_only':True,'no_user_home_credentials_or_repository_in_image':True,'dependency_libraries':sorted(libs),'ELF_files_checked':len(elf),'rootfs_tar_bytes':(BASE/'rootfs.tar').stat().st_size},indent=2)+'\n')
print('ROOTFS_READY',len(elf),'ELF files,',len(libs),'libraries',flush=True)
