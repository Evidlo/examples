#!/bin/bash

subdomain=home
domain=widloski.com

# get current interface
interface=$(ip route | awk '/default/{print $5;exit}')
# get address
address=$(ip -f inet addr show ${interface} | awk '/inet / {match($2,"[^/]+",a);print a[0]}')
# alternatively use ifconfig.me
# address=$(curl ifconfig.me)

# ----- namecheap -----
# password=
# url="https://dynamicdns.park-your-domain.com/update?host=${subdomain}&domain=${domain}&password=${password}&ip=${address}"

# ----- porkbun -----
id=
apikey=
secretapikey=
data='{
"apikey":"'${apikey}'",
"secretapikey":"'${secretapikey}'",
"name":"'${subdomain}'",
"type":"A",
"content":"'${address}'"
}'
url=https://porkbun.com/api/json/v3/dns/edit/${domain}/${id}

curl "${url}" --data "${data}"
