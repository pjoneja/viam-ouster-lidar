#!/bin/sh
cd `dirname $0`

exec python3 module.py "$@"  # viam-server will pass the socket path as a command line argument here