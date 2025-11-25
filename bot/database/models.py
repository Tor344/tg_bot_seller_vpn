from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)# telegram id
    vpn = fields.ReverseRelation["Vpn"]

    class Meta:
        table = "user"


class Vpn(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="vpn")
    file_name = fields.TextField()
    data = fields.TextField()
    server = fields.ForeignKeyField("models.Server", related_name="vpn")
    date_break = fields.DatetimeField()

    class Meta:
        table = "vpn"


class Location(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    servers = fields.ReverseRelation["Server"]

    class Meta:
        table = "locations"


class Server(Model):
    id = fields.IntField(pk=True)
    ip = fields.CharField(max_length=20)
    location = fields.ForeignKeyField("models.Location", related_name="servers")
    vpn = fields.ReverseRelation["Vpn"]

    class Meta:
        table = "server"


class AdminUser(Model):
    tg_id = fields.IntField(pk=True)


class VpnType(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    class Meta:
        table = "vpntype"