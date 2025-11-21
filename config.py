class Config:
    BASE_URL = "https://www.saucedemo.com/"
    
    # Library credentials for different user scenarios
    CREDENTIALS = {
        "valid": {
            "username": "standard_user",
            "password": "secret_sauce"
        },
        "locked": {
            "username": "locked_out_user",
            "password": "secret_sauce"
        },
        "invalid_user": {
            "username": "dada",
            "password": "secret_sauce"
        },
        "invalid_pass": {
            "username": "standard_user",
            "password": ""
        },
        "empty_user": {
            "username": "",
            "password": "secret_sauce"
        }
    }