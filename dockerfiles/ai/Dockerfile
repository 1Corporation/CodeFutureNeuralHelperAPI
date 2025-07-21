FROM python:3.13-slim

COPY ai/requirements.txt .

RUN apt update \
&& apt install build-essential python3-dev -y \
&& python3 -m pip install --no-cache-dir --no-warn-script-location --upgrade pip \
&& python3 -m pip install --no-cache-dir --no-warn-script-location --user -r requirements.txt \
&& python3 -m pip uninstall torch -y \
&& python3 -m pip install --pre torch --index-url https://download.pytorch.org/whl/nightly/cu128 

COPY ai/ .

