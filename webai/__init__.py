import argparse
from webai.agent import GPTV_Actor
import os

def main():
    parser = argparse.ArgumentParser(description='Run GPTV Actor with given parameters.')
    parser.add_argument('--start_link', type=str, default='https://www.google.com', help='The start link for the actor to use.')
    parser.add_argument('--auto', type=bool, default=False, help='Boolean to set the auto mode.')
    args = parser.parse_args()
    
    if args.auto:
        raise Exception("Auto mode is still under development.")
    if os.environ["OPENAI_API_KEY"] is None:
        raise Exception("Please set OPENAI_API_KEY in your environment variables.")
    actor = GPTV_Actor()
    actor.start(args.start_link, args.auto)

if __name__ == '__main__':
    main()
