FROM balao1312/ubuntu_with_python37:latest

ADD ./project_104_multi/ /project_104_multi

WORKDIR /project_104_multi

RUN pip3 install -r requirement.txt

ADD ./project_104_multi/simhei.ttf /usr/local/lib/python3.8/dist-packages/matplotlib/mpl-data/fonts/ttf

RUN mv /project_104_multi/matplotlibrc /usr/local/lib/python3.8/dist-packages/matplotlib/mpl-data/matplotlibrc

CMD python3 app.py 
