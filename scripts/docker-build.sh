#!/bin/bash

set -e

_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

TAG="bossjones/boss-ansible-role-dnsmasq:latest"

docker build --tag "${TAG}" \
    --file "Dockerfile" $(pwd)

docker run \
	--name boss-dnsmasq \
	-d \
	-p 153:53/udp \
	-p 5380:8080 \
	-v ./virtualization/docker/dnsmasq.conf:/etc/dnsmasq.conf \
	--log-opt "max-size=100m" \
	-e "HTTP_USER=foo" \
	-e "HTTP_PASS=bar" \
	--restart always \
	"${TAG}"
