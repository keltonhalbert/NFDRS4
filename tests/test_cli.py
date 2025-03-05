from scipy.stats import percentileofscore
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import argparse
import os

mpl.use("Agg")


def run_nfdrs_cli(dir):
    """
    Run the NFDRS4 CLI on the testing data.
    Must be run from the $PROJECT_ROOT/tests
    directory.
    """
    print("Running the NFDRS CLI")
    os.system(f"{dir}/NFDRS4_cli ./RunNFDRSSample.cfg")


def load_known():
    """
    Load the known values from the NFDRS4 CLI
    output and return the Pandas dataframes.
    """
    df_all = pd.read_csv(
        "./data/KnownValue-NFDRSOutput.csv",
        parse_dates=["DateTime"]
    ).set_index(["DateTime"])
    df_indices = pd.read_csv(
        "./data/KnownValue-NFDRSIndexes.csv",
        parse_dates=["DateTime"]
    ).set_index(["DateTime"])
    df_moisture = pd.read_csv(
        "./data/KnownValue-NFDRSMoistures.csv",
        parse_dates=["DateTime"]
    ).set_index(["DateTime"])

    return df_moisture, df_indices, df_all


def load_unknown():
    """
    Load the unverified data we will be testing
    against the known values from the NFDRS4
    CLI.
    """
    df_all = pd.read_csv(
        "./NFDRSOutput.csv",
        parse_dates=["DateTime"]
    ).set_index(["DateTime"])
    df_indices = pd.read_csv(
        "./NFDRSIndexes.csv",
        parse_dates=["DateTime"]
    ).set_index(["DateTime"])
    df_moisture = pd.read_csv(
        "./NFDRSMoistures.csv",
        parse_dates=["DateTime"]
    ).set_index(["DateTime"])

    return df_moisture, df_indices, df_all


def plot_dfm_diff(key, df_known, df_test):
    """
    Plot the 1-hour Dead Fuel Moisture differences
    between the "known" data and the testing data.
    """
    ylabel_dict = {
        "1HourDFM(%)": "1-Hour Dead Fuel Moisture Difference (%)\n",
        "10HourDFM(%)": "10-Hour Dead Fuel Moisture Difference (%)\n",
        "100HourDFM(%)": "100-Hour Dead Fuel Moisture Difference (%)\n",
        "1000HourDFM(%)": "1000-Hour Dead Fuel Moisture Difference (%)\n",
    }
    outname_dict = {
        "1HourDFM(%)": "1hour",
        "10HourDFM(%)": "10hour",
        "100HourDFM(%)": "100hour",
        "1000HourDFM(%)": "1000hour",
    }

    ylabel_str = ylabel_dict[key] + "(tested value - known value)"
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)

    date_time = df_known.index
    known_dfm = df_known[key]
    test_dfm = df_test[key]

    ax.plot(date_time, test_dfm - known_dfm, 'g-')

    ax.set_ylabel(ylabel_str)
    ax.set_xlabel("Period of Record")

    plt.savefig(f"DFM_{outname_dict[key]}_comparison.png", bbox_inches="tight")


def plot_derived_diff(key, df_known, df_test):
    """
    Plot the 1-hour Dead Fuel Moisture differences
    between the "known" data and the testing data.
    """

    ylabel_dict = {
        "ERC": "Energy Release Component Difference\n",
        "BI": "Burning Index Difference\n",
        "KBDI": "Keetch-Byram Drought Index Difference\n",
    }

    ylabel_str = ylabel_dict[key] + "(tested value - known value)"
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)

    date_time = df_known.index
    known_dfm = df_known[key]
    test_dfm = df_test[key]

    ax.plot(date_time, test_dfm - known_dfm, 'r-')

    ax.set_ylabel(ylabel_str)
    ax.set_xlabel("Period of Record")

    plt.savefig(f"{key}_comparison.png", bbox_inches="tight")


def plot_erc_percentiles(df_known, df_test):
    """
    Plot the ERC percentiles for the given
    test data.
    """
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    df_known["day_of_year"] = df_known.index.dayofyear
    df_test["day_of_year"] = df_test.index.dayofyear

    df_known["percentile"] = percentileofscore(
        df_known["ERC"], df_known["ERC"])
    df_test["percentile"] = percentileofscore(
        df_test["ERC"], df_test["ERC"])

    daily_mean_known = df_known.groupby("day_of_year").mean()
    daily_mean_test = df_test.groupby("day_of_year").mean()
    date_time = daily_mean_known.index

    ax.plot(
        date_time,
        daily_mean_known["percentile"].values,
        'k-',
        label="Operational NFDRS4"
    )
    ax.plot(
        date_time,
        daily_mean_test["percentile"].values,
        'r-',
        label="Modified NFDRS4"
    )
    ax.set_ylabel("")
    ax.set_xlabel("Day of Year")
    ax.legend(loc="upper right")
    plt.savefig("erc_percentiles.png", bbox_inches="tight")

    df_known.drop(columns=["day_of_year", "percentile"], inplace=True)
    df_test.drop(columns=["day_of_year", "percentile"], inplace=True)


