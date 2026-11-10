"""V15.1 prepare-only: verify backup/source jobs and copy valid jobs; never train."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib,tarfile,shutil,datetime
ROOT=Path('/repo');OUT=Path('/runs');SOURCE=Path('/source');BACKUP=Path('/backup/source.tar.gz');FROZEN=ROOT/'artifacts/jof_v15_neural_extension';AUTH=Path('/authorization/record.json')
sys.path.insert(0,str(FROZEN));sys.path.insert(0,str(Path(__file__).parent))
import base_v15_0_ops as ops

def verify_code():
 manifest=json.loads(Path(__file__).with_name('version_manifest.json').read_text())
 for name,digest in manifest['files_sha256'].items():
  if ops.sha(Path(__file__).parent/name)!=digest:raise ValueError('Recovery code drift:'+name)
 return manifest

def verify_backup(expected):
 if ops.sha(BACKUP)!=expected:raise ValueError('Backup SHA mismatch;do not train')
 count=0;seen=set();old_record=json.loads((SOURCE/'authorization.json').read_text());run_id=old_record['run_id']
 with tarfile.open(BACKUP,'r:gz') as archive:
  for member in archive:
   path=Path(member.name)
   if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0]!=run_id:raise ValueError('Unexpected backup member')
   rel=Path(*path.parts[1:])
   if member.isdir():continue
   if not member.isfile():raise ValueError('Nonregular backup member')
   stream=archive.extractfile(member);h=hashlib.sha256()
   for chunk in iter(lambda:stream.read(1048576),b''):h.update(chunk)
   if not (SOURCE/rel).is_file() or ops.sha(SOURCE/rel)!=h.hexdigest():raise ValueError('Backup/source drift:'+str(rel))
   seen.add(str(rel));count+=1
 actual={str(p.relative_to(SOURCE)) for p in SOURCE.rglob('*') if p.is_file()}
 if seen!=actual:raise ValueError('Backup/source file inventory differs')
 return {'sha256':expected,'source_run_id':run_id,'verified_files':count}

def main():
 import v15_locked_runner as runner
 verify_code();cfg,anchor=runner.check_lock(ROOT,FROZEN/'V15_CONFIG_LOCKED.json',AUTH,require_execution=True)
 authorization=json.loads(AUTH.read_text());backup=verify_backup(authorization['source_backup_sha256'])
 oldauth=json.loads((SOURCE/'authorization.json').read_text())
 if oldauth['locked_commit']!=anchor or oldauth['sha256']!=authorization['sha256']:raise ValueError('Source authorization not same locked protocol')
 for name,digest in json.loads((SOURCE/'operations_sha256.json').read_text()).items():
  if ops.sha(SOURCE/'operations'/name)!=digest:raise ValueError('Old operation snapshot drift')
 oldstate=json.loads((SOURCE/'job_status.json').read_text());jobs=json.loads((FROZEN/'step4/job_manifest.json').read_text())['jobs'];byid={j['fit_id']:j for j in jobs};v14=runner.v14_module(ROOT);context={};reused={};quarantined=[]
 if (OUT/'recovery_plan.json').exists() or (OUT/'results').exists():raise ValueError('Recovery preparation already exists;never overwrite')
 (OUT/'results/fits').mkdir(parents=True)
 for job in jobs:
  jid=job['fit_id'];folder=SOURCE/'results/fits'/jid;recorded=oldstate['states'].get(jid)=='COMPLETE'
  if not folder.exists():
   if recorded:raise ValueError('Recorded complete job missing:'+jid)
   continue
  if recorded:
   prior=oldstate['completed_artifacts'][jid]
   for name,digest in prior['files_sha256'].items():
    if ops.sha(folder/name)!=digest:raise ValueError('Completed job SHA mismatch:'+jid+'/'+name)
  # Never treat a failed/partial folder as complete merely because it exists.
  try:verified=ops.check_job(job,SOURCE/'results',runner,v14,context)
  except Exception as error:
   if recorded:raise
   quarantined.append({'fit_id':jid,'action':'restart_from_epoch1_new_attempt','reason':str(error),'original_preserved_read_only':True});continue
  destination=OUT/'results/fits'/jid;shutil.copytree(folder,destination)
  for name,digest in verified['files_sha256'].items():
   if ops.sha(destination/name)!=digest:raise ValueError('Copied job drift:'+jid)
  verified.update({'provenance':'reused_verified_prior_job','source_run_id':backup['source_run_id'],'source_fit_id':jid,'source_was_recorded_complete':recorded});reused[jid]=verified
  print('REUSE_VERIFIED',len(reused),'/1080',jid,flush=True)
 unknown=[p.name for p in (SOURCE/'results/fits').iterdir() if p.is_dir() and p.name not in byid]
 if unknown:raise ValueError('Unknown source job folders:'+str(unknown))
 plan={'status':'PREPARED_ONLY_NO_NEW_TRAINING','version':'V15.1-job-level-recovery','base_payload_commit':anchor,'source_backup':backup,'reused_jobs':reused,'reused_count':len(reused),'new_fit_count':1080-len(reused),'quarantined_incomplete_jobs':quarantined,'no_optimizer_epoch_resume':True,'epochs_for_new_fits':60,'source_model_hyperparameters_unchanged':True,'code_manifest_sha256':ops.sha(Path(__file__).with_name('version_manifest.json')),'prepared_at_utc':ops.now(),'job_ids':list(byid)}
 ops.js(OUT/'recovery_plan.json',plan);ops.js(OUT/'preparation_complete.json',{'status':'READY_FOR_SEPARATE_RECOVERY_EXECUTION','reused_jobs':len(reused),'new_fits_required':1080-len(reused),'new_training_started':False,'analysis_executed':False,'recovery_plan_sha256':ops.sha(OUT/'recovery_plan.json'),'code_manifest_sha256':plan['code_manifest_sha256']})
 print('RECOVERY_PREPARATION_PASS',len(reused),'reused;',1080-len(reused),'new fits required;NO_NEW_TRAINING',flush=True)
if __name__=='__main__':main()
