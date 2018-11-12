#!/usr/bin/env bash
function scandir(){
    local cur_dir parent_dir workdir
    workdir=$1
    cd ${workdir}
    if [ ${workdir} = "/" ]
    then
        cur_dir=""
    else
        cur_dir=$(pwd)
    fi

    for dirlist in $(ls ${cur_dir})
    do
        if test -d ${dirlist}
        then
            cd ${dirlist}
            scandir ${cur_dir}/${dirlist}
            cd ..
        else
            echo ${cur_dir}/${dirlist}
        fi
    done
}

if test -d $1
then
    scandir $1
elif test -f $1
then
    echo "input is a file but not a directory, please input another name"
    exit 1
else
    echo "the name you input doesn't exist, try another name"
    exit 1
fi