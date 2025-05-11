# python_src/main.py

import user_interface
import query_processor
import data_ingestion
import data_processing
import visualization
import error_handling

def main():
    print("Congressional Trading Analyzer initialized.")
    user_interface.init()
    data = data_ingestion.load_data()
    processed_data = data_processing.analyze_data(data)
    visualization.visualize_data(processed_data)

if __name__ == "__main__":
    main()