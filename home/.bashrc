#    _               _              
#   | |__   __ _ ___| |__  _ __ ___ 
#   | '_ \ / _` / __| '_ \| '__/ __|
#  _| |_) | (_| \__ \ | | | | | (__ 
# (_)_.__/ \__,_|___/_| |_|_|  \___|
# 
# by Stephan Raabe (2023)
# -----------------------------------------------------
# ~/.bashrc
# -----------------------------------------------------

# If not running interactively, don't do anything
[[ $- != *i* ]] && return
PS1='[\u@\h \W]\$ '

# Define Editor
export EDITOR=nvim

# -----------------------------------------------------
# ALIASES
# -----------------------------------------------------

alias c='clear'
alias nf='neofetch'
alias pf='pfetch'
alias ls='eza -a --icons'
alias ll='eza -al --icons'
alias lt='eza -a --tree --level=1 --icons'
alias matrix='cmatrix'
alias wifi='nmtui'
alias winclass="xprop | grep 'CLASS'"

alias paruS="sudo pacman -Sy && sudo powerpill -Su && paru -Su"

export PATH="/usr/lib/cache/bin/:$PATH"

# -----------------------------------------------------
# START STARSHIP
# -----------------------------------------------------
if [[ "$TERM_PROGRAM" != "vscode" ]];
then
eval "$(starship init bash)"
fi
# -----------------------------------------------------
# PYWAL
# -----------------------------------------------------
# cat ~/.cache/wal/sequences

# -----------------------------------------------------
# FASTFETCH if on wm
# -----------------------------------------------------
echo ""
if [[ $(tty) == *"pts"* ]]; then
    fastfetch
else
    if [ -f /bin/qtile ]; then
        echo "Start Qtile X11 with command Qtile"
    fi
    if [ -f /bin/hyprctl ]; then
        echo "Start Hyprland with command Hyprland"
    fi
fi

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/home/saipavanchitta/mambaforge/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/home/saipavanchitta/mambaforge/etc/profile.d/conda.sh" ]; then
        . "/home/saipavanchitta/mambaforge/etc/profile.d/conda.sh"
    else
        export PATH="/home/saipavanchitta/mambaforge/bin:$PATH"
    fi
fi
unset __conda_setup

if [ -f "/home/saipavanchitta/mambaforge/etc/profile.d/mamba.sh" ]; then
    . "/home/saipavanchitta/mambaforge/etc/profile.d/mamba.sh"
fi
# <<< conda initialize <<<

