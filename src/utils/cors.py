def get_origins_list(cors_origins_str: str):
    if cors_origins_str == "*":
        origins_list = ["*"]
    else:
        origins_list = [origin.strip() for origin in cors_origins_str.split(",")]
    
    return origins_list