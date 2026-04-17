def format_streams(streams):
    qualities = []
    for stream in streams:
        if stream.resolution:
            qualities.append(stream.resolution)
    return list(set(qualities))