import os
from airflow.models import Variable
output_path = Variable.get('OUTPUT')
