from __future__ import annotations
from enum import Enum, auto
from typing import Dict, Protocol, Type, Any, Tuple, List


class MusicServiceType(Enum):
    SPOTIFY = auto()
    PANDORA = auto()
    LOCAL = auto()


class MusicService(Protocol):
    """
    Music Service Interface
    """

    def test_connection(self) -> None:
        ...


class MusicServiceBuilder(Protocol):
    """
    Music Service Builder Interface
    """

    def __call__(self, *args: Any, **kwargs: Any) -> MusicService:
        ...

    def authorize(self, *args: Any, **kwargs: Any) -> Any:
        ...


class SpotifyService:
    """
    Spotify Music Service
    """

    def __init__(self, access_code: str) -> None:
        self._access_code: str = access_code

    def test_connection(self) -> None:
        print(f"Accessing Spotify with {self._access_code}")

    def __repr__(self) -> str:
        return f"SpotifyService(access_code={self._access_code})"


class SpotifyServiceBuilder:
    """
    Spotify Music Service Builder which sends spotify_client_key and spotify_client_secret
    to authorize with a access_code, and caches and returns the service.
    """

    def __init__(self) -> None:
        self._instance: SpotifyService | None = None

    def __call__(
        self, spotify_client_key: str, spotify_client_secret: str, **_ignored: Any
    ) -> SpotifyService:
        if not self._instance:
            access_code = self.authorize(spotify_client_key, spotify_client_secret)
            self._instance = SpotifyService(access_code)
        return self._instance

    def authorize(self, key: str, secret: str) -> str:
        return "SPOTIFY_ACCESS_CODE"

    def __repr__(self) -> str:
        return f"SpotifyServiceBuilder()"


class PandoraService:
    """
    Pandora Music Service Builder which sends pandora_client_key and pandora_client_secret
    to authorize with consumer_key and consumer_secret, and caches and returns the service.
    """

    def __init__(self, consumer_key: str, consumer_secret: str) -> None:
        self._key: str = consumer_key
        self._secret: str = consumer_secret

    def test_connection(self) -> None:
        print(f"Accessing Pandora with {self._key} and {self._secret}")

    def __repr__(self) -> str:
        return (
            f"PandoraService(consumer_key={self._key}, consumer_secret={self._secret})"
        )


class PandoraServiceBuilder:
    def __init__(self) -> None:
        self._instance: PandoraService | None = None

    def __call__(
        self, pandora_client_key: str, pandora_client_secret: str, **_ignored: Any
    ) -> PandoraService:
        if not self._instance:
            consumer_key, consumer_secret = self.authorize(
                pandora_client_key, pandora_client_secret
            )
            self._instance = PandoraService(consumer_key, consumer_secret)
        return self._instance

    def authorize(self, key: str, secret: str) -> Tuple[str, str]:
        return "PANDORA_CONSUMER_KEY", "PANDORA_CONSUMER_SECRET"

    def __repr__(self) -> str:
        return f"PandoraServiceBuilder()"


class LocalService:
    """
    Local Music Service
    """

    def __init__(self, location: str) -> None:
        self._location: str = location

    def test_connection(self) -> None:
        print(f"Accessing Local music at {self._location}")

    def __repr__(self) -> str:
        return f"LocalService(location={self._location})"


class LocalServiceBuilder:
    """
    A Local Music Service Builder which creates a Local Music Service by local_music_location
    """

    def __call__(self, local_music_location: str, **_ignored: Any) -> LocalService:
        return LocalService(local_music_location)

    def __repr__(self) -> str:
        return f"LocalServiceBuilder()"


# def create_local_music_service(local_music_location: str, **_ignored: Any) -> LocalService:
#     return LocalService(local_music_location)


class ObjectFactory:
    """
    A generic object factory that can register a particular type of music service,
    and create the music service
    """

    def __init__(self) -> None:
        self._builders: Dict[MusicServiceType, MusicServiceBuilder] = {}

    def register_builder(
        self, key: MusicServiceType, builder: MusicServiceBuilder
    ) -> None:
        self._builders[key] = builder

    def create(self, key: MusicServiceType, **kwargs: Any) -> MusicService:
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)

    def list_all_services(self) -> List[MusicService]:
        return list(self._builders.values())


class MusicServiceProvider(ObjectFactory):
    """
    A Wrapper class that creates the music service using the object factory.
    """

    def get(self, service_type: MusicServiceType, **kwargs: Any) -> MusicService:
        return self.create(service_type, **kwargs)


services = MusicServiceProvider()
services.register_builder(MusicServiceType.SPOTIFY, SpotifyServiceBuilder())
services.register_builder(MusicServiceType.PANDORA, PandoraServiceBuilder())
services.register_builder(MusicServiceType.LOCAL, LocalServiceBuilder())
