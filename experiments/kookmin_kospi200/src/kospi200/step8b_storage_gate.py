"""Pre-release NPZ schema gate; no financial model fitting or pickle loading."""
import zipfile
from numpy.lib import format
from .data import BlockedError

def inspect_safe_npz(path):
 schema={}
 with zipfile.ZipFile(path) as archive:
  for name in archive.namelist():
   if not name.endswith('.npy'):raise BlockedError('Unexpected archive member')
   with archive.open(name) as stream:
    version=format.read_magic(stream)
    if version not in [(1,0),(2,0)]:raise BlockedError('Unsupported NPY header version')
    reader=format.read_array_header_1_0 if version==(1,0) else format.read_array_header_2_0
    shape,fortran,dtype=reader(stream)
   schema[name[:-4]]={'shape':list(shape),'dtype':str(dtype),'hasobject':dtype.hasobject}
 if any(v['hasobject'] for v in schema.values()):raise BlockedError('Persisted input contains object dtype; requires Unicode date serialization and fresh preflight/release')
 return schema
