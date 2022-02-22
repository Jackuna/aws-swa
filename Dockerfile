FROM python:3.7
RUN python3 -m pip install ansible==2.10 boto3 awscli

RUN rm -rf /usr/local/ansible/

copy lambda_folder /usr/local/ansible/lambda_folder

WORKDIR usr/local/ansible/

CMD ["ansible-playbook", "--version"]
