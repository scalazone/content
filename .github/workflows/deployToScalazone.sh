#!/usr/bin/env bash

set -e -o pipefail -u

TOKEN=$(curl -d 'client_id=web' -d 'username=gh-content' -d "password=$AUTH_PASSWORD" -d 'grant_type=password' "$AUTH_URL" | jq .access_token --raw-output)

json_res=$(curl --request POST \
  --url "${API_URL}courses/update" \
  --header "authorization: Bearer $TOKEN" \
  --header 'content-length: 0')

success_status=$(echo "$json_res" | jq '.success')

if [[ $success_status != "true" ]]; then
  errors=$(echo "$json_res" | jq -r '.errors[]?')
  if [[ $errors ]]; then
    for error in "${errors[@]}"; do
      echo "$error"
    done
  else
    echo "No errors provided with response"
  fi
  exit 1
fi
