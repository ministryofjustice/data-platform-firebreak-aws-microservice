# ROLES

GET
`/roles/`

- list roles read from AWS
- paginated (fastapi, boto3)
- return response from boto3
  https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/list_roles.html
- convert response data e.g. camelcase to underscore\_
  - ReturnResponse models

`/roles/<rolename>/`

- detail of role
- include https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/list_role_policies.html

`/roles/<rolename>/policies/`

- list all policy documents
- response size limit??

OR list policy names and then
`/roles/<rolename>/policies/<policyname>/`

- policy documents

POST create
`/roles/`
Expected data:

- rolename - required - up to the client to define
  - validate role does not already exist
- Create role and trust policy (defaults)
- Add attach policies (defaults)
  Response:
- statuscode
- role arn
- error message (if applicable)

Notes:

- Base policies stored as json files in the repo - take out of the code
- Need to accept variables to build up for each user
  https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam/client/create_role.html

POST
`/roles/<rolename>/datasource/`

- Grant access to a s3bucket/folder
- Creates or updates the s3 policy
  Data:
- name
- access_level
- paths
  Response:
- statuscode
- arn
- error message (if applicable)

DELETE
`/roles/<rolename>/`

- Delete the role

TBC

- Format/how to store for policies
- Error messages
