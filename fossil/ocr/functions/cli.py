# cli_script.py

import argparse
from image_to_text import image_to_text

def main():
    # 커맨드 라인 인자 파싱
    parser = argparse.ArgumentParser(description='Extract text from an image.')
    parser.add_argument('path', type=str, help='Path to the image file')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')
    args = parser.parse_args()

    # 함수 호출
    result = image_to_text(args.path, verbose=args.verbose)

    # 결과 출력 또는 다른 작업 수행
    print("Result:", result)

if __name__ == "__main__":
    main()
