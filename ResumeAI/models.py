import mongoengine as me


from datetime import datetime
class CVAppData(me.Document):
    job_desc = me.StringField(max_length=1550)
    cv_file = me.StringField()
    result=me.StringField(max_length=221)
    output=me.StringField()
    resume_pdf=me.FileField()
    created_at = me.DateTimeField(default=datetime.now())