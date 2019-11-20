FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /root/.config/matplotlib
RUN echo "backend : Agg" > /root/.config/matplotlib/matplotlibrc

COPY . .

ENTRYPOINT [ "gunicorn" ]

CMD [ "--bind", "0.0.0.0:5000", "app:app" ]