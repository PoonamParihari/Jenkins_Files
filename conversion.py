l_header="http://microservices.blablabla/v1/payload"
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
 
    echo "Siry Meldung BOID: $kvuv_boid"
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
        echo "Siry Meldung BOID: `echo ${curl_response} | jq -r .data 2>/dev/null`"
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
        echo "Siry Meldung BOID: `echo ${curl_response} | jq -r .data 2>/dev/null`"
        rm ${testfile}
    done
  ;;
esac

popd >/dev/null
"""
f.write(s)
f.close()
os.chmod(bashfile, 0o755)
bashcmd=bashfile
for arg in sys.argv[1:]:
bashcmd += ' '+arg
subprocess.call(bashcmd, shell=True)
