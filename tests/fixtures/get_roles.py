from datetime import datetime

get_roles_response = {
    "Roles": [
        {
            "Path": "string",
            "RoleName": "string",
            "RoleId": "string",
            "Arn": "string",
            "CreateDate": datetime(2015, 1, 1),
            "AssumeRolePolicyDocument": "string",
            "Description": "string",
            "MaxSessionDuration": 123,
            "PermissionsBoundary": {
                "PermissionsBoundaryType": "PermissionsBoundaryPolicy",
                "PermissionsBoundaryArn": "string",
            },
            "Tags": [
                {"Key": "string", "Value": "string"},
            ],
            "RoleLastUsed": {"LastUsedDate": datetime(2015, 1, 1), "Region": "string"},
        },
    ],
    "IsTruncated": True | False,
    "Marker": "string",
}
