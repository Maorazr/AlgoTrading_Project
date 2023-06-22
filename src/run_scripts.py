from unittest.mock import patch



def run_dataScalping(params):
    with patch('builtins.input', side_effect=params):
        import dataScapling
        dataScapling.main()

def run_main(params):
    with patch('builtins.input', side_effect=params):
        import main
        main.main()

def run_summary(params):
    with patch('builtins.input', side_effect=params):
        import summary
        summary.main()

def run_scripts(params_list):
    for params in params_list:
        run_dataScalping(params[0])
        run_main(params[1])
        run_summary(params[2])

if __name__ == "__main__":
    # An example of how to call run_scripts with a list of tuples
    parameters = [
        (["y", "2020-01-01,2022-12-31", "14", "14", "10,0.015", "10", "2020_2022_Processed", "n"],  # parameters for dataScalping
         ["", "0.25", "62", "38", "100", "-100", "filename2", "n"],  # parameters for main
         ["filename3", "n"]  # parameters for summary
        ), 
        # Add more tuples for each additional set of parameters...
    ]
    run_scripts(parameters)
