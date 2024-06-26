# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Efmigrationshistory(models.Model):
    migration_id = models.CharField(primary_key=True, max_length=150)
    product_version = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = '__EFMigrationsHistory'


class Audit(models.Model):
    id = models.UUIDField(primary_key=True)
    title = models.TextField()
    acceptance_threshold = models.FloatField()
    ehpad = models.ForeignKey('Ehpad', models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit'


class AuditElement(models.Model):
    id = models.UUIDField(primary_key=True)
    title = models.TextField()
    sub_title = models.TextField(blank=True, null=True)
    evaluation_criteria = models.TextField()
    target_quality_threshold = models.TextField()
    coefficient = models.IntegerField()
    audit = models.ForeignKey(Audit, models.DO_NOTHING)
    ehpad = models.ForeignKey('Ehpad', models.DO_NOTHING)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_element'


class AuditElementEvent(models.Model):
    id = models.UUIDField(primary_key=True)
    is_valid = models.BooleanField()
    audit_event = models.ForeignKey('AuditEvent', models.DO_NOTHING)
    audit_element = models.ForeignKey(AuditElement, models.DO_NOTHING)
    ehpad = models.ForeignKey('Ehpad', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audit_element_event'


class AuditEvent(models.Model):
    id = models.UUIDField(primary_key=True)
    execution_date = models.DateTimeField()
    note = models.FloatField()
    audit = models.ForeignKey(Audit, models.DO_NOTHING)
    room = models.ForeignKey('Room', models.DO_NOTHING)
    user_id = models.IntegerField()
    ehpad = models.ForeignKey('Ehpad', models.DO_NOTHING)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_event'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Custombalise(models.Model):
    custombalise_id = models.AutoField(primary_key=True)
    custombalise_value = models.TextField()
    default_balise = models.ForeignKey('Defaultbalise', models.DO_NOTHING, blank=True, null=True)
    ehpad = models.ForeignKey('Ehpad', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'custombalise'


class DayOfWeek(models.Model):
    id = models.IntegerField(primary_key=True)
    day_of_week = models.TextField()

    class Meta:
        managed = False
        db_table = 'day_of_week'


class DayOfWeekEntityPostTaskEntity(models.Model):
    days_of_week = models.OneToOneField(DayOfWeek, models.DO_NOTHING, primary_key=True)  # The composite primary key (days_of_week_id, post_task_entities_id) found, that is not supported. The first column is selected.
    post_task_entities = models.ForeignKey('PostTask', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'day_of_week_entity_post_task_entity'
        unique_together = (('days_of_week', 'post_task_entities'),)


class DayOfWeekEntityProtocolTaskEntity(models.Model):
    days_of_week = models.OneToOneField(DayOfWeek, models.DO_NOTHING, primary_key=True)  # The composite primary key (days_of_week_id, protocol_task_entities_id) found, that is not supported. The first column is selected.
    protocol_task_entities = models.ForeignKey('ProtocolTask', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'day_of_week_entity_protocol_task_entity'
        unique_together = (('days_of_week', 'protocol_task_entities'),)


class DefaultBaliseProtocolTaskRelationEntity(models.Model):
    protocol_task = models.OneToOneField('ProtocolTask', models.DO_NOTHING, primary_key=True)  # The composite primary key (protocol_task_id, default_balise_id) found, that is not supported. The first column is selected.
    default_balise = models.ForeignKey('Defaultbalise', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'default_balise_protocol_task_relation_entity'
        unique_together = (('protocol_task', 'default_balise'),)


class Defaultbalise(models.Model):
    defaultbalise_id = models.AutoField(primary_key=True)
    defaultbalise_value = models.TextField()

    class Meta:
        managed = False
        db_table = 'defaultbalise'


class Distribution(models.Model):
    name = models.TextField()
    ehpad = models.ForeignKey('Ehpad', models.DO_NOTHING)
    liquid_measure = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'distribution'


class DistributionDetail(models.Model):
    resident_id = models.IntegerField()
    distribution_item = models.ForeignKey('DistributionItems', models.DO_NOTHING)
    distribution_resident = models.ForeignKey('DistributionResident', models.DO_NOTHING)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField()
    distribution = models.ForeignKey(Distribution, models.DO_NOTHING)
    ehpad = models.ForeignKey('Ehpad', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'distribution_detail'


class DistributionEvent(models.Model):
    user_id = models.IntegerField()
    date = models.DateTimeField()
    resident_id = models.IntegerField()
    distribution_resident = models.ForeignKey('DistributionResident', models.DO_NOTHING)
    commentaire = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'distribution_event'


class DistributionItems(models.Model):
    icon = models.TextField(blank=True, null=True)
    is_in_sentence = models.BooleanField()
    name = models.TextField()
    template = models.TextField(blank=True, null=True)
    quantity_required = models.BooleanField()
    is_utensil = models.BooleanField()
    reporting_count_enable = models.BooleanField()
    distribution = models.ForeignKey(Distribution, models.DO_NOTHING)
    ehpad = models.ForeignKey('Ehpad', models.DO_NOTHING)
    is_liquid = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'distribution_items'


class DistributionItemsLink(models.Model):
    distribution = models.ForeignKey(Distribution, models.DO_NOTHING)
    distribution_item = models.ForeignKey(DistributionItems, models.DO_NOTHING)
    parent = models.ForeignKey(DistributionItems, models.DO_NOTHING, related_name='distributionitemslink_parent_set', blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'distribution_items_link'


class DistributionResident(models.Model):
    resident = models.ForeignKey('Resident', models.DO_NOTHING)
    creation_date = models.DateTimeField()
    sentence = models.TextField(blank=True, null=True)
    observation = models.TextField(blank=True, null=True)
    distribution = models.ForeignKey(Distribution, models.DO_NOTHING)
    ehpad = models.ForeignKey('Ehpad', models.DO_NOTHING)
    ash = models.BooleanField()
    denture = models.BooleanField()
    special_towel = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'distribution_resident'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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


class ExternalUrls(models.Model):
    external_api_base_url = models.TextField()

    class Meta:
        managed = False
        db_table = 'external_urls'


class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    file_name = models.TextField()
    path = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'file'


class Incident(models.Model):
    incident_id = models.UUIDField(primary_key=True)
    task_event = models.ForeignKey('TaskEvent', models.DO_NOTHING)
    incident_comment = models.TextField()
    incident_status = models.IntegerField()
    ehpad = models.ForeignKey(Ehpad, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'incident'


class Mode(models.Model):
    mode_id = models.AutoField(primary_key=True)
    mode_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'mode'


class ModeEntityUserEntity(models.Model):
    modes = models.OneToOneField(Mode, models.DO_NOTHING, primary_key=True)  # The composite primary key (modes_id, users_id) found, that is not supported. The first column is selected.
    users_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'mode_entity_user_entity'
        unique_together = (('modes', 'users_id'),)


class PeriodicTask(models.Model):
    periodic_task_id = models.AutoField(primary_key=True)
    periodic_task_name = models.TextField()
    periodic_task_duration = models.IntegerField()
    periodic_task_delete_date = models.DateTimeField(blank=True, null=True)
    ehpad = models.ForeignKey(Ehpad, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'periodic_task'


class PeriodicTaskEntityRoomEntity(models.Model):
    periodic_tasks = models.OneToOneField(PeriodicTask, models.DO_NOTHING, primary_key=True)  # The composite primary key (periodic_tasks_id, rooms_id) found, that is not supported. The first column is selected.
    rooms = models.ForeignKey('Room', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'periodic_task_entity_room_entity'
        unique_together = (('periodic_tasks', 'rooms'),)


class PeriodicTaskEntityRoomGroupEntity(models.Model):
    periodic_tasks = models.OneToOneField(PeriodicTask, models.DO_NOTHING, primary_key=True)  # The composite primary key (periodic_tasks_id, room_groups_id) found, that is not supported. The first column is selected.
    room_groups = models.ForeignKey('RoomGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'periodic_task_entity_room_group_entity'
        unique_together = (('periodic_tasks', 'room_groups'),)


class PeriodicTaskEvent(models.Model):
    periodic_task_event_id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    periodic_task = models.ForeignKey(PeriodicTask, models.DO_NOTHING)
    room = models.ForeignKey('Room', models.DO_NOTHING, blank=True, null=True)
    room_group = models.ForeignKey('RoomGroup', models.DO_NOTHING, blank=True, null=True)
    user_id = models.IntegerField()
    ehpad = models.ForeignKey(Ehpad, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'periodic_task_event'


class Post(models.Model):
    name = models.TextField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    ehpad = models.ForeignKey(Ehpad, models.DO_NOTHING)
    start_time = models.TimeField()
    archived_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'


class PostTask(models.Model):
    post = models.ForeignKey(Post, models.DO_NOTHING)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField()
    description = models.TextField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    linked_to = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'post_task'


class PostTaskEventEntity(models.Model):
    id = models.UUIDField(primary_key=True)
    post_task = models.ForeignKey(PostTask, models.DO_NOTHING)
    user_id = models.IntegerField()
    completion_date = models.DateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_task_event_entity'


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

class ProtocolTask(models.Model):
    id = models.UUIDField(primary_key=True)
    protocol = models.ForeignKey(Protocol, models.DO_NOTHING)
    protocol_task_info = models.ForeignKey('ProtocolTaskInfoEntity', models.DO_NOTHING, blank=True, null=True)
    order = models.IntegerField()
    description = models.TextField()
    vocal_description = models.TextField()

    class Meta:
        managed = False
        db_table = 'protocol_task'

class TaskEvent(models.Model):
    id = models.UUIDField(primary_key=True)
    protocol_event = models.ForeignKey(ProtocolEvent, models.DO_NOTHING)
    user_id = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    protocol_task = models.ForeignKey(ProtocolTask, models.DO_NOTHING)
    ehpad = models.ForeignKey(Ehpad, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'task_event'


class ProtocolPriority(models.Model):
    priority_order = models.IntegerField()
    protocol = models.ForeignKey(Protocol, models.DO_NOTHING)
    room = models.ForeignKey('Room', models.DO_NOTHING, blank=True, null=True)
    room_group = models.ForeignKey('RoomGroup', models.DO_NOTHING, blank=True, null=True)
    ehpad = models.ForeignKey(Ehpad, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'protocol_priority'

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_number = models.TextField(unique=True)
    room_group = models.ForeignKey('RoomGroup', models.DO_NOTHING, blank=True, null=True)
    ehpad = models.ForeignKey(Ehpad, models.DO_NOTHING)
    external_api_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room'


class RoomGroup(models.Model):
    name = models.TextField(blank=True, null=True)
    ehpad = models.ForeignKey(Ehpad, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'room_group'


class ProtocolTaskInfoEntity(models.Model):
    id = models.UUIDField(primary_key=True)
    type = models.TextField()
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'protocol_task_info_entity'


class RecordData(models.Model):
    id = models.UUIDField(primary_key=True)
    value = models.IntegerField()
    date = models.DateTimeField()
    user_id = models.IntegerField()
    resident = models.ForeignKey('Resident', models.DO_NOTHING)
    is_synchronized_with_external_api = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'record_data'


class RelFileIncident(models.Model):
    file_incident_id = models.AutoField(primary_key=True)
    file = models.ForeignKey(File, models.DO_NOTHING)
    incident = models.ForeignKey(Incident, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'rel_file_incident'
        unique_together = (('incident', 'file'),)


class RelTaskEventInfo(models.Model):
    id = models.UUIDField(primary_key=True)
    value = models.TextField()
    protocol_task_event = models.ForeignKey('TaskEvent', models.DO_NOTHING)
    protocol_task_info = models.ForeignKey(ProtocolTaskInfoEntity, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'rel_task_event_info'


class Resident(models.Model):
    resident_id = models.AutoField(primary_key=True)
    resident_room = models.ForeignKey('Room', models.DO_NOTHING)
    resident_first_name = models.TextField()
    resident_last_name = models.TextField()
    resident_birth_date = models.TextField(blank=True, null=True)
    resident_social_number = models.TextField(blank=True, null=True)
    ehpad = models.ForeignKey(Ehpad, models.DO_NOTHING)
    external_api_id = models.TextField(blank=True, null=True)
    picture = models.ForeignKey(File, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resident'


class ResidentEntityRestrictionsAlimentaires(models.Model):
    residents = models.OneToOneField(Resident, models.DO_NOTHING, primary_key=True)  # The composite primary key (residents_id, restrictions_alimentaires_id) found, that is not supported. The first column is selected.
    restrictions_alimentaires = models.ForeignKey('RestrictionsAlimentaires', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'resident_entity_restrictions_alimentaires'
        unique_together = (('residents', 'restrictions_alimentaires'),)


class RestrictionsAlimentaires(models.Model):
    name = models.TextField()
    color = models.TextField()

    class Meta:
        managed = False
        db_table = 'restrictions_alimentaires'


class TaskEvent(models.Model):
    id = models.UUIDField(primary_key=True)
    protocol_event = models.ForeignKey(ProtocolEvent, models.DO_NOTHING)
    user_id = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    protocol_task = models.ForeignKey(ProtocolTask, models.DO_NOTHING)
    ehpad = models.ForeignKey(Ehpad, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'task_event'


class UserRole(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'user_role'


class Version(models.Model):
    version_id = models.AutoField(primary_key=True)
    version_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'version'
