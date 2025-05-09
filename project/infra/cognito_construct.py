from constructs import Construct
from aws_cdk import aws_cognito as cognito

class UserPoolConstruct(Construct):

    def __init__(self, scope: Construct, id: str, user_db_lambda_arn: str = None) -> None:
        super().__init__(scope, id)

        # Define the user pool
        self.user_pool = cognito.UserPool(self, "UserPool",
            user_pool_name="TaskManagerUserPool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True, mutable=True),
                given_name=cognito.StandardAttribute(required=True, mutable=True),
                family_name=cognito.StandardAttribute(required=True, mutable=True),
                gender=cognito.StandardAttribute(required=True, mutable=True),
                birthdate=cognito.StandardAttribute(required=True, mutable=True),
            ),
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True,
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
        )

        # User Pool Client
        self.user_pool_client = cognito.UserPoolClient(self, "UserPoolClient",
            user_pool=self.user_pool
        )
