#!/bin/bash
set -ev

# Update apt-get
apt-get -qq update;

# Install sundials
apt-get install -y libsundials-dev;
