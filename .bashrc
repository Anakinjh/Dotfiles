#My bash config. Not much to see here; just some pretty standard stuff.

### EXPORT
export TERM="xterm-256color"      
export HISTCONTROL=ignoredups:erasedups   
export EDITOR="vim"
export PATH="$HOME/.emacs.d/bin:$PATH"
export PATH="$HOME/.scripts/bin:$PATH"

### SET MANPAGER
### "vim" as manpager
export MANPAGER="vim +Man!"

### PATH
if [ -d "$HOME/.bin" ] ;
  then PATH="$HOME/.bin:$PATH"
fi

if [ -d "$HOME/.local/bin" ] ;
  then PATH="$HOME/.local/bin:$PATH"
fi

if [ -d "$HOME/.emacs.d/bin" ] ;
  then PATH="$HOME/.emacs.d/bin:$PATH"
fi

if [ -d "$HOME/Applications" ] ;
  then PATH="$HOME/Applications:$PATH"
fi

if [ -d "/var/lib/flatpak/exports/bin/" ] ;
  then PATH="/var/lib/flatpak/exports/bin/:$PATH"
fi

if [ -d "$HOME/.config/emacs/bin/" ] ;
  then PATH="$HOME/.config/emacs/bin/:$PATH"
fi
export PATH="/etc/profiles/per-user/anakin/bin:$PATH"

### SETTING OTHER ENVIRONMENT VARIABLES
if [ -z "$XDG_CONFIG_HOME" ] ; then
    export XDG_CONFIG_HOME="$HOME/.config"
fi
if [ -z "$XDG_DATA_HOME" ] ; then
    export XDG_DATA_HOME="$HOME/.local/share"
fi
if [ -z "$XDG_CACHE_HOME" ] ; then
    export XDG_CACHE_HOME="$HOME/.cache"
fi
export XMONAD_CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/xmonad" # xmonad.hs is expected to stay here
export XMONAD_DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/xmonad"
export XMONAD_CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/xmonad"

### CHANGE TITLE OF TERMINALS
case ${TERM} in
  xterm*|rxvt*|Eterm*|aterm|kterm|gnome*|alacritty|st|konsole*)
    PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME%%.*}:${PWD/#$HOME/\~}\007"'
        ;;
  screen*)
    PROMPT_COMMAND='echo -ne "\033_${USER}@${HOSTNAME%%.*}:${PWD/#$HOME/\~}\033\\"'
    ;;
esac

### ALIASES ###
# navigation
alias ..='cd ..'
alias ...='cd ../..'
alias .3='cd ../../..'
alias .4='cd ../../../..'
alias .5='cd ../../../../..'
alias cdnix="cd /etc/nixos/"

# vim and emacs
alias emacs="emacsclient -c -a 'emacs'" # GUI versions of Emacs
alias em="/usr/bin/emacs -nw" # Terminal version of Emacs
alias rem="killall emacs || echo 'Emacs server not running'; /usr/bin/emacs --daemon" # Kill Emacs and restart daemon..
alias emacsd="/etc/profiles/per-user/anakin/bin/emacs"

# Changing "ls" to "eza"
alias ls='eza -Alh --color=always --group-directories-first' 
alias la='eza -A --color=always --group-directories-first'  
alias ll='eza -l --color=always --group-directories-first'  
alias lt='eza -AT --color=always --group-directories-first' 
alias l.='eza -Al --color=always --group-directories-first ../' 
alias l..='eza -Al --color=always --group-directories-first ../../' 
alias l...='eza -Al --color=always --group-directories-first ../../../'
alias lnix="eza /etc/nixos/ --color=always --group-directories-first"

# Fixing spelling errors
alias celar='clear'
alias claer='clear'
alias pdw='pwd'
alias please='sudo !!'
alias clear="clear && fastfetch"
alias shutdown="shutdown -h now"
alias ranger="yazi"
alias suspend="sudo systemctl suspend"
alias pingq="ping -c 3 bitetheroses.com"

# NixOS shortcuts
alias nixswitch='sudo nixos-rebuild switch'
alias addpkg='sudo vim /etc/nixos/packages.nix'
alias nixi='yazi /etc/nixos'
alias degenerate='read -p "Input days: " days; sudo nix-collect-garbage --delete-older-than "${days}d"; sudo nixos-rebuild boot'
alias S-='sudo'

# adding flags
alias df='df -h'               # human-readable sizes
alias free='free -m'           # show sizes in MB
alias grep='grep --color=auto' # colorize output (good for log files)

# ps
alias psa="ps auxf"
alias psgrep="ps aux | grep -v grep | grep -i -e VSZ -e"
alias psmem='ps auxf | sort -nr -k 4'
alias pscpu='ps auxf | sort -nr -k 3'

# Merge Xresources
alias merge='xrdb -merge ~/.Xresources'

# git
alias addup='git add -u'
alias addall='git add .'
alias branch='git branch'
alias checkout='git checkout'
alias clone='git clone'
alias commit='git commit -m'
alias fetch='git fetch'
alias pull='git pull origin'
alias push='git push origin'
alias stat='git status'  # 'status' is protected name so using 'stat' instead
alias tag='git tag'
alias newtag='git tag -a'

