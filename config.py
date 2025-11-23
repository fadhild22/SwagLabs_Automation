class Config:
    BASE_URL = "https://www.saucedemo.com/"
    
    CREDENTIALS = {
        "valid": {
            "username": "standard_user",
            "password": "secret_sauce"
        },
        "locked": {
            "username": "locked_out_user",
            "password": "secret_sauce"
        },
        "problem": {
            "username": "problem_user",
            "password": "secret_sauce"
        },
        "glitch": {
            "username": "performance_glitch_user",
            "password": "secret_sauce"
        },
        "invalid_user": {
            "username": "",
            "password": "secret_sauce"
        },
        "invalid_pass": {
            "username": "standard_user",
            "password": ""
        },
        "empty_user": {
            "username": "",
            "password": ""
        }
    }  
    
