import subprocess
import textblob
cmd = ['python3','-m','textblob.download_corpora']
subprocess.run(cmd)
