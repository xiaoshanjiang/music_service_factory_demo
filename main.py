import music
from music import MusicServiceType


config = {
    "spotify_client_key": "THE_SPOTIFY_CLIENT_KEY",
    "spotify_client_secret": "THE_SPOTIFY_CLIENT_SECRET",
    "pandora_client_key": "THE_PANDORA_CLIENT_KEY",
    "pandora_client_secret": "THE_PANDORA_CLIENT_SECRET",
    "local_music_location": "/usr/data/music",
}


def main() -> int:
    pandora = music.services.get(MusicServiceType.PANDORA, **config)
    pandora.test_connection()
    spotify = music.services.get(MusicServiceType.SPOTIFY, **config)
    spotify.test_connection()
    local = music.services.get(MusicServiceType.LOCAL, **config)
    local.test_connection()

    pandora2 = music.services.get(MusicServiceType.PANDORA, **config)
    print(f"id(pandora) == id(pandora2): {id(pandora) == id(pandora2)}")

    spotify2 = music.services.get(MusicServiceType.SPOTIFY, **config)
    print(f"id(spotify) == id(spotify2): {id(spotify) == id(spotify2)}")

    return 0


if __name__ == "__main__":
    exit(main())
