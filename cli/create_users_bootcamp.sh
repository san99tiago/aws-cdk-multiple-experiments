#!/bin/bash

# CREATE USERS UNDER MY IAM IDENTITY CENTER

IAM_IDENTITY_CENTER_ID=$1

# List of users
users=(
    "santi"
    "moni"
    "manu"
)

# Loop through each user
for user in "${users[@]}"
do
    # Define given name and family name
    given_name=$user
    family_name=$user

    echo "Creating user: $user ..."
    aws identitystore create-user --identity-store-id $IAM_IDENTITY_CENTER_ID --user-name "$user" --name="{\"GivenName\":\"$given_name\",\"FamilyName\":\"$family_name\"}" --display-name "$user" --no-cli-pager
done
