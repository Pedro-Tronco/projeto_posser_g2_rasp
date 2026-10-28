from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class BackendSettings(BaseModel):
    port: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter='__')
    
    backend: BackendSettings
    

def get_settings() -> Settings:
    return Settings() # type: ignore

