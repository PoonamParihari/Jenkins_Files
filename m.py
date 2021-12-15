#!/usr/bin/python

import os
import subprocess
import string
import random
import cx_Oracle
import time
import config


bashfile=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
bashfile='/tmp/'+bashfile+'.sh'

file_name = open(bashfile, 'w')
script_name = """#!/bin/bash

# def variables
curl_header="http://microservices-syrius-claims-input.dev.tst.oc/v1/payload"

git_repo_=test-files

# functions
check_cygwin_packages() {
  # TODO
  #check if all required cygwin packages are installed - command (package-name)
  # - ts (moreutils)
  # - curl (curl)
  # - jq (jq)
  # - md5sum (coreutils)
  # - uuidgen (util-linux)
  echo
}

curl_post() {
  # call curl post and return curl response
  local _curl_post_url="${1}"
  local _curl_post_datafile="${2}"
  local _curl_post_response=""

  _curl_post_response=$(curl -X POST "${_curl_post_url}" \\
     --header "Content-Type: application/xml" \\
     --data @${_curl_post_datafile} 2>>./upload.log)
  echo $_curl_post_response
}

create_testfile() {
  # replaces uuid and generates md5 based filenames for the test files
  local _create_testfile_filename="${1}"
  local _create_testfile_response=""
  local _create_testfile_md5hash=""

  _create_testfile_md5hash=($(md5sum ${_create_testfile_filename}))
  cp ${_create_testfile_filename} ./TF_${_create_testfile_md5hash}.xml
  sed -i "s/###UUID###/`uuidgen | tr -d -`/g" ./TF_${_create_testfile_md5hash}.xml

  echo TF_${_create_testfile_md5hash}.xml
}


get_testfiles() {
  # TODO - special case: doppelzahlungen
  #
  test "${PWD##/test-files/}" != "${PWD}"
}
locate_testfile() {
  echo ""
}


# main
pushd . >/dev/null

case "${1}" in
  a*|A*)
    if [ -d "../data" ] ; then
      cd ../data
    fi

    for filename in ./*/*.xml; do
    echo -n "Executing LAS Test: "
    echo ${filename%/*} | sed -r 's/^.{2}//'

    create_testfile ${filename}

    kvuv_boid=$(curl_post ${curl_header} $}${filename})


    kvuv_boid="`echo ${_curl_post_response} | jq -r .data 2>/dev/null`"

    echo "Syrius KVUV Meldung BOID: $kvuv_boid"
    echo

    rm TF_${md5hash}.xml

    done
  ;;
  t*|T*)
    echo "Executing LAS Test: ${PWD##*/}"
    test_files=${@}
    for f in ${test_files[@]}
      do
        echo
        echo -n "Uploading " ${f}
        testfile=$(create_testfile ${f})
        echo " as:" ${testfile}
        curl_response=$(curl_post ${curl_header} ${testfile})
        echo "Syrius KVUV Meldung BOID: `echo ${curl_response} | jq -r .data 2>/dev/null`"
        #rm ${testfile}
    done
  ;;
  *)
    echo "Executing LAS Test: ${PWD##*/}"
    test_files=(
      "./*.xml"
    )
    for f in ${test_files[@]}
      do
        echo
        echo -n "Uploading " ${f}
        testfile=$(create_testfile ${f})
        echo " as:" ${testfile}
        curl_response=$(curl_post ${curl_header} ${testfile})
        echo "Syrius KVUV Meldung BOID: `echo ${curl_response} | jq -r .data 2>/dev/null`"
        rm ${testfile}
    done
  ;;
esac
popd >/dev/null
"""

file_name.write(script_name)
file_name.close()
os.chmod(bashfile, 0o755)
bashcmd=bashfile
subprocess.call(bashcmd, shell=True)

#Time needed after BOID creation
time.sleep(30)

#Change BOID to list element for which sql statement takes are variable
initBOIDHolder = curl_response
boIDHolder = [initBOIDHolder]

#connection is established with these credential and pwd is set as a env variable
def getConnection():
    connection = cx_Oracle.connect("usrname/password@hostname:1521/TCUSTAS7")
    return connection

#fetchs 3 colums and displays only "itsfachobjekt" column
def fetchData():
    connection = getConnection()
    cursor = connection.cursor()
    sql_fetch_data = ("select boid, itsfachobjekt, processid from asecust.KVUVMeldung where boid =:1", boIDHolder)
    cursor.execute(sql_fetch_data)
    for result in cursor:
        print(result[1])
    connection.commit()
    cursor.close()

fetchData()
