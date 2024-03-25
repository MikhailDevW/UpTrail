from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DB_HOST: str = 'tawaluk.ru'
    DB_PORT: int = 5432
    DB_USER: str = 'uptrail_dev'
    DB_PASS: str = '1903marth'
    DB_NAME: str = 'uptrail_dev'

    @property
    def DatabaseUrlPsycopg(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    #model_config = SettingsConfigDict(env_file="UpTrail/db/.env_db_dev")

settings = Settings()
