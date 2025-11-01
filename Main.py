from fastapi import FastAPI
import logging
from ib_insync.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()

# print the load of the env file
print(settings.model_dump())


@app.get("/")
def read_root():
    error = ""
    if not settings.debug:
        error += "debug dont exist in env file \n"
    if not settings.database_url:
        error += "database url dont exist in env file \n"
    if not settings.secret_key:
        error += "secret key dont exist in env file \n"
    return {
        "errors": "no errors occurs" if error == "" else error,
        "debug": settings.debug,
        "database_url": settings.database_url,
        "secret_key": settings.database_url
    }

# @app.get("/")
# async def root():
#     async with httpx.AsyncClient() as client:
#         users = (await client.get("https://jsonplaceholder.typicode.com/users")).json()
#         posts = (await client.get("https://jsonplaceholder.typicode.com/posts")).json()
#         comments = (await client.get("https://jsonplaceholder.typicode.com/comments")).json()
#
#         user_posts = defaultdict(list)
#         user_comments = defaultdict(list)
#
#         for comment in comments:
#             user_comments[comment["email"]].append(comment)
#
#         for post in posts:
#             user_posts[post["userId"]].append(post)
#
#         user_max_posts = max(users, key=lambda u: len(user_posts[u["id"]]))["id"]
#
#         max_comments = 0
#         email_max_comments = ""
#         for email, values in user_comments.items():
#             if len(values) > max_comments:
#                 user_email = any(user["email"] == email for user in users)
#             if user_email:
#                 max_comments = len(values)
#                 email_max_comments = email
#             user_email = False
#
#         # user_max_comments = u["id"] for u in users if u["email"] == email_max_comments
#
#
#         return {"max_posts": len(user_posts[user_max_posts]),
#                 "max_comments": max_comments,
#                 "user_max_posts_detail": users[user_max_posts],
#                 # "user_max_comments_detail": user_max_comments,
#                 "posts": user_posts[user_max_posts],
#                 "comments": user_comments[email_max_comments]
#                 }