#!/bin/bash

# Preparing SSH connection
mkdir -p ${HOME}/.ssh
echo "$PRIVATE_KEY" > ${HOME}/.ssh/id_rsa
echo "$PUBLIC_KEY" > ${HOME}/.ssh/id_rsa.pub
chmod 600 ${HOME}/.ssh/id_rsa
chmod 600 ${HOME}/.ssh/id_rsa.pub
ssh-keyscan -t rsa github.com >> ${HOME}/.ssh/known_hosts

# Git config
git config --global user.email "$USER_EMAIL"
git config --global user.name "$USER_NAME"

git clone git@github.com:$REPOSITORY.git .
python main.py

git add .
git commit -m "Auto update: $(date)"
git push origin master