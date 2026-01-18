"""Cliente para API do TMDb."""

import logging
import requests
import json
from time import sleep
from typing import Optional, List


class TMDbClient:
    """Cliente para API do TMDb com logging."""

    def __init__(self, config_path: str = "config.json"):
        """Inicializa cliente."""
        self.logger = logging.getLogger("TMDbClient")

        with open(config_path) as f:
            config = json.load(f)

        self.api_key = config['tmdb']['api_key']
        self.base_url = config['tmdb']['base_url']
        self.language = config['tmdb']['language']

        self.logger.info("Cliente TMDb inicializado")

    def get_movie(self, movie_id: int, max_retries: int = 3) -> Optional[dict]:
        """Busca detalhes de um filme."""
        self.logger.debug(f"Buscando filme {movie_id}")

        for tentativa in range(1, max_retries + 1):
            try:
                url = f"{self.base_url}/movie/{movie_id}"

                response = requests.get(
                    url,
                    params={
                        'api_key': self.api_key,
                        'language': self.language
                    },
                    timeout=10
                )

                if response.status_code == 200:
                    self.logger.info(f"Filme {movie_id} obtido com sucesso")
                    return response.json()
                elif response.status_code == 404:
                    self.logger.warning(f"Filme {movie_id} não encontrado")
                    return None
                elif response.status_code == 429:
                    self.logger.warning("Limite de requisições atingido")
                    sleep(2)
                else:
                    self.logger.error(f"Erro {response.status_code}")

            except requests.exceptions.Timeout:
                self.logger.error(f"Timeout na tentativa {tentativa}")
            except Exception as e:
                self.logger.error(f"Erro: {e}")

            if tentativa < max_retries:
                sleep(1)

        return None

    def get_popular(self, page: int = 1) -> List[dict]:
        """Busca filmes populares."""
        self.logger.info(f"Buscando filmes populares (página {page})")

        url = f"{self.base_url}/movie/popular"

        response = requests.get(
            url,
            params={
                'api_key': self.api_key,
                'language': self.language,
                'page': page
            }
        )

        if response.status_code == 200:
            data = response.json()
            self.logger.info(f"Obtidos {len(data['results'])} filmes")
            return data['results']
        else:
            self.logger.error(f"Erro: {response.status_code}")
            return []
