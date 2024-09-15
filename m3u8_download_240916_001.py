import subprocess

# .m3u8 파일 URL
m3u8_url = 'https://strm2.spatic.go.kr/live/152.stream/playlist.m3u8'

# 출력 파일명
output_file = 'output.mp4'

# streamlink를 사용해 스트리밍을 다운로드
subprocess.run(['streamlink', m3u8_url, 'best', '-o', output_file])
