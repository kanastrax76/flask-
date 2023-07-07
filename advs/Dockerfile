FROM python:3.10

RUN apt update && apt install -y curl

COPY requirements.txt .


RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . ./advs

WORKDIR /advs
EXPOSE 5001

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait
RUN chmod +x ./entrypoint.sh


#ENTRYPOINT ["entrypoint.sh"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT /wait && bash ./entrypoint.sh
