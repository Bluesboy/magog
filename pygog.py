#!/usr/bin/env python3

import argparse
import os
import json
import urllib.request

# argparse
parser = argparse.ArgumentParser()
parser.add_argument("--clone-addr", type = str, help = "source repo url", required = True)
parser.add_argument("--repo-name", type = str, help = "repository name", required = True)
parser.add_argument("-m", "--mirror", action="store_true", help = "Repository will be a mirror. Default is false")
parser.add_argument("-p", "--private", action="store_true", help = "Repository will be private. Default is false")
parser.add_argument("--description", type = str, help = "Repository description")
parser.add_argument("--fqdn", type = str, help = "FQDN of target repos server")

token = os.environ['GOGSTOKEN']
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
