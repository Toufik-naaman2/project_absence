from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.mysql.features import DatabaseFeatures

# 1. إيقاف فحص الإصدار
BaseDatabaseWrapper.check_database_version_supported = lambda self: None

# 2. إيقاف خاصية RETURNING عبر تعديل خصائص الصنف مباشرة
# نستخدم property لإرجاع False دائماً لتجنب خطأ AttributeError
@property
def disable_feature(self):
    return False

DatabaseFeatures.can_return_columns_from_insert = disable_feature
DatabaseFeatures.can_return_rows_from_bulk_insert = disable_feature