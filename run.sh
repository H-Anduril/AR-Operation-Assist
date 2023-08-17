#!/bin/bash

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "Options:"
    echo " -b, --build     Build Docker Image 'goa_op_assist'"
    echo " -h, --help      Display help message"
    echo " -r, --run       Run Docker Container and Start Program"
}

has_argument() {
    [[ ("$1" == *=* && -n ${1#*=}) || ( ! -z "$2" && "$2" != -*)  ]];
}

extract_argument() {
  echo "${2:-${1#*=}}"
}

handle_options() {
    if [ $# -eq 0 ]; then
        usage
        exit 0
    fi
    while [ $# -gt 0 ]; do
        case $1 in
            -b | --build)
                docker build -t goa_op_assist .
                ;;
            -h | --help)
                usage
                exit 0
                ;;
            -r | --run)
                docker run -i -t --rm -p 1433:1433 -p 3000:3000 -v C:/Users/hw1048/Documents/AR-Operation-Assist/output:/usr/src/app/output  goa_op_assist
                ;;
            -s | --set-runner)
                docker run -d --name gitlab-runner --restart always \
                    -v /var/run/docker.sock:/var/run/docker.sock \
                    -v gitlab-runner-config:/etc/gitlab-runner \
                    gitlab/gitlab-runner:latest
                    
                docker run --rm -it -v gitlab-runner-config:/etc/gitlab-runner gitlab/gitlab-runner:latest register
                ;;

            *)
                # echo "Invalid option: $1" >&2
                usage
                exit 1
                ;;
        esac
        shift
    done
}

handle_options "$@"