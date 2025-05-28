import logging


logger = logging.getLogger(__name__)


class Updater:
    system_user_id = 'system'
    system_ai_user_id = 'system_ai'
    system_company_id = 'vegeel'

    @classmethod
    def update001_system_admin_user_company(cls, apps, schema_editor):

        Company = apps.get_model("appdata", "Company")
        ComplianceUser = apps.get_model("appdata", "ComplianceUser")

        vegeel = Company.objects.get(id=cls.system_company_id)
        system_user = ComplianceUser.objects.get(id=cls.system_user_id)
        system_ai_user = ComplianceUser.objects.get(id=cls.system_ai_user_id)

        system_user.company = vegeel
        system_user.save()

        system_ai_user.company = vegeel
        system_ai_user.save()
