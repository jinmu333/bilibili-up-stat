
import logging
import os
import requests

from fastapi import FastAPI
from pydantic import BaseModel, BaseSettings


app = FastAPI()
_logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    cookie: str

    class Config:
        env_file = os.environ.get("ENV_FILE", ".env")


settings = Settings()


class UpData(BaseModel):
    mid: int
    follower: int
    view: int
    likes: int


HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.39",
    "cookie": settings.cookie
}
STAT_URL = "https://api.bilibili.com/x/relation/stat?vmid={mid}&jsonp=jsonp"
UPSTAT_URL = "https://api.bilibili.com/x/space/upstat?mid={mid}&jsonp=jsonp"


@app.get("/upstat", response_model=UpData, tags=["bilibili"])
def upstat(mid: str):
    stat = requests.get(url=STAT_URL.format(mid=mid), headers=HEADERS).json()
    upstat = requests.get(url=UPSTAT_URL.format(
        mid=mid), headers=HEADERS
    ).json()
    res = UpData(
        mid=mid, follower=stat["data"]["follower"],
        view=upstat["data"]["archive"]["view"],
        likes=upstat["data"]["likes"]
    )
    _logger.info(res)
    return res
