#!/bin/bash

USER=srguser
PW=wduw2g2d

echo ${PW} | sudo -S sh -c "echo \"${USER} ALL=(ALL) NOPASSWD:ALL\" > /etc/sudoers.d/10-${USER}"

echo ${PW} | sudo -S sh -c "service sudo restart"
