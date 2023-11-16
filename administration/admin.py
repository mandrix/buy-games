import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.contrib import messages


from administration.models import Request, RequestStateEnum
from ui.views import SendMailError


class RequestAdmin(admin.ModelAdmin):
    model = Request
    readonly_fields = ("wf_box_number", "wf_box_received_datetime", "weight", "items",
                       "modification_date", "creation_date")
    list_display = ("__str__", "_status", "wf_box_number")
    list_filter = ("status",)
    search_fields = ("wf_box_number", "tracking_number", "item_name")
    fieldsets = (
        (None, {
            "fields": ("item_name", "tracking_number", "provider", "status", "creation_date", "modification_date")
        },),
        ("WFBox", {
            "fields": ("wf_box_number", "wf_box_received_datetime", "weight", "items",)
        },)
    )

    change_form_template = "overrides/send_wfbox_email.html"

    def _status(self, obj: Request):
        hex_colors = {
            RequestStateEnum.purchased: "#F34E33",
            RequestStateEnum.received: "#70BF2B",
            RequestStateEnum.in_transit_wfbox: "#E70012",
            RequestStateEnum.in_transit: "#FCC10F",
            RequestStateEnum.not_found: "#202C33",
            RequestStateEnum.na: "#202C33",
        }
        return format_html(
            "<div style='padding: 0.5em; background-color: {}; color: #fff; border-radius: 0.25em;'>{}</div>",
            hex_colors[obj.status],
            obj.get_status_display()
        )

    def response_change(self, request, obj: Request):
        if "_correo_a_wfbox" in request.POST and obj.tracking_number:
            response = HttpResponseRedirect("/admin/administration/request/")

            self.send_wfbox_alert_email(obj)

            return response
        return super().response_change(request, obj)

    def send_wfbox_alert_email(self, obj: Request):
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = 'readygamescr@gmail.com'
        smtp_password = 'dasieujszfbbvcew'

        remittent = 'readygamescr@gmail.com'
        destination = "facturas@wfboxcr.com"

        message = MIMEMultipart()
        message['From'] = remittent
        message['To'] = f'{destination}'
        message['Subject'] = 'Envío'

        email = """
Buenas, llegará un paquete para RANDAL MAURICIO FERNANDEZ MARIN cédula 206060879 con este código de rastreo

""" + obj.tracking_number +\
""" en el paquete lo que va es """ + obj.item_name + """

, Gracias.
"""

        message.attach(MIMEText(email))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(remittent, destination, message.as_string())
            print('Correo enviado correctamente')
        except Exception as e:
            raise SendMailError(str(e))
        finally:
            server.quit()


admin.site.register(Request, RequestAdmin)