# get error messages from journalctl
alias jctl="journalctl -p 3 -xb"

# gpg encryption
# verify signature for isos
alias gpg-check="gpg2 --keyserver-options auto-key-retrieve --verify"

# receive the key of a developer
alias gpg-retrieve="gpg2 --keyserver-options auto-key-retrieve --receive-keys"

# cryptsetup aliases
alias decrypt="sudo cryptsetup open /dev/sda1 Seagate-2TB && sudo mount /dev/mapper/Seagate-2TB /mnt/usb"
alias encrypt="sudo umount /mnt/usb && sudo cryptsetup close Seagate-2TB"

# change your default USER shell
alias tobash="sudo chsh $USER -s /bin/bash && echo 'Log out and log back in for change to take effect.'"
alias tozsh="sudo chsh $USER -s /bin/zsh && echo 'Log out and log back in for change to take effect.'"
alias tofish="sudo chsh $USER -s /bin/fish && echo 'Log out and log back in for change to take effect.'"

# bare git repo alias for managing my dotfiles
alias config="/usr/bin/git --git-dir=$HOME/dotfiles --work-tree=$HOME"

# termbin
alias tb="nc termbin.com 9999"
### SHOPT
shopt -s autocd # change to named directory
shopt -s cdspell # autocorrects cd misspellings
shopt -s cmdhist # save multi-line commands in history as single line
shopt -s dotglob
shopt -s histappend # do not overwrite history
shopt -s expand_aliases # expand aliases
shopt -s checkwinsize # checks term size when bash regains control

#ignore upper and lowercase when TAB completion
bind "set completion-ignore-case on"

### COUNTDOWN
cdown () {
    N=$1
  while [[ $((--N)) -gt  0 ]]
    do
        echo "$N" |  figlet -c | lolcat &&  sleep 1
    done
}

### Function extract for common file formats ###
SAVEIFS=$IFS
IFS=$(echo -en "\n\b")

### ARCHIVE EXTRACTION
# usage: ex <file>
function ex {
 if [ -z "$1" ]; then
    # display usage if no parameters given
    echo "Usage: ex <path/file_name>.<zip|rar|bz2|gz|tar|tbz2|tgz|Z|7z|xz|ex|tar.bz2|tar.gz|tar.xz>"
    echo "       extract <path/file_name_1.ext> [path/file_name_2.ext] [path/file_name_3.ext]"
 else
    for n in "$@"
    do
      if [ -f "$n" ] ; then
          case "${n%,}" in
            *.cbt|*.tar.bz2|*.tar.gz|*.tar.xz|*.tbz2|*.tgz|*.txz|*.tar)
                         tar xvf "$n"       ;;
            *.lzma)      unlzma ./"$n"      ;;
            *.bz2)       bunzip2 ./"$n"     ;;
            *.cbr|*.rar)       unrar x -ad ./"$n" ;;
            *.gz)        gunzip ./"$n"      ;;
            *.cbz|*.epub|*.zip)       unzip ./"$n"       ;;
            *.z)         uncompress ./"$n"  ;;
            *.7z|*.arj|*.cab|*.cb7|*.chm|*.deb|*.dmg|*.iso|*.lzh|*.msi|*.pkg|*.rpm|*.udf|*.wim|*.xar)
                         7z x ./"$n"        ;;
            *.xz)        unxz ./"$n"        ;;
            *.exe)       cabextract ./"$n"  ;;
            *.cpio)      cpio -id < ./"$n"  ;;
            *.cba|*.ace)      unace x ./"$n"      ;;
            *)
                         echo "ex: '$n' - unknown archive method"
                         return 1
                         ;;
          esac
      else
          echo "'$n' - file does not exist"
          return 1
      fi
    done
fi
}

IFS=$SAVEIFS

# navigation
up () {
  local d=""
  local limit="$1"

  # Default to limit of 1
  if [ -z "$limit" ] || [ "$limit" -le 0 ]; then
    limit=1
  fi

  for ((i=1;i<=limit;i++)); do
    d="../$d"
  done

  # perform cd. Show error if cd fails
  if ! cd "$d"; then
    echo "Couldn't go up $limit dirs.";
  fi
}

# ProtonVPN service through WireGuard
vpn () {
      config=("/etc/wireguard"/*.conf)
      random_config=${config[RANDOM % ${#config[@]}]}
      service="/tmp/vpn-service"
      case $1 in
        up)
          wg-quick up "$random_config"
          echo "$random_config" > "$service"
          ;;
        down)
          if [ -f "$service" ]; then
                current_config=$(cat "$service")
                wg-quick down "$current_config"
                rm "$service"
          else
                echo "VPN service is not running"
          fi
          ;;
        *)
          echo "Usage: vpn {up|down}"
          ;;
      esac
}

# run pywal to recolor the terminal
wal -i ~/Wallpapers/Untitled_Artwork.jpeg

# run fastfetch in each new terminal instance 
clear 
