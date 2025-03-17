#
# ~/.bash_profile
#

#[[ -f ~/.bashrc ]] && . ~/.bashrc
export SSH_AUTH_SOCK="$XDG_RUNTIME_DIR/ssh-agent.socket"

if [ x"$XDG_CURRENT_DESKTOP" = x"Sway" ] ; then 
  QT_QPA_PLATFORMTHEME=qt5ct
  export QT_QPA_PLATFORMTHEME
fi
