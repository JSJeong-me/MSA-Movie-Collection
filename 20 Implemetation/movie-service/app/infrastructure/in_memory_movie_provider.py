class InMemoryExternalMovieProvider:
    async def fetch_movie_metadata(self, query: object) -> object:
        provider = str(getattr(query, "provider", "unknown"))
        external_id = str(getattr(query, "external_id", "unknown"))
        return {
            "title": f"Imported-{external_id}",
            "description": f"Imported from {provider}",
            "release_year": 2020,
            "external_provider": provider,
            "external_id": external_id,
            "genres": ["Drama"],
            "cast": ["Sample Actor"],
            "directors": ["Sample Director"],
        }
