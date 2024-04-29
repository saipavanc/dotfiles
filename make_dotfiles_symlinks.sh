#!/bin/bash

# This script creates symlinks from the home directory to any desired dotfiles in ~/dotfiles
# using the options -s for symbolic, -f for force, -n for no dereference, -r for relative path

# enable seeing hidden files
shopt -s extglob
shopt -s dotglob

# make symlinks for .config
ln -snfr ./.config/* -t ~/.config/

# make symlinks for home
ln -snfr ./home/* -t ~/