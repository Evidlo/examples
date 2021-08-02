filename=test4.kdbx
password=password
keyfile=test4.key

entry_title=test
entry_user=user
entry_pass=pass

python - << EOF
from pykeepass import PyKeePass
kp = PyKeePass("${filename}", "${password}", "${keyfile}")
print(kp.entries)
EOF
