# ----------------------------------------------------------------------------
# ------------------------------ SOURCES -------------------------------------
source /home/bryan/Dropbox/dotfiles/extras/oh-my-zsh
source /home/bryan/Dropbox/dotfiles/extras/tmuxinator.zsh
source /home/bryan/Dropbox/dotfiles/extras/globrc

# -------------------------- OH-MY-ZSH ---------------------------------------
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=242'

# ----------------------------------- ALIASES --------------------------------

alias so='RUNNING_SOURCE_CMD=1 source ~/Dropbox/dotfiles/.zshrc'

# --- Suffix Aliases
# Zathura
alias -s pdf="zathura"
alias -s epub="zathura"
alias -s djvu="zathura"
alias -s ps="zathura"

# LibreOffice
alias -s doc="/usr/lib/libreoffice/program/soffice.bin --writer"
alias -s docx="/usr/lib/libreoffice/program/soffice.bin --writer"
alias -s odt="/usr/lib/libreoffice/program/soffice.bin --writer"
alias -s ppt="/usr/lib/libreoffice/program/soffice.bin --impress"

# Imv
alias -s xbm="imv"
alias -s png="imv"
alias -s pcx="imv"
alias -s jpg="imv"
alias -s jpeg="imv"

# Miscellaneous
alias -s git="git clone"
alias -s html="google-chrome-stable"


# --- Global Aliases
alias -g @@="&> /dev/null & disown"
alias -g X="&& exit"
alias -g ::="| grep"

# -------------------------------- BINDINGS ----------------------------------
bindkey "^P" up-line-or-search
bindkey "^N" down-line-or-search

# -------------------------------- FUNCTIONS ---------------------------------

# Starts ssh-agent automatically
if ! pgrep -u "$USER" ssh-agent > /dev/null; then
    ssh-agent > ~/.ssh-agent-thing
fi
if [[ "$SSH_AGENT_PID" == "" ]]; then
    eval "$(<~/.ssh-agent-thing)" > /dev/null
fi

# Needed for Eternal Command History
precmd() { eval "$PROMPT_COMMAND" }

command_not_found_handler() {
    WORD=$1; shift
    LocalAlias -x $WORD -- "$@"
}

if [[ -f $PWD/.lzshrc ]] && [[ -z "$RUNNING_SOURCE_CMD" ]]; then
    source ".lzshrc"
    printf "*** ALERT: Sourced Local zshrc File ***\n\n"
fi

compdef __git_branch_names gff gco
compdef _task tt ti tpi ts to ta tg tgw tgr tga
