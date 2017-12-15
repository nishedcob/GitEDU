# coding: utf-8
import subprocess
import re
command = ["git", "show", "HEAD"]
cmd = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
commit_id_regex = re.compile("commit ([0-9a-f]*)\\\\n")
commit_id_regex.findall(str(cmd.stdout))[0]
