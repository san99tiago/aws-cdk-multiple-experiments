from aws_cdk import aws_kms


key = aws_kms.Key(
    "a",
    "b",
    
)

key1 = aws_kms.CfnReplicaKey(
    "a", 
    "b",
    primary_key_arn="",
    key_policy=
)