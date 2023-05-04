from dataScapling import main as dataScapling
from main import main
from summary import main as summary

def run_all():
    dataScapling()
    main()
    summary()

if __name__ == "__main__":
    run_all()
