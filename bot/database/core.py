from tortoise import Tortoise


class Database():
    def __init__(self, db_url: str = "sqlite://db.sqlite3") -> None:
        self.db_url = db_url

    async def connect(self) -> None:
        """Конектимся к базе"""
        await Tortoise.init(db_url=self.db_url, modules={"models": ["bot.database.models"]})
        await Tortoise.generate_schemas()

    async def close(self):
        """Закрываем конект"""
        await Tortoise.close_connections()

db = Database()