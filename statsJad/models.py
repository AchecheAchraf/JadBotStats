# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Mode(models.Model):
    mode_id = models.AutoField(primary_key=True)
    mode_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'mode'

class Ehpad(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.TextField()
    data_version = models.IntegerField()
    address = models.TextField()
    external_api_key = models.TextField(blank=True, null=True)
    external_api_type = models.IntegerField()
    external_api_record_data_type = models.TextField(blank=True, null=True)
    external_urls = models.ForeignKey('ExternalUrls', models.DO_NOTHING, blank=True, null=True)
    daily_goal = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ehpad'

class Protocol(models.Model):
    protocol_id = models.UUIDField(primary_key=True)
    protocol_buisness_id = models.IntegerField(blank=True, null=True)
    protocol_name = models.TextField()
    protocol_deleted_date = models.DateTimeField(blank=True, null=True)
    protocol_mode = models.ForeignKey(Mode, models.DO_NOTHING, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    ehpad = models.ForeignKey(Ehpad, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'protocol'




class ProtocolEvent(models.Model):
    id = models.UUIDField(primary_key=True)
    user_id = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    protocol = models.ForeignKey(Protocol, models.DO_NOTHING)
    ehpad = models.ForeignKey(Ehpad, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'protocol_event'



