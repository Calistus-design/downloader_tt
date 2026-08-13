# filter_tiktok_videos.py

with open("links.txt", "r") as f:
    links = f.readlines()

video_links = [link.strip() for link in links if "/video/" in link]

with open("video_links.txt", "w") as f:
    f.write("\n".join(video_links))

print("Extracted video links saved to video_links.txt")
