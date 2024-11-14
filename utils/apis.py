from openbb import obb

# Function to check API credentials
def verify_api_credentials(token):
    """Attempts to log in and verify if OpenBB API credentials are valid."""
    try:
        obb.account.login(pat=token)
        if obb.user.credentials:
            obb.user.preferences.output_type = "dataframe"
            return "success"
        else:
            return "fail"
    except Exception as e:
        return f"error: {str(e)}"
