FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

# To use a different model, change the model URL below:
ARG MODEL_URL='https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt'

# To use a different embedding, change the URL below:
ARG EMBEDDING_URL='https://civitai.com/api/download/models/9208?type=Model&format=SafeTensor&size=full&fp=fp16'

# If you are using a private Huggingface model (sign in required to download) insert your Huggingface
# access token (https://huggingface.co/settings/tokens) below:
ARG HF_TOKEN=''

RUN apt update && apt-get -y install git wget\
    build-essential cmake libgl-dev libglib2.0-0 vim
RUN ln -s /usr/bin/python3.10 /usr/bin/python

RUN useradd -ms /bin/bash banana
WORKDIR /app

RUN git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git && \
    cd stable-diffusion-webui && \
    git checkout d5063e07e8b4737621978feffd37b18077b9ea64
WORKDIR /app/stable-diffusion-webui

ENV MODEL_URL=${MODEL_URL}
ENV HF_TOKEN=${HF_TOKEN}

RUN pip install tqdm requests

ADD download_embedding.py .
RUN python download_embedding.py

ADD download_checkpoint.py .
RUN python download_checkpoint.py

ADD prepare.py .
RUN python prepare.py --skip-torch-cuda-test --xformers --reinstall-torch --reinstall-xformers

ADD download.py download.py
RUN python download.py

RUN pip install dill

RUN mkdir -p extensions/banana/scripts
ADD script.py extensions/banana/scripts/banana.py
ADD app.py app.py
ADD server.py server.py

CMD ["python", "server.py", "--xformers", "--disable-safe-unpickle", "--lowram", "--no-hashing", "--listen", "--port", "8000"]
