FROM python:3-alpine
COPY * /apps/gh-follow-bot/
WORKDIR /apps/gh-follow-bot/
RUN ["pip","install","-r","requirements.txt"]
ENV ghuser=""
ENV ghtoken=""
CMD ["python", "main.py"]