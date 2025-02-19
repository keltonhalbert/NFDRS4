import pandas as pd
import os

def run_nfdrs_cli(): 
    """
    Run the NFDRS4 CLI on the testing data.
    Must be run from the $PROJECT_ROOT/tests 
    directory.
    """
    print("Running the NFDRS CLI")
    os.system("../build/bin/NFDRS4_cli ./RunNFDRSSample.cfg")

def load_known():
    """
    Load the known values from the NFDRS4 CLI 
    output and return the Pandas dataframes.
    """
    df_all = pd.read_csv("./data/KnownValue-NFDRSOutput.csv")
    df_indices = pd.read_csv("./data/KnownValue-NFDRSIndexes.csv")
    df_moisture = pd.read_csv("./data/KnownValue-NFDRSMoistures.csv")

    return df_moisture, df_indices, df_all

def load_unknown():
    """
    Load the unverified data we will be testing
    against the known values from the NFDRS4 
    CLI. 
    """
    df_all = pd.read_csv("./NFDRSOutput.csv")
    df_indices = pd.read_csv("./NFDRSIndexes.csv")
    df_moisture = pd.read_csv("./NFDRSMoistures.csv")

    return df_moisture, df_indices, df_all

def main():
    run_nfdrs_cli()

    df_known_moisture, df_known_indices, df_known_all = load_known()
    df_unknown_moisture, df_unknown_indices, df_unknown_all = load_unknown()

    df_compare_all = df_known_all.compare(df_unknown_all)
    df_compare_indices = df_known_indices.compare(df_unknown_indices)
    df_compare_moisture = df_known_moisture.compare(df_unknown_moisture)

    assert(df_compare_all.empty)
    assert(df_compare_indices.empty)
    assert(df_compare_moisture.empty)
    print("All tests passed!")

if __name__ == "__main__":
    main()
