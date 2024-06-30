from dotenv import load_dotenv
import os
load_dotenv()
import loader.broker_inversis
from modelos.constants import EnvironmentVariableNames, BankNames

def main():
    loader.broker_inversis.load_inversis_broker_operations(os.getenv(EnvironmentVariableNames.SOURCE_EVO_FILES),BankNames.EVO)

if __name__ == '__main__':
    main()