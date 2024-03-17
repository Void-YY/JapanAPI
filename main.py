# main.py
from fastapi import FastAPI
from routers import daily_question

# 创建FastAPI应用
app = FastAPI()

# 包含所有路由
app.include_router(daily_question.router)
