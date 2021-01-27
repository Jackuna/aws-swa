#!/bin/bash
#
# Parameters
# $1 => Directory/Folder to search file.
# $2 => AWS Bucket subdirectories 
#       Example -- myAWSs3bucket/folderA/FolderB/FolderC
#	           1.) In case one want to put files in folderA, use folderA as $2
#                  2.) In case one want to put files in folderB, use folderA/folderB as $2
#                  3.) In case one want to put files in folderC, use folderA/folderB/folderC as $2
# $3 => Existense of file from Start date in format YYYYMMDD 
#       Example --
#                  1.) 20210104 -> 4th January 2021
#                  2.) 20201212 -> 12th December 2020
# $4 => Existense of file upto end date in format YYYYMMDD
#       Example --
#                  1.) 20200322 -> 22nd March 2020
#                  2.) 20201212 -> 12th December 2020
# $5 => File Filter 
#       Example -- We need only specific files from a folder.
#                  1.) 20200122_data_settlement.txt --> Use $5 as *_data_settlement.txt
#                  2.) salesdata-20201215100610.txt --> Use $5 as salesdata-*
#      
# 
# Task - Find similar 20200122_data_settlement.txt on location /usr/data/
#        File existence date range 20200322 (22nd March 2020) to 20210104 (4th January 2021)
#        Copy it to AWS S3 bucket's subfolder named as folderA 
#
#     
# Syntax -  ./copy_data_to_S3_via_Curl.sh <LocalFolderLocation> <S3BUCKET-DIRECTORY> <STARTDATE> <ENDDATE> <FILEFILTER>
#
# Usage
#
#        1.) With File Filter
#         ./copy_data_to_S3_via_Curl.sh /usr/data folderA 20200322 20210104  '*data_settlement.txt'
#
#        2.) Without File Filter
#         ./copy_data_to_S3_via_Curl.sh /usr/data folderA 20200322 20210104  
#        
#	 3.) Reinitiate left upload
#
#         ./copy_data_to_S3_via_Curl.sh 1 folderA
#
#
#  Flow 
#  1.) Script use find command to find all the files with parameters and write it to a file "/tmp/file_inventory.txt"
#  2.) For Loop is being used further ti read file inputs and do S3 operations using HTTPS API
#  3.) Script keeps removing the entries from inventory file after a successful upload.
#  4.) Script writes the successful and failed upload status within log file "/tmp/file_copy_status.log"
#  5.) Incase we want to interrupt and upload the remaining files later, comment line no 62
#        62 find $1 -newermt $3 \! -newermt $4   -iname "$5" >> $inventory
#      To avoid confusion run the script with same paramter.
#
#
# Author: Jackuna
#

# Bucket Data
bucket="mys3bucket-data"
s3_access_key="AKgtusjksskXXXXTQTW"
s3_secret_key="KSKKSIS HSNKSLS+ydRQ3Ya37A5NUd1V7QvEwDUZR"

# Files
inventory="/tmp/file_inventory.txt"
logme="/tmp/file_copy_status.log"


if  [ $# == 2 ]; then
  echo "`date` -  Initiating left file upload from old inventory " >> $logme

elif [ $# -eq 5 ]; then
  truncate -s 0 $inventory
  find $1 -newermt $3 \! -newermt $4   -iname "$5" >> $inventory
  echo "`date` - Initiating all file that contains string $5 and found between $3 - $4  upload from new inventory " >> $logme

elif [ $# -eq 4 ]; then
  truncate -s 0 $inventory
  find $1 -newermt $3 \! -newermt $4  >> $inventory
  sed -i 1d $inventory
  echo "`date` - Initiating all file found between $3 - $4  upload from new inventory " >> $logme

else
  echo " Some or all arguments Missing from CLI"
  echo " Usage :  ./copy_data_to_S3_via_Curl.sh <LocalFolderLocation> <S3BUCKET-DIRECTORY> <STARTDATE> <ENDDATE> <FILEFILTER>"
  echo " Open Script README section"
  exit 1
fi

file_list=`cat $inventory`
total_file_count=`cat $inventory|wc -l`


for local_file_val in $file_list; do
        aws_folder=$2
        aws_file_name=`echo $local_file_val| rev| cut -d '/' -f1 | rev`
        aws_filepath="/${bucket}/$aws_folder/$aws_file_name"

        # metadata
        contentType="application/x-compressed-tar"
        dateValue=`date -R`
        signature_string="PUT\n\n${contentType}\n${dateValue}\n${aws_filepath}"
        signature_hash=`echo -en ${signature_string} | openssl sha1 -hmac ${s3_secret_key} -binary | base64`


        curl -X PUT -T "$local_file_val" \
    -H "Host: ${bucket}.s3.amazonaws.com" \
    -H "Date: ${dateValue}" \
    -H "Content-Type: ${contentType}" \
    -H "Authorization: AWS ${s3_access_key}:${signature_hash}" \
        https://${bucket}.s3.amazonaws.com/$aws_folder/$aws_file_name

    if [ $? -gt 0 ]; then
            echo "`date` Upload Failed  $local_file_val to $bucket" >> $logme
    else
            echo "`date` Upload Success $local_file_val to $bucket" >> $logme
            count=$((count + 1))
            printf "\rCopy Status -  $count/$total_file_count - Completed "

            sleep 1
            sed -i "/\/$aws_file_name/d" $inventory
    fi

done;

