#!/usr/bin/env bash
function scandir(){
    local cur_dir parent_dir workdir outputdir
    workdir=$1
    outputdir=$2
    echo "output directory is ${outputdir}"
    if [ ! -d ${outputdir} ]
    then
        mkdir ${outputdir}
    else
        echo "output directory exists"
    fi
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
            if [ ! -d ${outputdir}/${dirlist} ]
            then
                mkdir ${outputdir}/${dirlist}
            else
                rm -r ${outputdir}/${dirlist}
                mkdir ${outputdir}/${dirlist}
            fi
            cd ${dirlist}
#            scandir ${cur_dir}/${dirlist}
            for zip_file in $(ls | grep zip)
            do
                if [ -d ${zip_file%".zip"} ]
                then
                    rm -r ${zip_file%".zip"}
                fi
                unzip ${zip_file}
            done
            if [ ! -d ${outputdir}/${dirlist}/original ]
            then
                mkdir ${outputdir}/${dirlist}/original
                mv PATIENT_DICOM/* ${outputdir}/${dirlist}/original/
                rm -r PATIENT_DICOM
            fi

            if [ ! -d ${outputdir}/${dirlist}/vtks ]
            then
                mkdir ${outputdir}/${dirlist}/vtks
                mv MESHES_VTK/* ${outputdir}/${dirlist}/vtks/
                rm -r MESHES_VTK
            fi

            if [ ! -d ${outputdir}/${dirlist}/sematic_mask ]
            then
                mkdir ${outputdir}/${dirlist}/sematic_mask
                mv LABELLED_DICOM/* ${outputdir}/${dirlist}/sematic_mask/
                rm -r LABELLED_DICOM
            fi

            cd MASKS_DICOM
            for mask_name in $(ls)
            do
                mv ${mask_name} ${outputdir}/${dirlist}/
            done
            cd ..
            rm -r MASKS_DICOM
            cd ..
        else
            echo ${cur_dir}/${dirlist}
        fi
    done
}

if test -d $1
then
    scandir $1 $2
elif test -f $1
then
    echo "input is a file but not a directory, please input another name"
    exit 1
else
    echo "the name you input doesn't exist, try another name"
    exit 1
fi