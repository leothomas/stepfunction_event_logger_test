import os

TAGS = {
    "Project": "smallsat",
    "Owner": f"{os.environ.get('OWNER', 'alukach')} - DevelopmentSeed",
    "Client": "nasa-impact",
    "Stack": os.environ.get("STAGE", "dev"),
}
