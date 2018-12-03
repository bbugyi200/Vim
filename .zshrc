###############
#  Oh-My-Zsh  #
###############
ZSH=/home/bryan/.oh-my-zsh/
ZSH_THEME="mytheme"
DEFAULT_USER="bryan"
DISABLE_AUTO_UPDATE="true"
DISABLE_AUTO_TITLE="true"

# 'sudo' plugin MUST remain near the end or (for some reason) it won't work
plugins=(git lpass vi-mode z zsh-autosuggestions sudo)

ZSH_CACHE_DIR=$HOME/.cache/oh-my-zsh
if [[ ! -d $ZSH_CACHE_DIR ]]; then
  mkdir $ZSH_CACHE_DIR
fi

ZSH_DISABLE_COMPFIX="true"  # disable warning messages whenever I use 'su' to login as root

source $ZSH/oh-my-zsh.sh

ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=242'

################################
#  Disable Aliases / Builtins  #
################################
# Disable aliases
arr=("ll" "gco")
for i in "${arr[@]}"; do
    unalias "$i" &> /dev/null
done

# Disable builtins
disable r

####################
#  Autocompletion  #
####################
autoload -U +X compinit && compinit -u
autoload -U +X bashcompinit && bashcompinit
for filename in ~/.bash-completions/*; do
    source "$filename"
done

_git 2> /dev/null  # hack to make git branch completion work
compdef __git_branch_names gco
compdef _command_names wim
compdef _task tt ti tpi ts to ta tg tgw tgr tga tin tmi tget
compdef _tmuxinator tm
compdef del=emerge
compdef get=emerge
compdef rcst=rc-service
compdef vman=man

#####################
#  Source Commands  #
#####################
source /usr/local/lib/aliases.sh
source /usr/local/lib/tmuxinator.zsh

##############
#  Settings  #
##############
setopt null_glob  # disables errors when GLOB pattern does not match
setopt globdots

#################
#  ZSH Aliases  #
#################
so() { unalias -a && source ~/.zshrc; }

# ---------- Suffix Aliases ----------
# Zathura
alias -s pdf="zathura"
alias -s epub="zathura"
alias -s djvu="zathura"
alias -s ps="zathura"
# LibreOffice
alias -s csv="libreoffice"
alias -s xls="libreoffice"
alias -s xlsx="libreoffice"
alias -s doc="libreoffice"
alias -s docx="libreoffice"
alias -s odt="libreoffice"
alias -s ppt="libreoffice"
alias -s pptx="libreoffice"
# Imv
alias -s xbm="imv -d"
alias -s png="imv -d"
alias -s pcx="imv -d"
alias -s jpg="imv -d"
alias -s jpeg="imv -d"
alias -s gif="imv -d"
# Miscellaneous
alias -s git="git clone"
alias -s html="google-chrome-stable"
alias -s avi="vlc"
alias -s txt="vim"

# ---------- Global Aliases ----------
alias -g :c="clear &&"
alias -g @@="&> /dev/null & disown"
alias -g ::="| grep -i -e"
alias -g :::="| grep -A 5 -B 5 -i -e"
alias -g :l="| less"
alias -g :L="tmux send-keys '!-2 | less' Enter Enter"
alias -g :w="watch -n 1"

##############
#  Bindings  #
##############
bindkey "^P" up-line-or-search
bindkey "^N" down-line-or-search

#############
#  Exports  #
#############
# I set this so the crontab would use vim for editing
export EDITOR=$(which vim)

# Fixes Mutt Background Issue (stays transparent) in TMUX
export TERM="rxvt-unicode-256color"

###################
#  Miscellaneous  #
###################
# Enable Core Dumps
ulimit -c unlimited

#so as not to be disturbed by Ctrl-S ctrl-Q in terminals:
stty -ixon

if [[ -d $PWD/.git ]] && [[ -d ~/.virtualenvs/$(basename $PWD) ]]; then
    workon $(basename $PWD) &> /dev/null
fi

# Starts ssh-agent automatically
if ! pgrep -u "$USER" ssh-agent > /dev/null; then
    ssh-agent > ~/.ssh-agent-thing
fi
if [[ "$SSH_AGENT_PID" == "" ]]; then
    eval "$(<~/.ssh-agent-thing)" > /dev/null
fi

# Needed for Eternal Command History
preexec() { log_shell_history "$1"; }

if [[ -f $PWD/.lzshrc ]]; then
    printf "\n*** ALERT: A Local zshrc File has been Sourced ***\n\n"
    source ".lzshrc"
fi

if (( $+commands[tag] )); then
  export TAG_SEARCH_PROG=ag  # replace with rg for ripgrep
  tag() { command tag "$@"; source ${TAG_ALIAS_FILE:-/tmp/tag_aliases} 2>/dev/null }
  alias ag=tag  # replace with rg for ripgrep
fi

if [[ "$(id -u)" = 0 ]]; then
    export PATH="/root/.local/bin:$PATH"
fi

function command_not_found_handler() {
    cmd="$1"; shift
    if [[ "${cmd}" == "+"* ]]; then
        funky_cmd="funky -a ${cmd:1}"
    elif [[ "${cmd}" == "-"* ]]; then
        funky_cmd="funky -r ${cmd:1}"
    else
        >&2 printf "%s\n" "zsh: command not found: ${cmd}"
        exit 127
    fi

    tmux send-keys "${funky_cmd}" "Enter"
}

[ -f ~/.local/share/funky/funky.sh ] && source ~/.local/share/funky/funky.sh
