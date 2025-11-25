from datetime import datetime
from typing import List

from bot.database.models import *


class DB_user():
    id = fields.IntField(pk=True)

    async def add(self, id: int) -> User:
        """создаем пользователя"""
        user = await User.filter(id=id).first()
        if user:
            return user
        return await User.create(id=id)


class DB_vpn():
    async def add(self, user_id: int,file_name, data: str,date_break:datetime,server_id:int) -> Vpn:
        """date: YYYY-MM-DD"""
        server = await Server.get(id=server_id)
        user = await User.get(id=user_id)
        return await Vpn.create(user=user,file_name=file_name, data=data, server=server, date_break=date_break)

    async def get_vpns_by_user(self, user_id:int) -> List[Vpn]:
        user = await User.get(id=user_id)
        vpn = await Vpn.filter(user=user).all()
        if not vpn: return []
        return vpn

    async def get_data(self,id:int)-> str:
        vpn = await Vpn.get(id=id)
        return vpn.data

    async def update_date_break(self,id: int, new_date_break: datetime) -> bool:
        vpn = await Vpn.get(id=id)
        vpn.date_break = new_date_break
        await vpn.save()
        return True

    async def delete(self, id: Vpn) -> bool:
        vpn = await Vpn.get(id=id)
        await vpn.delete()
        return True


class DB_location:
    async def add(self,name: str) -> Location:
        location = await Location.create(name=name)
        return location

    async def get(self, location_name: str):
        return await Location.filter(name=location_name).first()

    async def get_all(self) -> List[Location]:
        return await Location.all().order_by('id')

class DB_server:
    async def add(self, ip: str, location_name: str):
        location = await Location.filter(name=location_name).first()
        if not location:
            return False
        return await Server.create(ip=ip, location=location)

    async def get_all(self) -> List[Server]:
        server = await Server.all().order_by('id')
        return server

    async def get_all_for_name(self,name: str) -> List[Server]:
        return await Server.filter(location__name=name).all()

    async def get_location(self, vpn_id: int) -> str:
        vpn = await Vpn.get(id=vpn_id).select_related("server__location")
        return vpn.server.location.name

    async def delete(self, server_id: int) -> bool:
        server = await Server.get(id=server_id)
        await server.delete()
        return True


class DB_admin_user:
    async def add(self, id: int):
        admin_user = await AdminUser.filter(id=id).first()
        if admin_user:
            return False
        return await AdminUser.create(id=id)

    async def delete(self, id: int) -> bool:
        admin_user = await AdminUser.filter(id=id).first()
        if not(admin_user):
            return False
        await admin_user.delete()
        return True

    async def is_admin(self,id: int):
        user = await AdminUser.filter(id=id).first()
        if not user:
            return False
        return True

db_user = DB_user()
db_location = DB_location()
db_server = DB_server()
db_vpn = DB_vpn()
db_admin = DB_admin_user()