def plot_daily_mean_DFM(key, df_known, df_test):
    """
    Generate plots of daily averaged dead fuel moisture
    for the 15 year period of record.
    """
    ylabel_dict = {
        "1HourDFM(%)": "1-Hour Daily Mean Dead Fuel Moisture (%)\n",
        "10HourDFM(%)": "10-Hour Daily Mean Dead Fuel Moisture (%)\n",
        "100HourDFM(%)": "100-Hour Daily Mean Dead Fuel Moisture (%)\n",
        "1000HourDFM(%)": "1000-Hour Daily Mean Dead Fuel Moisture (%)\n",
    }
    outname_dict = {
        "1HourDFM(%)": "1hour",
        "10HourDFM(%)": "10hour",
        "100HourDFM(%)": "100hour",
        "1000HourDFM(%)": "1000hour",
    }
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    df_known["day_of_year"] = df_known.index.dayofyear
    df_test["day_of_year"] = df_test.index.dayofyear

    daily_mean_known = df_known.groupby("day_of_year").mean()
    daily_mean_test = df_test.groupby("day_of_year").mean()
    date_time = daily_mean_known.index

    ax.plot(date_time, daily_mean_known[key].values,
            'k-', label="Operational NFDRS4")
    ax.plot(date_time, daily_mean_test[key].values,
            'g-', label="Modified NFDRS4")

    ax.set_ylabel(ylabel_dict[key])
    ax.set_xlabel("Day of Year")
    ax.set_title(f"Lolo Natl. Forest 2001-2018\n{ylabel_dict[key]}")
    ax.legend(loc="upper right")
    plt.savefig(f"{outname_dict[key]}_dailymean.png", bbox_inches="tight")

    df_known.drop(columns=["day_of_year"], inplace=True)
    df_test.drop(columns=["day_of_year"], inplace=True)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--bin-dir", type=str)
    parser.add_argument("--skip-cli", action="store_true", required=False)
    args = parser.parse_args()

    if not args.skip_cli:
        run_nfdrs_cli(args.bin_dir)

    df_known_moisture, df_known_indices, df_known_all = load_known()
    df_unknown_moisture, df_unknown_indices, df_unknown_all = load_unknown()

    # plot comparisons
    plot_dfm_diff("1HourDFM(%)", df_known_moisture, df_unknown_moisture)
    plot_dfm_diff("10HourDFM(%)", df_known_moisture, df_unknown_moisture)
    plot_dfm_diff("100HourDFM(%)", df_known_moisture, df_unknown_moisture)
    plot_dfm_diff("1000HourDFM(%)", df_known_moisture, df_unknown_moisture)

    plot_derived_diff("BI", df_known_indices, df_unknown_indices)
    plot_derived_diff("ERC", df_known_indices, df_unknown_indices)
    plot_derived_diff("KBDI", df_known_indices, df_unknown_indices)

    plot_daily_mean_DFM("1HourDFM(%)", df_known_moisture,
                        df_unknown_moisture)
    plot_daily_mean_DFM("10HourDFM(%)", df_known_moisture,
                        df_unknown_moisture)
    plot_daily_mean_DFM("100HourDFM(%)", df_known_moisture,
                        df_unknown_moisture)
    plot_daily_mean_DFM("1000HourDFM(%)", df_known_moisture,
                        df_unknown_moisture)

    # Broken for now due to old scipy version behavior
    # plot_erc_percentiles(df_known_indices, df_unknown_indices)

    df_compare_all = df_known_all.compare(df_unknown_all)
    df_compare_indices = df_known_indices.compare(df_unknown_indices)
    df_compare_moisture = df_known_moisture.compare(df_unknown_moisture)

    print("Teting the NFDRS fuel moisture output")
    assert (df_compare_moisture.empty), \
        "Output differs from testing data.\n" + f"{df_compare_moisture}"
    print("Testing the NFDRS indices output")

    assert (df_compare_indices.empty), \
        "Output differs from testing data.\n" + f"{df_compare_indices}"

    print("Testing the CSV with all combined data present")
    assert (df_compare_all.empty), \
        "Output differs from testing data.\n" + f"{df_compare_all}"

    print("All tests passed!")


if __name__ == "__main__":
    main()
