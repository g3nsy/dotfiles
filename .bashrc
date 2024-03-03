#
# ~/.bashrc
#

# If not running interactively, don't do anything.
[[ $- != *i* ]] && return

# history
shopt -s histappend
HISTCONTROL=ignoreboth
HISTSIZE=1000
HISTFILESIZE=200

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# aliases.
alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias gpt='tgpt --interactive'
alias youtube='youtube-viewer'
alias build='python setup.py sdist bdist_wheel'
alias dotfiles='cd ~/Documents/code/dotfiles/'
repo="~/Documents/calcurse"
alias calcurse="git -C $repo fetch;
                git -C $repo pull;
                calcurse --datadir $repo;
                git -C $repo add .;
                git -C $repo commit -m 'update';
                git -C $repo push"

# enable programmable completion features.
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

export PATH=/home/g3nsy/.local/bin:$PATH
export PATH=$PATH:/home/g3nsy/.spicetify

eval "$(starship init bash)"

