import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.contrib import messages


from administration.models import Request, RequestStateEnum, Coupon
from ui.views import SendMailError


class RequestAdmin(admin.ModelAdmin):
    model = Request
    readonly_fields = ("wf_box_number", "wf_box_received_datetime", "weight", "items",
                       "modification_date", "creation_date", "email_sent")
    list_display = ("__str__", "_status", "provider", "wf_box_number", "email_sent")
    list_filter = ("status", "email_sent", "provider")
    search_fields = ("wf_box_number", "tracking_number", "item_name", "wf_box_number", "tracking_number")
    fieldsets = (
        (None, {
            "fields": ("item_name", "tracking_number", "provider", "status", "creation_date", "modification_date")
        },),
        ("WFBox", {
            "fields": ("wf_box_number", "wf_box_received_datetime", "weight", "items", "email_sent")
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

            if self.send_wfbox_alert_email(obj):
                messages.add_message(request, messages.INFO, f"Correo sobre {obj.tracking_number} enviado correctamente a facturas@wfboxcr.com")
            else:
                messages.add_message(request, messages.WARNING, f"El correo no se envio a WFBox. Posiblemente falten datos del pedido con ID: {obj.id}")


            return response
        elif "_track_wfbox" in request.POST and obj.tracking_number:
            messages.add_message(request, messages.INFO, f"Autorastreo exitoso")
            response = HttpResponseRedirect("/admin/administration/request/")
            if referer := request.META.get("HTTP_REFERER"):
                response = HttpResponseRedirect(referer)

            obj.track_wfbox()

            return response
        return super().response_change(request, obj)

    def send_wfbox_alert_email(self, obj: Request):
        if not all([obj.tracking_number, obj.item_name, obj.status != RequestStateEnum.received]):
            return False


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
""" en el paquete lo que va es """ + obj.item_name + """,

Gracias.
"""

        message.attach(MIMEText(email))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(remittent, destination, message.as_string())
            print('Correo enviado correctamente')
            obj.email_sent = True
            obj.save()
        except Exception as e:
            raise SendMailError(str(e))
        finally:
            server.quit()
        return True


class CouponAdmin(admin.ModelAdmin):
    model = Coupon
    list_display = ("__str__", "uses", "expiration")

admin.site.register(Request, RequestAdmin)
admin.site.register(Coupon, CouponAdmin)
