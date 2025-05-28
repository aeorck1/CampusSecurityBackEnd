import os

import dotenv

dotenv.load_dotenv() # Load .env variables


class EnvironmentVariables:

    API_SERVER_URL: str = os.environ.get('API_SERVER_URL', 'http://localhost:8000')

    APP_SERVER_URL: str = os.environ.get('APP_SERVER_URL', 'http://localhost:5173')

    DEBUG: bool = os.environ.get('DEBUG', 'False') == 'True'

    PRODUCTION: bool = os.environ.get('PRODUCTION', 'False') == 'True'

    MEDIA_SELF_SERVE: bool = os.environ.get('MEDIA_SELF_SERVE', 'True') == 'True'

    USE_S3: bool = os.getenv('USE_S3') == 'True'

    USE_CLOUDINARY: bool = os.getenv('USE_CLOUDINARY') == 'True'

    AWS_ACCESS_KEY_ID: str = os.environ.get('AWS_ACCESS_KEY_ID')

    AWS_SECRET_ACCESS_KEY: str = os.environ.get('AWS_SECRET_ACCESS_KEY')

    AWS_STORAGE_BUCKET_NAME: str = os.environ.get('AWS_STORAGE_BUCKET_NAME')

    AWS_S3_REGION_NAME: str = os.environ.get('AWS_S3_REGION_NAME')

    CLOUDINARY_CLOUD_NAME: str = os.environ.get('CLOUDINARY_CLOUD_NAME')

    CLOUDINARY_API_KEY: str = os.environ.get('CLOUDINARY_API_KEY')

    CLOUDINARY_API_SECRET: str = os.environ.get('CLOUDINARY_API_SECRET')

    CLOUDINARY_API_PROXY: str = os.environ.get('CLOUDINARY_API_PROXY')

    DEFAULT_DATABASE_NAME: str = os.environ.get('DEFAULT_DATABASE_NAME', 'campussecurity')

    DEFAULT_DATABASE_USER: str = os.environ.get('DEFAULT_DATABASE_USER', 'campussecurity')

    DEFAULT_DATABASE_PASSWORD: str = os.environ.get('DEFAULT_DATABASE_PASSWORD')

    DEFAULT_DATABASE_HOST: str = os.environ.get('DEFAULT_DATABASE_HOST')

    DEFAULT_DATABASE_PORT: str = os.environ.get('DEFAULT_DATABASE_PORT')

    EMAIL_HOST: str = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')

    EMAIL_PORT: str = os.environ.get('EMAIL_PORT', 587)

    EMAIL_USE_TLS: str = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'

    EMAIL_HOST_USER: str = os.environ.get('EMAIL_HOST_USER')

    EMAIL_HOST_PASSWORD: str = os.environ.get('EMAIL_HOST_PASSWORD')

    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY')

    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", 'HS256')

    JWT_ACCESS_TOKEN_LIFETIME: int = int(os.environ.get('JWT_ACCESS_TOKEN_LIFETIME', 1)) # In hours (1 hr)

    JWT_REFRESH_TOKEN_LIFETIME: int = int(os.environ.get('JWT_REFRESH_TOKEN_LIFETIME', 168)) # In hours (7 days)

