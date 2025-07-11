#!/usr/bin/env python3

import os
import json
import sys
import re

CONFIG_FILE = "/etc/jarvice/users.json"
BASE_PATH = os.environ.get("BASE_PATH", "/home")

def is_valid_name(name):
    # Only allow alphanumeric, dash, and underscore
    return re.fullmatch(r'[a-zA-Z0-9_-]+', name) is not None

def validate_uid_gid(value):
    return isinstance(value, int) and value >= 0

def recursive_chown(path, uid, gid):
    for root, dirs, files in os.walk(path):
        os.chown(root, uid, gid)
        for d in dirs:
            os.chown(os.path.join(root, d), uid, gid)
        for f in files:
            os.chown(os.path.join(root, f), uid, gid)

def create_dirs(config):
    for dirname, perms in config.items():
        if not is_valid_name(dirname):
            print(f"Skipping invalid directory name: '{dirname}'")
            continue

        uid = perms.get("uid")
        gid = perms.get("gid")

        if not validate_uid_gid(uid) or not validate_uid_gid(gid):
            print(f"Skipping '{dirname}' due to invalid uid/gid: uid={uid}, gid={gid}")
            continue

        path = os.path.join(BASE_PATH, dirname)

        try:
            os.makedirs(path, exist_ok=True)
            recursive_chown(path, uid, gid)
            print(f"Created and chowned recursively: {path} to {uid}:{gid}")
        except Exception as e:
            print(f"Failed to create/chown {path}: {e}")

def main():
    if not os.path.exists(CONFIG_FILE):
        print(f"Config file not found/supplied: {CONFIG_FILE}")
        sys.exit(0)

    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        sys.exit(1)

    if not isinstance(config, dict):
        print("Invalid JSON format: expected a top-level object with directory names.")
        sys.exit(1)

    create_dirs(config)

if __name__ == "__main__":
    main()
