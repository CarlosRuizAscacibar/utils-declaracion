import modelos.constants as constants 
from dotenv import load_dotenv
load_dotenv()
import os
import loader.banco_sabadell as banco_sabadell
import loader.mynvestor_banco as mynvestor_banco
import loader.evo as evo_banco
import loader.broker_evo as broker_evo
import loader.broker_myinvestor as broker_myinvestor
import loader.myinvestor_json as my_investor_json




def process_all_files_from_folder(file_path, read_single_file):
    files_in_folder = [f'{file_path}/{f}' for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
    for current_file in files_in_folder:
        print(f"processing file {current_file}")
        read_single_file(current_file)

def main():
    print("Loading banco_sabadell")
    process_all_files_from_folder(os.getenv(constants.EnvironmentVariableNames.MOVIMIENTOS_SABADELL), banco_sabadell.read_single_file)
    print("Loading evo_banco")
    process_all_files_from_folder(os.getenv(constants.EnvironmentVariableNames.MOVIMIENTOS_CUENTA_CORRIENTE_EVO), evo_banco.process_file)
    print("Loading mynvestor_banco")
    process_all_files_from_folder(os.getenv(constants.EnvironmentVariableNames.MOVIMIENTOS_MY_INVESTOR), mynvestor_banco.process_file)
    print("Loading broker_evo")
    process_all_files_from_folder(os.getenv(constants.EnvironmentVariableNames.SOURCE_EVO_FILES), broker_evo.process_file)
    print("Loading broker_myinvestor")
    process_all_files_from_folder(os.getenv(constants.EnvironmentVariableNames.SOURCE_MY_INVESTOR_FILES), broker_myinvestor.process_file)
    print("Loading broker_myinvestor_json")
    my_investor_json.load_all_operations_and_persist()
    print("Loading json_bank_myinvestor")
    my_investor_json.load_all_movements_and_persist()

if __name__ == '__main__':
    main()