# main.py
from fastapi import FastAPI
from apis.daily_question import router as daily_question_router
from tasks.daily_question import start_daily_question_task

app = FastAPI()
app.include_router(daily_question_router)

# 启动定时任务
start_daily_question_task()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
