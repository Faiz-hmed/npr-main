FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
COPY test.jpg .

RUN useradd -ms /bin/bash user
RUN apt-get update && apt-get install tesseract-ocr -y

RUN pip install -r requirements.txt

RUN pip install torch torchvision
RUN pip install easyocr

RUN mkdir static
VOLUME [ "static" ]
RUN chown -R user: static

RUN chmod o+x -R /app
# RUN chown -Rc user: ./static
USER user

RUN python -c "import easyocr;reader=easyocr.Reader(['en']);res=reader.readtext('test.jpg',detail=0);print(res)"
EXPOSE 8000
COPY . .

ENTRYPOINT ["sh","startup.sh"] 