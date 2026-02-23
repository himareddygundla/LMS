import argparse
from services.report_service import ReportService

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    service = ReportService(args.input, args.output)
    service.run()

if __name__ == "__main__":
    main()