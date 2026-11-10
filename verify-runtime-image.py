"""Docker classic/config-ID and containerd/manifest-ID identity checks.
Expected identities and layer hashes are from the original SHA256-verified archive;
this does not relax any frozen runtime/source hash checks or run a model.
"""
import json,sys
CONFIG='sha256:cb7fdf00a342e756668faec689892d6d90c72fd0a3c13b8912ba9021d365de48'
MANIFEST='sha256:cb5442db779c72e32e7ab854ff2abd7ce9baf68d6fc46924803b428892ef130a'
LAYERS=['sha256:85ef42186c6e4a39394084c9d2de86c595663566aef9c44b97b5a4f4bf5d92c4','sha256:5f70bf18a086007016e948b04aed3b82103a36bea41755b6cddfaf10ace3c6ef']
ENV=['PATH=/usr/local/bin:/usr/bin:/bin','PYTHONPATH=/workspace/.jof-phase1-deps','PYTHONDONTWRITEBYTECODE=1','LANG=C.UTF-8','LC_ALL=C.UTF-8','HOME=/root','GIT_OPTIONAL_LOCKS=0','GIT_CONFIG_SYSTEM=/etc/gitconfig']
def verify(items):
 if not isinstance(items,list) or len(items)!=1:raise ValueError('Expected one inspected image')
 info=items[0]
 if info.get('Id') not in [CONFIG,MANIFEST]:raise ValueError('Unrecognized image identity')
 if (info.get('Os'),info.get('Architecture'))!=('linux','amd64'):raise ValueError('Unexpected image platform')
 if info.get('RootFS',{}).get('Type')!='layers' or info['RootFS'].get('Layers')!=LAYERS:raise ValueError('Image rootfs layer digests differ from archived payload')
 c=info.get('Config',{})
 if c.get('Entrypoint')!=['/workspace/.venvs/global-lnn-sci/bin/python','/opt/v15/verify_entry.py'] or c.get('WorkingDir')!='/repo':raise ValueError('Unexpected image entrypoint/workdir')
 if sorted(c.get('Env') or [])!=sorted(ENV):raise ValueError('Image environment differs from archived configuration')
 if c.get('User','') not in ['', 'root']:raise ValueError('Unexpected image user')
 return 'config-digest' if info['Id']==CONFIG else 'OCI-manifest-digest'
if __name__=='__main__':
 try:print('IMAGE_ID_LAYERS_CONFIG_PASS',verify(json.load(sys.stdin)))
 except (ValueError,KeyError,TypeError) as error:raise SystemExit('STOP: '+str(error))
