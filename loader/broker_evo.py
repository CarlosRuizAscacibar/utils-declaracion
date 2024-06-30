from dotenv import load_dotenv
import os
load_dotenv()
import loader.broker_inversis
from modelos.constants import EnvironmentVariableNames, BrokerNames

def main():
    loader.broker_inversis.load_inversis_broker_operations(os.getenv(EnvironmentVariableNames.SOURCE_EVO_FILES),BrokerNames.EVO)

def process_file(file_path):
    loader.broker_inversis.load_inversis_broker_operations(file_path=file_path,bank=BrokerNames.EVO)


if __name__ == '__main__':
    main()