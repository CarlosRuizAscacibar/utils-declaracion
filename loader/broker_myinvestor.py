from dotenv import load_dotenv
import os
load_dotenv()
import loader.broker_inversis
from modelos.constants import EnvironmentVariableNames, BrokerNames

def main():
    loader.broker_inversis.load_inversis_broker_operations(os.getenv(EnvironmentVariableNames.SOURCE_MY_INVESTOR_FILES),BrokerNames.MYINVESTOR)

def process_file(file_path):
    loader.broker_inversis.load_inversis_broker_operations(file_path=file_path,bank=BrokerNames.MYINVESTOR)

if __name__ == '__main__':
    main()