import uuid

from django.utils.timezone import now


class UserVerificationMixin:

    def handle_verification(self, user):
        verification_code = user.generate_code()
        user.send_verification_email(verification_code)
        self.request.session['two_factor_code'] = verification_code
        self.request.session['user_id'] = user.id
        verification_uuid = uuid.uuid4()
        self.request.session['verification_uuid'] = str(verification_uuid)
        self.request.session['timestamp'] = now().strftime('%Y-%m-%d %H:%M:%S')

        return verification_uuid
