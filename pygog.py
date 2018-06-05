#!/usr/bin/env python3

import argparse
import os
import json
import urllib.request

# argparse
parser = argparse.ArgumentParser()
parser.add_argument("--cloneaddr", type = str, help = "source repo url", required = True)
# parser.add_argument("--reponame", type = str, help = "repository name", required = True)
parser.add_argument("-m", "--mirror", action="store_true", help = "Repository will be a mirror. Default is false")
parser.add_argument("-p", "--private", action="store_true", help = "Repository will be private. Default is false")
parser.add_argument("--description", type = str, help = "Repository description")
parser.add_argument("--fqdn", type = str, help = "FQDN of target repos server")
parser.add_argument("-o", "--owner", type = str, help = "Target repo owner", required = True)
args = parser.parse_args()

reponame = args.cloneaddr.split('/')[-1].split('.')[0]

token = os.environ['GOGSTOKEN']
user = os.environ['SOURCEUSER']
passwd = os.environ['SOURCEPASSWD']
headers = {
        'Authorization': "token {}".format(token),
        'Content-Type': "application/json",
        'Cache-Control': "no-cache"
        }

# function to get id of owner of target repo
def get_owner_id(owner, req_headers, target_fqdn):
    request = urllib.request.Request("http://{0}/api/v1/users/{1}".format(target_fqdn, owner), headers = req_headers, method = 'GET')
    with urllib.request.urlopen(request) as f:
        return json.loads(f.read().decode("utf-8"))['id']

# migrate function
def migrate(req_headers, repo_name, clone_addr, user_name, user_passwd, uid, description, private, target_fqdn):
    body = json.dumps({ "clone_addr" : clone_addr, "auth_username" : user_name, "auth_password": user_passwd, "uid" : uid, "description" : description, "private" : private, "repo_name" : repo_name }).encode()
    request = urllib.request.Request("http://{0}/api/v1/repos/migrate".format(target_fqdn), data = body, headers = req_headers, method = 'POST')
    with urllib.request.urlopen(request) as f:
        return json.loads(f.read().decode("utf-8"))

uid = get_owner_id(args.owner, headers, args.fqdn)
result = migrate(headers, reponame, args.cloneaddr, user, passwd, uid, args.description, args.private, args.fqdn)
print(json.dumps(result, indent = 4, ensure_ascii=False))
