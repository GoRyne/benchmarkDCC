FROM tensorflow/tensorflow:1.13.1-py3

RUN apt-get update \
    && apt-get install -y git vim build-essential libssl-dev libffi-dev python-dev wget zip

RUN git clone https://github.com/TalwalkarLab/leaf.git 
RUN pip install --upgrade pip
RUN pip install -r /leaf/requirements.txt
RUN pip install pillow
