#!/bin/bash

# took it from https://github.com/pardahlman/docker-rabbitmq-cluster

set -e

# Start RMQ from entrypoint.
# This will ensure that environment variables passed
/usr/local/bin/docker-entrypoint.sh rabbitmq-server -detached

sleep 5s
rabbitmqctl stop_app
rabbitmqctl join_cluster node1@rabbitmq1

rabbitmqctl stop
# Wait for the app to really stop
sleep 2s
# Start it
rabbitmq-server

