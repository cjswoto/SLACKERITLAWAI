#!/bin/bash
set -e

rpk topic create audit.prompts audit.responses ingest.events --replicas 1 --partitions 1 --config retention.ms=-1 --brokers $KAFKA_BOOTSTRAP
