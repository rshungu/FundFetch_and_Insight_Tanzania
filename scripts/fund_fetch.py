from scripts.fetch_zansec import fetch_zansec_data
from scripts.fetch_sanlaam import fetch_sanlaam_data
from scripts.fetch_utt import fetch_utt_data
from scripts.fetch_nav import fetch_nav_data

def main():
    fetch_zansec_data()
    fetch_sanlaam_data()
    fetch_utt_data()
    fetch_nav_data()

if __name__ == "__main__":
    main()
