import asyncio
import random
from typing import Dict, Optional

from utils.request import DEFAULT_COOKIE, DEFAULT_HEADER, ROOT, BaseReq

from .graphql import GraphQL

HASHES = {
    "default": "02e14f6a7812a876f7d133c9555b1151",
    "stories": "d15efd8c0c5b23f0ef71f18bf363c704",
    "reels": "303a4ae99711322310f25250d988f3b7",
    "profile": "d4d88dc1500312af6f937f7b804c68c3",
}


class Profile(GraphQL):
    def __init__(self, auth_data: Optional[Dict], user_id: str) -> None:
        super().__init__(auth_data, user_id)

    async def metadata(self) -> Dict:
        params = {"__a": 1}

        metadata = await self.get(
            f"{ROOT}/{self.profile}",
            params=params,
            headers=self.headers,
            cookies=self.cookies,
        )

        data = await metadata.json(encoding="utf-8")

        self.headers["Referer"] = f"https://www.instagram.com/{self.profile}/"
        self.metadata = data["graphql"]["user"]

        return self.metadata

    async def stories(self):

        # if not self.metadata["has_clips"]:
        #   self.logger.error(
        #        f"User {self.metadata['full_name']} ({self.metadata['username']}) does not have any stories uploaded. Aborting"
        #   )
        #    exit()

        params = {"reel_ids": self.metadata["id"]}

        stories = await self.get(
            url=f"https://i.instagram.com/api/v1/feed/reels_media",
            params=params,
            headers=self.headers,
            cookies=self.cookies,
            allow_redirects=False,
        )

        data = await stories.json(encoding="utf-8")

        story_videoes = [
            items["video_versions"][0]["url"]
            for items in data["reels"][str(self.metadata["id"])]["items"]
        ]

        return story_videoes

    async def grab_posts(self):

        await asyncio.sleep(min(random.expovariate(0.6), 15.0))

    async def download(self, stories: bool):
        try:
            await self.metadata()

            if stories:
                return await self.stories()

        finally:
            await self.session.close()
